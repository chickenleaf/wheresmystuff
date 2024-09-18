# backend/app/services/matching_service.py

from app.services.elasticsearch_service import es
from app.models.item import Item, ItemStatus

async def find_matches(item_id: str):
    item = await es.get(index="items", id=item_id)
    item_data = item["_source"]

    opposite_status = ItemStatus.FOUND if item_data["status"] == ItemStatus.LOST else ItemStatus.LOST

    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"status": opposite_status}},
                    {"multi_match": {
                        "query": f"{item_data['title']} {item_data['description']}",
                        "fields": ["title", "description"],
                        "fuzziness": "AUTO"
                    }}
                ],
                "should": [
                    {"match": {"category": item_data["category"]}},
                    {"match": {"location": item_data["location"]}}
                ]
            }
        },
        "size": 10
    }

    result = await es.search(index="items", body=body)
    return [Item(**hit["_source"]) for hit in result["hits"]["hits"]]