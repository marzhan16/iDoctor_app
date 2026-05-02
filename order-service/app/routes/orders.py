from fastapi import APIRouter, HTTPException, status
from app.models import OrderCreate, Order, OrderUpdate, OrderStatus
from app.database import OrderRepository
from datetime import timedelta
import random

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """Create a new order (reservation request)"""
    
    # Calculate end time and total price
    end_time = order_data.startTime + timedelta(hours=order_data.duration)
    
    # Mock price calculation (€5 per hour for demo)
    price_per_hour = 5.0
    total_price = price_per_hour * order_data.duration
    
    order = Order(
        parkingId=order_data.parkingId,
        userId=order_data.userId,
        duration=order_data.duration,
        startTime=order_data.startTime,
        endTime=end_time,
        totalPrice=total_price
    )
    
    return OrderRepository.save(order)


@router.get("/", response_model=list[Order])
async def get_all_orders(skip: int = 0, limit: int = 100):
    """Get all orders with pagination"""
    return OrderRepository.get_all(skip, limit)


@router.get("/user/{user_id}", response_model=list[Order])
async def get_orders_by_user(user_id: str):
    """Get all orders for a specific user"""
    return OrderRepository.get_by_user(user_id)


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get a single order by ID"""
    order = OrderRepository.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, update: OrderUpdate):
    """Update order status or payment ID"""
    order = OrderRepository.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if update.status:
        order.status = update.status
    if update.paymentId:
        order.paymentId = update.paymentId
    
    return OrderRepository.save(order)


@router.delete("/{order_id}")
async def cancel_order(order_id: str):
    """Cancel/delete an order"""
    order = OrderRepository.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Mark as cancelled instead of deleting (soft delete)
    order.status = OrderStatus.CANCELLED
    OrderRepository.save(order)
    
    return {"message": "Order cancelled successfully"}


@router.post("/{order_id}/simulate-payment")
async def simulate_payment(order_id: str):
    """Simulate payment success/failure for testing"""
    order = OrderRepository.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Simulate 90% success rate
    success = random.random() > 0.1
    
    if success:
        order.status = OrderStatus.CONFIRMED
        order.paymentId = f"pay_{order.id[:8]}"
        message = "Payment successful! Order confirmed."
    else:
        order.status = OrderStatus.FAILED
        message = "Payment failed. Please try again."
    
    OrderRepository.save(order)
    return {"success": success, "message": message, "order": order}