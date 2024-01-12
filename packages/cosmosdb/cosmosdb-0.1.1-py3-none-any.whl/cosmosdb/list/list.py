from typing import Literal
from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosResourceExistsError
import haskellian.asynch as hka
from .. import KEY, ENDPOINT
from ..util import with_client

@with_client
async def dbs(
    *, client: CosmosClient | None, url: str | None = ENDPOINT, key: str | None = KEY
) -> list[dict[str]]:
    """List all databases of the Cosmos DB resource"""
    return await hka.synch(client.list_databases())
    
@with_client
async def containers(
    database: str, *, client: CosmosClient | None, url: str = ENDPOINT, key: str = KEY
) -> CosmosResourceNotFoundError | list[dict[str]]:
    """List all containers of a given database"""
    db = client.get_database_client(database)
    try:
        return await hka.synch(db.list_containers())
    except CosmosResourceNotFoundError as e:
        return e

@with_client
async def items(
    database: str, container: str, *,
    client: CosmosClient | None, url: str = ENDPOINT, key: str = KEY
) -> CosmosResourceNotFoundError | list[dict[str]]:
    """List all items of a given container (within a database)"""
    db = client.get_database_client(database)
    cc = db.get_container_client(container)
    try:
        return await hka.synch(cc.read_all_items())
    except CosmosResourceNotFoundError as e:
        return e