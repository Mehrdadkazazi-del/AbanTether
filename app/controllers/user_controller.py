from fastapi import APIRouter, Depends, HTTPException, status

from app.models.User import User
from app.schemas.user_schema import UserResponse, UserCreate
from app.services.user_service import UserService, get_user_service
from app.utils.oauth2 import oauth2_scheme

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("/add/",
             response_model=UserResponse,
             status_code=status.HTTP_200_OK,
             tags=['user'],
             summary="Add new user",
             response_description='create new User with account and then return user viewModel to client')
def add_user(user: UserCreate,
             user_service: UserService = Depends(get_user_service)):
    try:
        created_user = user_service.create_user_service(first_name=user.firstName,
                                                        last_name=user.lastName,
                                                        national_code=user.nationalCode,
                                                        password=user.password)
        return modelToViewMapper(created_user)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/loadUserByFirstName",
            response_model=UserResponse,
            status_code=status.HTTP_200_OK,
            tags=['user'],
            summary="get user",
            response_description='return user')
def load_user_by_first_name(first_name: str, user_service: UserService = Depends(get_user_service)):
    try:
        loaded_user = user_service.load_user_with_first_name(first_name)
        return modelToViewMapper(loaded_user)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


def modelToViewMapper(model: User) -> UserResponse:
    return UserResponse(
        id=model.id,
        firstName=model.first_name,
        lastName=model.last_name,
        nationalCode=model.national_code
    )
