# backend/app/services/elasticsearch_service.py

from elasticsearch import AsyncElasticsearch
from app.models.item import Item

es = AsyncElasticsearch("http://localhost:9200")

async def index_item(item: Item):
    await es.index(index="items", id=item.id, body=item.dict())

async def search_items(query: str, skip: int = 0, limit: int = 100):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "category", "location"]
            }
        },
        "from": skip,
        "size": limit
    }
    result = await es.search(index="items", body=body)
    return [Item(**hit["_source"]) for hit in result["hits"]["hits"]]

async def delete_item_index(item_id: str):
    await es.delete(index="items", id=item_id)