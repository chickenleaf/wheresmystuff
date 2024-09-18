# backend/app/services/celery_tasks.py

from celery import Celery
from app.services.mongodb_service import get_item
from app.services.elasticsearch_service import index_item, delete_item_index

celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery_app.task
def process_item_async(item_id: str):
    item = get_item(item_id)
    if item:
        index_item(item)
    else:
        delete_item_index(item_id)