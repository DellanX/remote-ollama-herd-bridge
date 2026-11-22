import argparse
import json
from dataclasses import asdict

from vhb.identify import identify
from vhb.tunnel import start_tunnel, wait_for_tunnel
from vhb.herd import start_herd


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vhb-cli",
        description="Vast Herd Bridge CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser("identify")
    subparsers.add_parser("tunnel")
    subparsers.add_parser("wait")
    subparsers.add_parser("herd")
    subparsers.add_parser("run")

    args = parser.parse_args()

    if args.command == "identify":
        instance = identify()

        print(
            json.dumps(
                asdict(instance),
                indent=2,
            )
        )

    elif args.command == "tunnel":
        instance = identify()

        process = start_tunnel(
            instance.host,
            instance.port,
        )

        print(process.pid)

    elif args.command == "wait":
        instance = identify()

        process = start_tunnel(
            instance.host,
            instance.port,
        )

        print(process.pid)
        wait_for_tunnel(process)
    elif args.command == "herd":
        start_herd()

    elif args.command == "run":
        instance = identify()

        process = start_tunnel(
            instance.host,
            instance.port,
        )

        wait_for_tunnel(process)

        start_herd()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()