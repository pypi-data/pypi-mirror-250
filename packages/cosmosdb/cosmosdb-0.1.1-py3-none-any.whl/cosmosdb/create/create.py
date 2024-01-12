from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey
from azure.cosmos.exceptions import CosmosResourceExistsError, CosmosResourceNotFoundError, CosmosHttpResponseError
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def db(
    database: str, *, client: CosmosClient | None = None,
    url: str = ENDPOINT, key: str = KEY
) -> CosmosResourceExistsError | None:
    """Creates a new DB"""
    try:
        await client.create_database(database)
    except CosmosResourceExistsError as e:
        return e

@with_client
async def container(
    database: str, container: str, partition_key: str = "/id", *,
    client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY
) -> CosmosResourceExistsError | None:
    """Creates container within DB (also creates database if needed)"""
    db = await client.create_database_if_not_exists(database)
    key_path = PartitionKey(path=partition_key)
    try:
        await db.create_container(id=container, partition_key=key_path)
    except CosmosResourceExistsError as e:
        return e
    
@with_client
async def item(
    database: str, container: str, body: dict[str], replace: bool = False,
    *, client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY,
) -> CosmosResourceNotFoundError | CosmosResourceExistsError | CosmosHttpResponseError | None:
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    try:
        if replace:
            await cc.upsert_item(body)
        else:
            await cc.create_item(body)
    except (CosmosResourceNotFoundError, CosmosResourceExistsError, CosmosHttpResponseError) as e:
        return e
        