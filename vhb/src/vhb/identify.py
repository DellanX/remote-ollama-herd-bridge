from __future__ import annotations

import json
import os

from vhb.models import InstanceInfo
from vastai import VastAI


def _instance_host(instance: dict) -> str:
    return (
        instance.get("public_ipaddr")
        or instance.get("ssh_host")
        or instance.get("host")
    )


def _instance_port(instance: dict) -> int | None:
    return (
        instance.get("ssh_port")
        or instance.get("ports", {})
        .get("22/tcp", [{}])[0]
        .get("HostPort")
        or None
    )


def identify() -> InstanceInfo:
    """
    Discovery order:

    1. VASTAI_HOST + VASTAI_PORT
    2. VASTAI_INSTANCE_ID
    3. VASTAI_INSTANCE_LABEL
    4. First running instance
    """

    #
    # Manual override
    #

    host = os.getenv("VASTAI_HOST")
    port = os.getenv("VASTAI_PORT")

    if host and port:
        return InstanceInfo(
            id=-1,
            host=host,
            port=int(port) if port else None,
            label="manual",
            status="manual",
        )

    #
    # API configuration
    #

    api_key = os.getenv("VASTAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "VASTAI_API_KEY is required."
        )

    vast = VastAI(api_key=api_key)

    #
    # Instance ID mode
    #

    instance_id = os.getenv("VASTAI_INSTANCE_ID")

    if instance_id:
        instance = vast.show_instance(int(instance_id))

        return InstanceInfo(
            id=instance["id"],
            host=_instance_host(instance),
            port=int(_instance_port(instance) if instance else None),
            label=instance.get("label"),
            status=instance.get("actual_status"),
        )

    #
    # Query all instances
    #

    instances = vast.show_instances()

    running = [
        i
        for i in instances
        if i.get("actual_status") == "running"
    ]

    #
    # Label mode
    #

    label = os.getenv("VASTAI_INSTANCE_LABEL")

    if label:
        matches = [
            i
            for i in running
            if i.get("label") == label
        ]

        matches.sort(
            key=lambda x: x["id"]
        )

        index = int(
            os.getenv(
                "VASTAI_INSTANCE_INDEX",
                "0",
            )
        )

        if index >= len(matches):
            raise RuntimeError(
                f"No instance found for label "
                f"'{label}' at index {index}"
            )

        instance = matches[index]

    #
    # Automatic discovery
    #

    else:
        if not running:
            raise RuntimeError(
                "No running Vast.ai instances found."
            )

        running.sort(
            key=lambda x: x["id"]
        )

        instance = running[0]

    json.dump(
        instance,
        open("instance.json", "w"),
        indent=2,
    )
    return InstanceInfo(
        id=instance["id"],
        host=_instance_host(instance),
        port=_instance_port(instance),
        label=instance.get("label"),
        status=instance.get("actual_status"),
    )