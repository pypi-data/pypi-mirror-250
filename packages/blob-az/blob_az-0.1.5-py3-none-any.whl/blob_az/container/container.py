from azure.storage.blob.aio import BlobServiceClient
import haskellian.asynch as hka
from .. import CONN_STR
from ..util import with_client
from ..errors import ResourceExistsError, ResourceNotFoundError

@with_client
async def create(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
) -> ResourceExistsError | None:
    try:
        await client.create_container(container)
    except ResourceExistsError as e:
        return e

@with_client
async def delete(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
) -> ResourceNotFoundError | None:
    try:
        await client.delete_container(container)
    except ResourceNotFoundError as e:
        return e
