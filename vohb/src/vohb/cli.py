import argparse
import json
from dataclasses import asdict

from vohb.models import HerdConfig, IdentifyConfig, RunConfig, TunnelConfig

from vohb.identify import identify
from vohb.tunnel import start_tunnel, wait_for_tunnel
from vohb.herd import start_herd

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vohb",
        description="Vast Herd Bridge CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    identify_parser = subparsers.add_parser("identify")
    add_identify_args(identify_parser)

    tunnel_parser = subparsers.add_parser("tunnel")
    add_identify_args(tunnel_parser)
    add_tunnel_args(tunnel_parser)

    herd_parser = subparsers.add_parser("herd")
    add_tunnel_args(herd_parser)
    add_herd_args(herd_parser)

    run_parser = subparsers.add_parser("run")
    add_identify_args(run_parser)
    add_tunnel_args(run_parser)
    add_herd_args(run_parser)

    args = parser.parse_args()


    if args.command is None:
        args.command = "run"

    if args.command == "identify":
        identify_config = identify_config_from_args(args)

        instance = identify(identify_config)

        print(
            json.dumps(
                asdict(instance),
                indent=2,
            )
        )

    elif args.command == "tunnel":
        identify_config = identify_config_from_args(args)
        tunnel_config = tunnel_config_from_args(args)

        instance = identify(identify_config)

        print(
            json.dumps(
                asdict(instance),
                indent=2,
            )
        )

        process = start_tunnel(
            instance.host,
            instance.port,
            tunnel_config,
        )

        print(process.pid)

        wait_for_tunnel(process)

    elif args.command == "herd":
        tunnel_config = tunnel_config_from_args(args)
        herd_config = herd_config_from_args(args)

        ollama_host = (
            f"http://"
            f"{tunnel_config.local_host}:"
            f"{tunnel_config.local_port}"
        )
        
        start_herd(
            ollama_host=ollama_host,
            config=herd_config,
        )
    elif args.command == "run":
        identify_config = identify_config_from_args(args)
        tunnel_config = tunnel_config_from_args(args)
        herd_config = herd_config_from_args(args)

        instance = identify(identify_config)
        
        print(
            json.dumps(
                asdict(instance),
                indent=2,
            )
        )

        process = start_tunnel(
            instance.host,
            instance.port,
            tunnel_config,
        )

        print(process.pid)

        wait_for_tunnel(process)

        ollama_host = (
            f"http://"
            f"{tunnel_config.local_host}:"
            f"{tunnel_config.local_port}"
        )
        
        start_herd(
            ollama_host=ollama_host,
            config=herd_config,
        )

    else:
        parser.print_help()

def add_identify_args(
    parser: argparse.ArgumentParser,
) -> None:

    parser.add_argument("--host")

    parser.add_argument(
        "--port",
        type=int,
    )

    parser.add_argument(
        "--api-key"
    )

    parser.add_argument(
        "--instance-id",
        type=int,
    )

    parser.add_argument(
        "--instance-label",
    )

    parser.add_argument(
        "--instance-index",
        type=int,
    )

def add_tunnel_args(
    parser: argparse.ArgumentParser,
) -> None:

    parser.add_argument(
        "--ssh-user"
    )

    parser.add_argument(
        "--ssh-identity-file"
    )

    parser.add_argument(
        "--local-host"
    )

    parser.add_argument(
        "--local-port",
        type=int,
    )

    parser.add_argument(
        "--remote-host"
    )

    parser.add_argument(
        "--remote-port",
        type=int,
    )

    parser.add_argument(
        "--wait-interval",
        type=float,
    )

    parser.add_argument(
        "--wait-max-retries",
        type=int,
    )

def add_herd_args(
    parser: argparse.ArgumentParser,
) -> None:

    parser.add_argument(
        "--node-id"
    )

    parser.add_argument(
        "--router-url"
    )

    parser.add_argument(
        "--learn-capacity",
        action="store_true",
    )

    parser.add_argument(
        "--log-level"
    )

def identify_config_from_args(
    args,
) -> IdentifyConfig:

    config = (
        IdentifyConfig.from_env()
    )

    if args.host is not None:
        config.host = args.host

    if args.port is not None:
        config.port = args.port

    if args.api_key is not None:
        config.api_key = args.api_key

    if args.instance_id is not None:
        config.instance_id = (
            args.instance_id
        )

    if (
        args.instance_label
        is not None
    ):
        config.instance_label = (
            args.instance_label
        )

    if (
        args.instance_index
        is not None
    ):
        config.instance_index = (
            args.instance_index
        )

    return config

def tunnel_config_from_args(
    args,
) -> TunnelConfig:

    config = (
        TunnelConfig.from_env()
    )

    if args.ssh_user is not None:
        config.ssh_user = (
            args.ssh_user
        )

    if (
        args.ssh_identity_file
        is not None
    ):
        config.ssh_identity_file = (
            args.ssh_identity_file
        )

    if args.local_host is not None:
        config.local_host = (
            args.local_host
        )

    if args.local_port is not None:
        config.local_port = (
            args.local_port
        )

    if args.remote_host is not None:
        config.remote_host = (
            args.remote_host
        )

    if args.remote_port is not None:
        config.remote_port = (
            args.remote_port
        )

    return config

def herd_config_from_args(
    args,
) -> HerdConfig:

    config = HerdConfig.from_env()

    if args.node_id is not None:
        config.node_id = args.node_id

    if args.router_url is not None:
        config.router_url = args.router_url

    if getattr(
        args,
        "learn_capacity",
        False,
    ):
        config.learn_capacity = True

    if args.log_level is not None:
        config.log_level = args.log_level

    return config

if __name__ == "__main__":
    main()