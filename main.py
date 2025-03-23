import os
from typing import List
import dotenv
from dataset_management import DatasetManager


def main() -> None:
    """Main function"""

    # Load environment variables from .env file
    dotenv.load_dotenv()
    app_id: str = os.getenv("APP_ID", "")
    secret: str = os.getenv("SECRET", "")
    dataset_folder: str = os.getenv("DATASET_FOLDER", "")
    scopes: List[str] = ["User.Read", "Mail.ReadWrite", "Mail.Send"]

    config = {
        "DATASET_FOLDER": dataset_folder,
    }

    dataset_manager = DatasetManager(config, app_id, secret, scopes)

    # download the data from the email
    dataset_manager.download_data()

    # expand dataset by breaking pdfs to pages
    dataset_manager.expand_dataset()


if __name__ == "__main__":
    main()
