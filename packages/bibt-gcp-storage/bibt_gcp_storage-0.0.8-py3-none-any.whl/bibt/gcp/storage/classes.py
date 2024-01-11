import logging

import google.auth.transport.requests
from google.api_core import exceptions as google_exceptions
from google.cloud import storage

from .methods import generate_json_nld
from .methods import parse_json_nld
from .params import _BYTES_IN_KB

_LOGGER = logging.getLogger(__name__)


class Client:
    """A Client object may be used to interact with the GCP GCS API.

    :param str project_id: the project within which to create the client.
        Optional, defaults to ``None``.

    :param google.oauth2.credentials.Credentials credentials: the credentials
        object to use when making the API call, if not to use the inferred
        gcloud account.
    """

    def __init__(self, project_id=None, credentials=None):
        self._client = storage.Client(project=project_id, credentials=credentials)

    def _ensure_valid_client(self):
        if not self._client._transport._credentials.valid:
            logging.info(
                "Refreshing client credentials, token expired: "
                f"[{self._client._transport._credentials.expiry}]"
            )
            request = google.auth.transport.requests.Request()
            self._client._transport._credentials.refresh(request=request)
            logging.info(
                f"New expiration: [{self._client._transport._credentials.expiry}]"
            )
        return

    def create_bucket(self, bucket_name, project_id=None, location="US"):
        """Creates a bucket in GCS.

        :param str bucket_name: The desired name for the bucket. Note that
            bucket names must be **universally** unique in GCP, and need to
            adhere to the GCS bucket naming guidelines:
            https://cloud.google.com/storage/docs/naming-buckets
        :param str project_id: The project in which to create the bucket.
            If not set, defaults to the project of the API client.
            Defaults to None
        :param str location: The location within which to create the bucket.
            The locations and regions supported are listed here:
            https://cloud.google.com/storage/docs/locations#available-locations.
            Defaults to ``US``, which is a multi-region configuration.
        :raises e: If bucket creation fails for any reason.
        :return google.cloud.storage.bucket.Bucket: The newly created bucket.
        """
        self._ensure_valid_client()
        if not project_id:
            project = self._client.project
        _LOGGER.info(
            f"Attempting to create bucket [{bucket_name}] in project [{project}] "
            f"in location [{location}]"
        )
        bucket = self._client.bucket(bucket_name)
        try:
            bucket = self._client.create_bucket(
                bucket, project=project, location=location
            )
        except (
            google_exceptions.Forbidden,
            google_exceptions.Conflict,
            google_exceptions.BadRequest,
        ) as e:
            if google_exceptions.Forbidden:
                _LOGGER.error(
                    "Current account does not have required permissions to create "
                    f"buckets in GCP project: [{project}]. Navigate to "
                    f"https://console.cloud.google.com/iam-admin/iam?project={project} "
                    'and add the "Storage Admin" role to the appropriate account.'
                )
            raise e
        _LOGGER.info(
            f"Bucket [{bucket.name}] created successfully in project [{project}]"
        )
        return bucket

    def read_gcs(self, bucket_name, blob_name, decode=True):
        """Reads a blob from GCS.

        :param str bucket_name: The name of the hosting bucket.
        :param str blob_name: The name of the specific blob.
        :param bool decode: Whether to decode the returned bytes as UTF-8
            or simply return the raw bytes. Note that for VERY large files
            decoding may increase execution time significantly.
            Defaults to ``True``.
        :return str or bytes: The data read from the blob.
        """
        self._ensure_valid_client()
        _LOGGER.info(f"Getting gs://{bucket_name}/{blob_name}")
        blob = self._client.get_bucket(bucket_name).get_blob(blob_name)
        contents = blob.download_as_bytes()
        if len(contents) < _BYTES_IN_KB * 0.25:
            _LOGGER.info(
                f"Read {len(contents)} bytes from gs://{bucket_name}/{blob_name}"
            )
        elif len(contents) < _BYTES_IN_KB * 50:
            _LOGGER.info(
                f"Read {len(contents)/_BYTES_IN_KB:.2f} kilobytes from "
                f"gs://{bucket_name}/{blob_name}"
            )
        else:
            _LOGGER.info(
                f"Read {len(contents)/(_BYTES_IN_KB*1000):.2f} megabytes from "
                f"gs://{bucket_name}/{blob_name}"
            )
        if decode:
            _LOGGER.debug("Decoding bucket contents as UTF-8...")
            return contents.decode("utf-8")
        _LOGGER.debug("Returning bucket contents as raw bytes...")
        return contents

    def read_gcs_nldjson(self, bucket_name, blob_name):
        """Read JSON NLD formatted data from GCS and return a list of dicts.

        :param str bucket_name: The name of the host bucket.
        :param str blob_name: The blob from which to read.
        :return list: A list of dicts containing the file data.
        """
        json_nld = self.read_gcs(bucket_name, blob_name, decode=True)
        return parse_json_nld(json_nld)

    def write_gcs(
        self,
        bucket_name,
        blob_name,
        data,
        mime_type="text/plain",
        create_bucket_if_not_found=False,
        timeout=storage.constants._DEFAULT_TIMEOUT,
    ):
        """Write data to a blob in GCS.

        :param str bucket_name: The name of the target bucket.
        :param str blob_name: The name of the blob to contain the data.
        :param str data: The data to write, as a string.
        :param str mime_type: The mime type of the data, (e.g. ``application/json``).
            Defaults to ``text/plain``.
        :param bool create_bucket_if_not_found: Whether to attempt to create the bucket
            if it is not found, or raise an exception. Defaults to ``False``.
        :param int timeout: The request timeout to use, defaults
            to ``storage.constants._DEFAULT_TIMEOUT`` (which is ``60`` seconds).
        :raises e: if the target bucket is not found and
            ``create_bucket_if_not_found!=True``.
        """
        self._ensure_valid_client()
        try:
            bucket = self._client.get_bucket(bucket_name)
        except google_exceptions.NotFound as e:
            if not create_bucket_if_not_found:
                raise e
            _LOGGER.info(
                "Creating not-found bucket as create_bucket_if_not_found==True"
            )
            bucket = self.create_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        _LOGGER.info(
            f"Writing {(len(data)/_BYTES_IN_KB):.2f} kilobytes "
            f"to GCS: gs://{bucket_name}/{blob_name}"
        )
        blob.upload_from_string(data, content_type=mime_type, timeout=timeout)
        _LOGGER.info("Upload complete.")
        return

    def write_gcs_nldjson(self, bucket_name, blob_name, json_data, add_date=False):
        """Write JSON data to GCS in JSON NLD format.

        :param str bucket_name: The name of the target bucket.
        :param str blob_name: The name of the blob to contain the data.
        :param list json_data: A list of dicts to parse into JSON NLD.
        :param bool add_date: Whether or not to add a field "upload_date" to each row
            containing today's date (may be useful for partitioning data in BQ).
            Defaults to ``False``.
        """
        nld_json = generate_json_nld(json_data, add_date)
        self.write_gcs(bucket_name, blob_name, nld_json)
        return
