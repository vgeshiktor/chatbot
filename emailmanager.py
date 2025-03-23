""" Email manager module """

import base64
import calendar
import datetime
import mimetypes
import os
from pathlib import Path
import pprint
from typing import Any, Dict, List

import dateutil.relativedelta
import dotenv
import httpx

from salaryops.msgraphhelper import (
    MS_GRAPH_ME_FOLDERS_EP,
    MS_GRAPH_ME_MSGS_EP,
    MS_GRAPH_ME_SEND_EMAIL_EP,
    MsGraphHelper,
)


class EmailManager:
    """EmailManager class to manage emails"""

    def __init__(
        self, config: Dict[str, Any], app_id: str, secret: str, scopes: List[str]
    ) -> None:
        """Initialize EmailManager"""

        self.config = config
        self.access_token = ""
        self.msgraphhelper = MsGraphHelper(app_id, secret, scopes)

    def login(self) -> None:
        """Login to Microsoft Graph API"""
        self.access_token = self.msgraphhelper.get_access_token()

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_messages_by_filter(
        self,
        filter_str: str,
        forder_id: str | None = None,
        fields: str = "*",
        top: int = 5,
        max_results: int = 10,
    ) -> List[Dict[str, Any]] | None:
        """Get messages by filter"""
        # configure endpoint url
        if forder_id is None:
            endpoint = f"{MS_GRAPH_ME_MSGS_EP}"
        else:
            endpoint = f"{MS_GRAPH_ME_FOLDERS_EP}/{forder_id}/messages"

        headers = self.get_auth_headers()

        # filter and search parameters can't be used together
        params: Dict[str, Any] | None = {
            "$filter": filter_str,
            "$select": fields,
            "$top": min(top, max_results),
        }

        messages: List[Dict[str, Any]] = []
        next_link = endpoint

        while next_link and len(messages) < max_results:
            response = httpx.get(next_link, headers=headers, params=params)
            if response.status_code != 200:
                raise httpx.RequestError(f"Failed to retrieve emails: {response.text}")

            json_response = response.json()
            messages.extend(json_response.get("value", []))
            next_link = json_response.get("@odata.nextLink", None)
            params = None

            if next_link and len(messages) + top > max_results:
                params = {
                    "$top": min(top, max_results - len(messages)),
                }

        return messages[:max_results]

    def get_attachments(self, message_id: str) -> List[Dict[str, Any]] | Any:
        """Get attachments for a message"""
        attachments_endpoint = f"{MS_GRAPH_ME_MSGS_EP}/{message_id}/attachments"
        response = httpx.get(attachments_endpoint, headers=self.get_auth_headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def download_attachment(
        self, message_id: str, attachment_id: str, attachments_name: str, folder: str
    ) -> bool:
        """Download attachment for a message"""
        downwload_ep = (
            f"{MS_GRAPH_ME_MSGS_EP}/{message_id}/attachments/{attachment_id}/$value"
        )
        response = httpx.get(downwload_ep, headers=self.get_auth_headers())
        response.raise_for_status()
        file = Path(folder) / attachments_name
        file.write_bytes(response.content)
        return True

    def search_folders(self, folder_name: str) -> Any:
        """
        The function `search_folders` searches for a specific folder 
        by name in Microsoft Graph API.
        
        :param folder_name: The `search_folders` method is used to
        search for a folder by its display name in Microsoft Graph API.
        The `folder_name` parameter is the name of the folder you want to
        search for in the list of folders returned by the API.
        The method will return the ID of the folder if it exists.
        :return: The `search_folders` method returns the ID of the
        folder with the specified `folder_name` if it exists in the list of folders
        obtained from the Microsoft Graph API. If a folder with the given name is found,
        its ID is returned. If no matching folder is found, `None`
        is returned.
        """

        folders_endpoint = f"{MS_GRAPH_ME_FOLDERS_EP}"
        response = httpx.get(folders_endpoint, headers=self.get_auth_headers())
        response.raise_for_status()
        folders = response.json().get("value", [])
        return next(
            (
                folder["id"]
                for folder in folders
                if folder["displayName"].lower() == folder_name
            ),
            None,
        )


def main() -> None:
    """Main function"""

    # Load environment variables from .env file
    dotenv.load_dotenv()
    app_id: str = os.getenv("APP_ID", "")
    secret: str = os.getenv("SECRET", "")
    scopes: List[str] = ["User.Read", "Mail.ReadWrite", "Mail.Send"]

    config: Dict[str, Any] = {}

    email_manager = EmailManager(config, app_id, secret, scopes)
    email_manager.login()
    folder_id = email_manager.search_folders('inbox')
    print(folder_id)


if __name__ == "__main__":
    main()
