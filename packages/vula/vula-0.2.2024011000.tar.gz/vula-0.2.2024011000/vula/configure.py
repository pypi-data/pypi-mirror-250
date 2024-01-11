"""
 *vula-configuration* creates *vula.conf* and enables the *vula*
 WireGuard device with *wg-quick*.
"""

import os
import time
from base64 import b64encode
from logging import Logger, getLogger
from os import geteuid, mkdir, system
from sys import platform

import click
from click.exceptions import Exit
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

from .csidh import ctidh, ctidh_parameters
from .status import main as StatusCommand

try:
    from dbus import Boolean, Interface, SystemBus
except ImportError:
    pass
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey

try:
    from systemd import daemon
except ImportError:
    pass

from .common import KeyFile, attrdict
from .constants import _ORGANIZE_KEYS_CONF_FILE, _WG_SERVICES
from .notclick import DualUse


@DualUse.object(
    short_help="Configure system for vula",
    invoke_without_command=True,
)
@click.option(
    "-k",
    "--keys-conf-file",
    default=_ORGANIZE_KEYS_CONF_FILE,
    show_default=True,
    help="YAML configuration file for cryptographic keys",
)
@click.pass_context
class Configure(attrdict):
    def __init__(self, ctx, **kw):
        """
        Configure interface (generating keys if necessary)
        """
        self.update(**kw)
        self.log: Logger = getLogger()
        self.log.debug("Debug level logging enabled")
        self._ctidh = None
        self._ctx = ctx

    def _ensure_root(self):
        if geteuid() != 0:
            self.log.error(
                "unable to configure: needs administrative privileges"
            )
            raise Exit(1)

    def _ensure_linux(self):
        if platform.startswith("linux"):
            if daemon.booted() != 1:
                self.log.error("no systemd: manual configuration required")
                raise Exit(2)

    @DualUse.method()
    def wg_quick_config(self):
        pass

    def _curve25519_keypair_gen(self):
        """
        Generate Curve25519 keypair and return *private* and *public* base64
        encoded values.
        """
        try:
            temp_key = X25519PrivateKey.generate()
        except UnsupportedAlgorithm:
            self.log.debug("Unable to generate Curve25519 keypair")
            raise Exit(3)

        private = b64encode(
            temp_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
        ).decode("utf-8")
        public = b64encode(
            temp_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode("utf-8")
        return private, public

    def _ed25519_keypair_gen(self):
        """
        Generate a seed for the Ed25519 verify keypair used by vula.

        """
        self.log.debug("Generating vula Ed25519 keypair...")
        signing_key = SigningKey.generate()
        private = signing_key.encode(encoder=Base64Encoder).decode()
        verify_key = signing_key.verify_key
        public = b64encode(verify_key.encode()).decode()
        return private, public

    def _ctidh_keypair_gen(self):
        if self._ctidh is None:
            self.log.debug("Initializing CTIDH")
            self._ctidh = ctidh(ctidh_parameters)
        self.log.debug("Generating CTIDH keypair")
        sk = self._ctidh.generate_secret_key()
        pk = sk.derive_public_key()
        self.log.debug("CTIDH keypair generated")
        public = b64encode(pk).decode()
        private = b64encode(sk).decode()
        return private, public

    @DualUse.method()
    def generate_or_read_keys(self) -> KeyFile:
        path = self.keys_conf_file
        keys = None
        try:
            keys = KeyFile.from_yaml_file(path)
            os.chmod(path, mode=0o600)
        except FileNotFoundError:
            self.log.info("Keys file not found")
        except Exception as ex:
            backup_path = path + '.' + str(time.time())
            self.log.info(
                "Invalid keys file: (%s); Saving old file as %s",
                ex,
                backup_path,
            )
            os.rename(path, backup_path)
        if keys is None:
            self.log.info("Generating keys...")
            keys = self.genkeys()
            keys.write_yaml_file(path, mode=0o600, autochown=True)
        return keys

    @DualUse.method()
    def genkeys(self):
        keys = KeyFile(
            zip(
                (
                    "pq_ctidhP512_sec_key",
                    "pq_ctidhP512_pub_key",
                    "vk_Ed25519_sec_key",
                    "vk_Ed25519_pub_key",
                    "wg_Curve25519_sec_key",
                    "wg_Curve25519_pub_key",
                ),
                (
                    self._ctidh_keypair_gen()
                    + self._ed25519_keypair_gen()
                    + self._curve25519_keypair_gen()
                ),
            )
        )
        return keys

    def _reconfigure_restart_systemd_services(
        self,
        mode: str = "replace",
        restart: bool = False,
    ):
        """
        Use DBus to check the status of, enable, and restart systemd services.
        """
        system_bus = SystemBus()
        systemd = system_bus.get_object(
            "org.freedesktop.systemd1", "/org/freedesktop/systemd1"
        )
        systemd_manager = Interface(
            systemd, "org.freedesktop.systemd1.Manager"
        )

        if restart:
            for service in _WG_SERVICES:
                systemd_manager.RestartUnit(service, mode)
                self.log.info("Restarted service: %s", service)
        else:
            for service in _WG_SERVICES:
                current_state = systemd_manager.GetUnitFileState(service)
                if current_state == "enabled":
                    self.log.info(
                        "systemd service %s is already enabled", service
                    )
                else:
                    self.log.info(
                        "systemd service %s was %s; enabling it",
                        service,
                        current_state,
                    )

                    systemd_manager.EnableUnitFiles(
                        [service], Boolean(False), Boolean(True)
                    )
                    current_state = systemd_manager.GetUnitFileState(service)
                    self.log.info("%s: %s", service, current_state)
        system_bus.close()

    @DualUse.method()
    def configure_system(self):
        self._ensure_root()
        if platform.startswith("linux"):
            self.log.info("Adding firewall exception with ufw")
            system("ufw allow 5354/udp")
        try:
            mkdir("/etc/wireguard/")
        except FileExistsError:
            pass
        if platform.startswith("linux"):
            system("systemctl daemon-reload")
            system("systemctl restart systemd-sysusers")
            system("systemctl reload dbus")
        if platform.startswith("linux"):
            # XXX: this line is left here to ease upgrades from systems where
            # the wg-quick@vula service is in a degraded state. it should not
            # ever be in a degraded state anymore after this code has run once,
            # now that we've removed the call to "wg-quick up vula". so, after
            # all existing installs have upgraded, we should remove this line:
            system("wg-quick down vula")

    @DualUse.method()
    def nsswitch(self):
        self._ensure_root()
        self.log.info("configuring nsswitch to respect our petname system")
        system(
            "perl -pi -e 'm/vula /s || s/^(hosts:\\s+)/${1}vula /'"
            " /etc/nsswitch.conf"
        )

    @DualUse.method()
    def systemd_restart(self):
        self._ensure_root()
        if platform.startswith("linux"):
            _reconfigure_restart_systemd_services()  # noqa: F821
            _reconfigure_restart_systemd_services(restart=True)  # noqa: F821
            time.sleep(1.5)
        # FIXME: this causes a non-zero exit status sometimes, if the organize
        # service is "activating" instead of "active". the sleep could be
        # increased, or we could perhaps hang around to find out what happened
        # via some dbus event or something?
        self._ctx.invoke(StatusCommand)


main = Configure.cli

if __name__ == "__main__":
    main()
