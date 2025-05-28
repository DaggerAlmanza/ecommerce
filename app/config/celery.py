import os
from celery import Celery


def make_celery():
    """Configuración de Celery con Redis"""
    celery = Celery(
        "orders_app",
        broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        include=["app.tasks.order"]
    )
    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_routes={
            "app.tasks.order.process_order": {"queue": "orders_queue"}
        },
        task_default_queue="orders_queue",
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        worker_disable_rate_limits=True
    )
    return celery


celery_app = make_celery()
