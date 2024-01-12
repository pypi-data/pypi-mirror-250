from azure.storage.blob.aio import BlobServiceClient
import haskellian.asynch as hka
from .. import CONN_STR
from ..util import with_client
from ..errors import ResourceNotFoundError

@with_client
async def containers(
    *, client: BlobServiceClient, conn_str: str = CONN_STR
) -> list[dict[str]]:
    return await hka.synch(client.list_containers())

@with_client
async def blobs(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
) -> ResourceNotFoundError | list[str]:
    try:
        cc = client.get_container_client(container)
        return await hka.synch(cc.list_blob_names())
    except ResourceNotFoundError as e:
        return e