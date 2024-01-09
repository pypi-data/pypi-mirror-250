from datetime import datetime, timedelta
from typing import Optional

import inquirer
from rich.console import Console
from rich.table import Table
from typer import Argument, Option, Typer

from ..models.api_keys import APIKeyCreate, APIKeyUpdate
from ..routes import V1Routes
from ..utils import make_request_with_api_key, parse_config_file

console = Console()
api_keys_app = Typer()


class APIKeysManager:
    @staticmethod
    def _get_api_keys():
        response = make_request_with_api_key("GET", V1Routes.LIST_API_KEYS)
        return response.json()["items"]

    @staticmethod
    def _select_api_key(prompt_message):
        api_keys = APIKeysManager._get_api_keys()
        choices = [(key["name"], key["id"]) for key in api_keys]
        questions = [
            inquirer.List(
                "api_key", message=prompt_message, choices=choices, carousel=True
            )
        ]
        answers = inquirer.prompt(questions)
        return answers["api_key"]

    @staticmethod
    def _print_table(items, columns):
        table = Table(show_header=True, header_style="green", padding=(0, 1, 0, 1))
        for col in columns:
            table.add_column(col)

        for item in items:
            table.add_row(*item, end_section=True)

        console.print(table)


@api_keys_app.command("create")
def create_api_key(config_file: Optional[str] = Option(None, "--config-file", "-c")):
    if config_file:
        api_key_create = parse_config_file(config_file, APIKeyCreate)
    else:
        name = inquirer.text(message="Enter the name of the API key")
        expiration_days = inquirer.text(
            message="Enter the number of days until expiration", default="30"
        )
        expiration_date = datetime.now() + timedelta(days=int(expiration_days))
        expires_at = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
        api_key_create = APIKeyCreate(name=name, expires_at=expires_at
        )

    response = make_request_with_api_key(
        "POST", V1Routes.API_KEYS, api_key_create.model_dump_json()
    )
    json_response = response.json()

    if response.status_code == 201:
        console.print(f"Successfully created API key {json_response['key']}")
    else:
        console.print(f"Error creating API key: {json_response['detail']}")


@api_keys_app.command("update")
def update_api_key(
    api_key_id: Optional[str] = Argument(
        None, help="The UUID of the API key to update."
    ),
    config_file: Optional[str] = Option(
        None,
        "--config-file",
        "-c",
        help="The path to a JSON file with the update data.",
    ),
):
    api_key_id = APIKeysManager._select_api_key("Choose the API key to update")

    if config_file:
        api_key_update = parse_config_file(config_file, APIKeyUpdate)
    else:
        name = inquirer.text(
            message="Enter the updated name of the API key", default=None
        )
        expiration_days = inquirer.text(
            message="Enter the number of days until expiration", default="30"
        )
        expiration_date = datetime.now() + timedelta(days=int(expiration_days))
        expires_at = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
        api_key_update = APIKeyUpdate(name=name, expires_at=expires_at)

    response = make_request_with_api_key(
        "PATCH", f"{V1Routes.API_KEYS}/{api_key_id}", api_key_update.model_dump_json()
    )
    json_response = response.json()

    if response.status_code == 200:
        console.print(f"Successfully updated API key {json_response['id']}")
    else:
        console.print(f"Error updating API key: {json_response['detail']}")


@api_keys_app.command("get")
def get_api_key(
    api_key_id: Optional[str] = Argument(None, help="The UUID of the API key to get."),
):
    api_key_id = APIKeysManager._select_api_key("Choose the API key to get")
    response = make_request_with_api_key("GET", f"{V1Routes.API_KEYS}/{api_key_id}")
    json_response = response.json()

    if response.status_code == 200:
        console.print(json_response)
    else:
        console.print(f"Error getting API key: {json_response['detail']}")


@api_keys_app.command("list")
def list_api_keys():
    api_keys = APIKeysManager._get_api_keys()
    items = [(key["id"], key["name"]) for key in api_keys]
    APIKeysManager._print_table(items, ["ID", "Name"])


@api_keys_app.command("delete")
def delete_api_key(
    api_key_id: Optional[str] = Argument(
        None, help="The UUID of the API key to delete."
    ),
):
    api_key_id = APIKeysManager._select_api_key("Choose the API key to delete")
    response = make_request_with_api_key("DELETE", f"{V1Routes.API_KEYS}/{api_key_id}")

    if response.status_code == 204:
        console.print(f"Successfully deleted API key {api_key_id}")
    else:
        json_response = response.json()
        console.print(f"Error deleting API key: {json_response['detail']}")
