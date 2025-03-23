from typing import Any, Dict, List
from mimetypes import guess_extension

from emailmanager import EmailManager


class DatasetManager:

    def __init__(
        self,
        config: Dict[str, Any],
        app_id: str,
        secret: str,
        scopes: List[str]
    ):
        """Initialize dataset management"""
        self.email_manager = EmailManager(config, app_id, secret, scopes)
        self.downloads_folder = config["DATASET_FOLDER"]

    def download_data(self) -> None:
        """Download the data from the email"""

        self.email_manager.login()
        print("Logged in to email")

        downloads_folder = self.downloads_folder

        # create query filter
        # sal_filter = (
        #     r"from/emailAddress/address eq 'yael@damsalem.co.il' and "
        #     r"contains(subject, 'שכר') and "
        #     r"hasAttachments eq true"
        # )

        sal_filter = (
            # r"from/emailAddress/address eq 'yael@damsalem.co.il' and "
            r"contains(subject, 'שכר') and "
            r"hasAttachments eq true and "
            r"receivedDateTime ge 2024-10-01T00:00:00Z"
        )

        print("Getting messages...")
        messages = self.email_manager.get_messages_by_filter(sal_filter, "inbox")

        print("Downloading data...")
        for message in messages:  # type: ignore
            attachments = self.email_manager.get_attachments(message["id"])
            for attachment in attachments:
                attachment_extension = guess_extension(
                    attachment["contentType"], strict=True
                )
                attachment_name = (
                    f'sal-{attachment["lastModifiedDateTime"]}{attachment_extension}'
                )
                attachment_name = attachment_name.replace(":", "-")
                self.email_manager.download_attachment(  # type: ignore
                    message["id"], attachment["id"], attachment_name,
                    str(downloads_folder)
                )

    def expand_dataset(self) -> None:
        """Expand dataset by breaking pdfs to pages"""
        print("Expanding dataset...")
