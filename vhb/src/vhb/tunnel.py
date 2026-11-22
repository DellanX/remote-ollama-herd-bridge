from __future__ import annotations

import os
import time
import subprocess
from pathlib import Path
from typing import Optional
import urllib.request

from vhb.models import TunnelConfig

def prepare_private_key() -> Optional[str]:
    """
    Creates a temporary SSH private key file if
    SSH_PRIVATE_KEY is supplied.

    Returns the key path or None.
    """

    private_key = os.getenv("SSH_PRIVATE_KEY")

    if not private_key:
        return None

    ssh_dir = Path("/root/.ssh")
    ssh_dir.mkdir(parents=True, exist_ok=True)

    key_file = ssh_dir / "id_vhb"

    key_file.write_text(private_key)
    key_file.chmod(0o600)

    return str(key_file)


def build_ssh_command(
    host: str,
    port: int,
    config: TunnelConfig,
) -> list[str]:
    """
    Construct SSH tunnel command.
    """

    config = config if config is not None else TunnelConfig.from_env()

    ssh_user = config.ssh_user

    identity_file = (
        prepare_private_key()
        or config.ssh_identity_file
    )

    cmd = [
        "ssh",
        "-o",
        "ExitOnForwardFailure=yes",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-N",
        "-L",
        f"{config.local_host}:{config.local_port}:{config.remote_host}:{config.remote_port}",
        "-p",
        str(port),
    ]

    if identity_file:
        cmd.extend(
            [
                "-i",
                identity_file,
            ]
        )

    cmd.append(f"{ssh_user}@{host}")

    return cmd


def start_tunnel(
    host: str,
    port: int,
    config: TunnelConfig | None = None,
) -> subprocess.Popen:
    """
    Start the SSH tunnel.

    Returns:
        subprocess.Popen
    """

    cmd = build_ssh_command(host, port, config)

    print(
        f"Starting SSH tunnel to "
        f"{host}:{port}"
    )

    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

def wait_for_tunnel(
    process: subprocess.Popen,
    config: TunnelConfig | None = None,
) -> None:
    config = config if config is not None else TunnelConfig.from_env()
    for attempt in range(
        1,
        config.wait_max_retries + 1,
    ):
        if process.poll() is not None:
            raise RuntimeError(
                "SSH tunnel exited unexpectedly."
            )

        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:11434/api/tags",
                timeout=2,
            ):
                print(
                    "Tunnel ready."
                )
                return

        except Exception:
            pass

        print(
            f"Waiting for tunnel "
            f"({attempt}/{config.wait_max_retries})"
        )

        time.sleep(config.wait_interval)

    raise RuntimeError(
        "Tunnel never became available."
    )