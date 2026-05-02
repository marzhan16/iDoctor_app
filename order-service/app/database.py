from typing import List, Dict, Optional
from app.models import Order, OrderStatus
from datetime import datetime, timedelta


# In-memory database (for demo purposes)
orders_db: Dict[str, Order] = {}


class OrderRepository:
    
    @staticmethod
    def save(order: Order) -> Order:
        orders_db[order.id] = order
        return order
    
    @staticmethod
    def get(order_id: str) -> Optional[Order]:
        return orders_db.get(order_id)
    
    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[Order]:
        return list(orders_db.values())[skip:skip + limit]
    
    @staticmethod
    def get_by_user(user_id: str) -> List[Order]:
        return [order for order in orders_db.values() if order.userId == user_id]
    
    @staticmethod
    def update_status(order_id: str, status: OrderStatus) -> Optional[Order]:
        order = orders_db.get(order_id)
        if order:
            order.status = status
            return order
        return None
    
    @staticmethod
    def delete(order_id: str) -> bool:
        if order_id in orders_db:
            del orders_db[order_id]
            return True
        return False