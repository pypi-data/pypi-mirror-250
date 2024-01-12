from azure.cosmos.aio import CosmosClient
from ..errors import CosmosResourceNotFoundError
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def db(
    database: str, *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
) -> CosmosResourceNotFoundError | None:
    async with CosmosClient(url=url, credential=key) as client:
        try:
            await client.delete_database(database)
        except CosmosResourceNotFoundError as e:
            return e

@with_client     
async def container(
    database: str, container: str, *, client: CosmosClient, url: str = ENDPOINT, key: str = KEY
) -> CosmosResourceNotFoundError | None:
    db = client.get_database_client(database)
    try:
        await db.delete_container(container)
    except CosmosResourceNotFoundError as e:
        return e

@with_client
async def item(
    database: str, container: str, id: str, partition_key: str | None = None,
    *, client: CosmosClient, url: str | None = ENDPOINT, key: str | None = KEY
) -> CosmosResourceNotFoundError | None:
    """Delete an item given its `id` and `partition_key`
    - If `partition_key is None`, it'll be set to `id`
    """
    partition_key = partition_key or id
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    try:
        await cc.delete_item(id, partition_key)
    except CosmosResourceNotFoundError as e:
        return e