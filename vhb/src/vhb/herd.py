from fleet_manager.cli.node_cli import start as start_herd_node
import os

def start_herd() -> None:
    start_herd_node(
        node_id=os.getenv("NODE_ID", ""),
        ollama_host=os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434",
        ),
        router_url=os.getenv(
            "ROUTER_URL",
            "",
        ),
        learn_capacity=os.getenv(
            "LEARN_CAPACITY",
            "false",
        ).lower()
        == "true",
        log_level=os.getenv(
            "LOG_LEVEL",
            "INFO",
        ),
    )