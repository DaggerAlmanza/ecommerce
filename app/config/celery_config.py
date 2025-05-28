import os
from celery import Celery


def make_celery():
    """Configuración de Celery con Redis"""
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", "6379")

    redis_url = f"redis://{redis_host}:{redis_port}/0"

    celery = Celery(
        "orders_app",
        broker=redis_url,
        backend=redis_url,
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
