from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def _safe_group_send(group: str, message: dict):
    """
    Don't crash app if Redis is not running.
    If channel layer is unavailable, just skip broadcasting.
    """
    try:
        channel_layer = get_channel_layer()
        if not channel_layer:
            return
        async_to_sync(channel_layer.group_send)(group, message)
    except Exception:
        # Redis not running / connection refused -> ignore
        return

def broadcast_table_update(table):
    _safe_group_send(
        "dashboard",
        {
            "type": "table_update",
            "payload": {
                "table_id": table.id,
                "number": table.number,
                "status": table.status,
                "capacity": table.capacity,
            },
        },
    )

def broadcast_kitchen_new_order(order):
    _safe_group_send(
        "kitchen",
        {
            "type": "new_order",
            "payload": {
                "order_id": order.id,
                "table_number": order.table.number,
                "status": order.status,
            },
        },
    )
