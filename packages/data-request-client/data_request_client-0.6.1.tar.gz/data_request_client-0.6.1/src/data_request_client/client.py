from typing import List, Optional
from uuid import UUID

import httpx

from data_request_client.models import (
    CreateDataRequestModel,
    ReadDataRequest,
    Status,
    UpdateDataRequestModel,
)
from data_request_client.settings import settings


class DataRequestsClient:
    """
    Client to interact with the DataRequests API.

    Usage:
    with DataRequestsClient(settings=settings) as client:
        client.create_data_request(some_data)
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the client with the given settings.

        Parameters:
            settings (ClientSettings): The client settings containing API base URL and API key.
        """
        self.base_url = base_url or settings.BASE_URL
        self.api_key = api_key or settings.API_KEY.get_secret_value()
        self.client = None

    def __enter__(self):
        """
        Context manager enter method. Initializes the httpx client.
        """
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"x-api-key": self.api_key},
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method. Closes the httpx client.
        """
        self.close()

    def _ensure_client_open(self):
        """
        Private helper method to ensure that the client is open before making a request.
        Raises a RuntimeError if the client is not open.
        """
        if self.client is None:
            raise RuntimeError(
                "Client is not open. Ensure you're using this within a 'with' context or have manually opened the client."
            )

    def _check_error_response(self, response: httpx.Response):
        """
        Private helper method to check for an error response.
        Raises a RuntimeError if the response is an error.
        """
        if response.status_code >= 400:
            raise RuntimeError(
                f"Received error response from API: {response.status_code} {response.text}"
            )

    def create_data_request(self, item: CreateDataRequestModel) -> ReadDataRequest:
        """
        Create a new data request.

        Parameters:
            item (CreateDataRequestModel): Data request details to be created.

        Returns:
            ReadDataRequest: Details of the created data request.
        """
        self._ensure_client_open()
        response = self.client.post("/data-requests/", json=item.model_dump())
        response.raise_for_status()
        return ReadDataRequest(**response.json())

    def update_data_request(self, item: UpdateDataRequestModel) -> ReadDataRequest:
        """
        Update an existing data request.

        Parameters:
            item (UpdateDataRequestModel): Data request details to be updated.

        Returns:
            ReadDataRequest: Details of the updated data request.
        """
        self._ensure_client_open()
        # convert UUID to string
        payload = item.model_dump(exclude_unset=True, exclude_defaults=True)
        payload["id"] = str(payload["id"])
        response = self.client.put("/data-requests/", json=payload)
        response.raise_for_status()
        return ReadDataRequest(**response.json())

    def read_data_request(self, data_request_id: UUID) -> ReadDataRequest:
        """
        Retrieve details of a specific data request by its ID.

        Parameters:
            data_request_id (UUID): Unique identifier of the data request.

        Returns:
            ReadDataRequest: Details of the retrieved data request.
        """
        self._ensure_client_open()
        response = self.client.get(f"/data-requests/id/{data_request_id}")
        response.raise_for_status()
        return ReadDataRequest(**response.json())

    def delete_data_request(self, data_request_id: UUID):
        """
        Delete a specific data request by its ID.

        Parameters:
            data_request_id (UUID): Unique identifier of the data request to be deleted.

        Returns:
            None
        """
        self._ensure_client_open()
        response = self.client.delete(f"/data-requests/id/{data_request_id}")
        response.raise_for_status()

    def acknowledge_data_request(self, data_request_id: str) -> ReadDataRequest:
        """
        Acknowledge a data request.

        Parameters:
            data_request_id (str): Identifier of the data request to be acknowledged.

        Returns:
            ReadDataRequest: Details of the acknowledged data request.
        """
        self._ensure_client_open()
        response = self.client.post(f"/data-requests/acknowledge/{data_request_id}")
        response.raise_for_status()
        return ReadDataRequest(**response.json())

    def set_status(self, status: Status, data_request_id: str) -> ReadDataRequest:
        """
        Set the status for a specific data request.

        Parameters:
            status (Status): The new status to be set.
            data_request_id (str): Identifier of the data request to be updated.

        Returns:
            ReadDataRequest: Details of the data request with the updated status.
        """
        self._ensure_client_open()
        response = self.client.post(f"/data-requests/status/{status}/{data_request_id}")
        response.raise_for_status()
        return ReadDataRequest(**response.json())

    def read_data_requests(
        self, status: Optional[Status] = None
    ) -> List[ReadDataRequest]:
        """
        Retrieve a list of data requests. Optionally, filter by status.

        Parameters:
            status (Optional[Status]): The status to filter by. If not provided, retrieves all data requests.

        Returns:
            List[ReadDataRequest]: List of retrieved data requests.
        """
        self._ensure_client_open()
        params = {"status": status} if status else {}
        response = self.client.get("/data-requests/", params=params)
        response.raise_for_status()
        return [ReadDataRequest(**item) for item in response.json()]

    def download_data_request(
        self, data_request_id: UUID, analysis_uuid: UUID, index: int
    ) -> dict:
        """
        Download the data for a specific data request.

        Parameters:
            data_request_id (str): Identifier of the data request to be downloaded.
            index (int): Index of the data to be downloaded.

        Returns:
            dict: Data for the requested data request.
        """
        self._ensure_client_open()
        response = self.client.get(
            f"/data-requests/download/{data_request_id}/{analysis_uuid}/{index}"
        )
        self._check_error_response(response)
        # download data from the presigned URL
        download_response = httpx.get(response.json())
        if download_response.status_code != 200:
            raise RuntimeError(
                f"Failed to download data from {response.json()}: {download_response.text}"
            )
        return download_response.json()

    def download_output(
        self,
        data_request_id: UUID,
        analysis_uuid: Optional[UUID] = None,
        index: Optional[int] = None,
        output_name: Optional[str] = None,
    ):
        if index is None and output_name is None:
            raise ValueError("Must provide either index or output_name.")
        if index is None:
            data_request = self.read_data_request(data_request_id)
            if data_request.analysis is None:
                raise ValueError(
                    f"Data request with id '{data_request_id}' does not have an analysis yet. It is in status '{data_request.status}'."
                )
            analysis_dict = {val["analysis_uuid"]: val for val in data_request.analysis}

            if analysis_uuid is None:
                if len(analysis_dict) > 1:
                    raise ValueError(
                        f"Data request with id '{data_request_id}' has multiple analyses. Please provide analysis_uuid."
                    )
                analysis_uuid = list(analysis_dict.keys())[0]
            elif analysis_uuid not in analysis_dict:
                raise ValueError(
                    f"Analysis with uuid '{analysis_uuid}' not found in data request with id '{data_request_id}'."
                )

            analysis = analysis_dict[analysis_uuid]
            output = [
                i
                for i, output in enumerate(analysis["outputs"])
                if output["output_name"] == output_name
            ]
            if len(output) == 0:
                raise ValueError(f"Output {output_name} not found.")
            elif len(output) > 1:
                raise ValueError(f"Multiple outputs with name {output_name} found.")
            index = output[0]
        data = self.download_data_request(data_request_id, analysis_uuid, index)
        return data

    def close(self):
        """
        Close the client connection.
        """
        if self.client:
            self.client.close()
