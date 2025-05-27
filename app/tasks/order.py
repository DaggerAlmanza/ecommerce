from app.config.celery import celery_app
from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.order.process_order")
def process_order(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tarea asíncrona para procesar la creación de órdenes
    Args:
        user_data: Diccionario con información del usuario
    Returns:
        Diccionario con el resultado de la operación
    """
    print(f"Procesando la orden {user_data}")
    try:
        self.update_state(
            state="PROCESSING",
            meta={
                "message": "Iniciando procesamiento de orden",
                "user_id": user_data.get("id")
            }
        )
        from app.services.orders import OrdersService
        orders_service = OrdersService()
        result = orders_service._process_order_creation(user_data)
        self.update_state(
            state="SUCCESS",
            meta={
                "message": result.get("message"),
                "user_id": user_data.get("id"),
                "is_created": result.get("data")
            }
        )
        return result
    except Exception as exc:
        logger.error(f"Error procesando orden para usuario {
            user_data.get("id")}: {str(exc)}"
        )
        print(f"Error procesando orden para usuario {
            user_data.get("id")
        }: {exc}"
        )
        self.update_state(
            state="FAILURE",
            meta={
                "message": "Error procesando la orden",
                "user_id": user_data.get("id")
            }
        )
        raise exc
