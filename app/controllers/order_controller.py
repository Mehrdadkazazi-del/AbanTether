from fastapi import APIRouter, Depends, HTTPException, status

from app.models.Order import Order
from app.schemas.order_schema import OrderCreate, OrderResponse
from app.services.order_service import OrderService, get_order_service
from app.utils.oauth2 import oauth2_scheme

router = APIRouter(
    prefix="/orders",
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("/payOrder/",
             response_model=OrderResponse,
             status_code=status.HTTP_200_OK,
             tags=['order'],
             summary="issue new Order",
             response_description='issue and pay order and do settlement with external exchange')
def pay_order(order: OrderCreate,
              order_service: OrderService = Depends(get_order_service)):
    try:
        new_order = order_service.create_order(int(order.user_id),
                                               order.crypto_name,
                                               float(order.amount),
                                               float(order.price_per_unit))
        return modelToViewMapper(new_order)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


def modelToViewMapper(model: Order) -> OrderResponse:
    return OrderResponse(
        order_id=model.id,
        status=model.is_settled
    )
