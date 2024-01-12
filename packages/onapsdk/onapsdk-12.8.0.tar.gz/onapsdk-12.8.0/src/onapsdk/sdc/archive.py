"""SDC archive module."""

from typing import Iterator, TYPE_CHECKING
from urllib.parse import urljoin

from . import SDC
from .service import Service


class SdcArchive(SDC):
    """Class to read SDC archive.

    Unfortunately there is only one endpoint to get archived elements from SDC
        and there is no way to filter resorces using API, so that class is going
        to get all archived objects, parse them and retrurn on demand.
    """

    ARCHIVE_ENDPOINT = "sdc2/rest/v1/catalog/archive/"
    ARCHIVE_URL = urljoin(SDC.base_back_url, ARCHIVE_ENDPOINT)

    @classmethod
    def get_archived_services(cls) -> Iterator[Service]:
        for archived_service_json in cls.send_message_json(
            "GET",
            "Get archived resources",
            cls.ARCHIVE_URL,
        ).get("services", []):
            yield Service.import_from_sdc(archived_service_json)
