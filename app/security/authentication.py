from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.services.user_service import UserService, get_user_service
from app.utils import oauth2
from app.utils.hash import Hash

router = APIRouter(tags=['authentication'])


@router.post("/token",
             status_code=status.HTTP_200_OK,
             summary="generate access token")
def get_token(request: OAuth2PasswordRequestForm = Depends(),
              user_service: UserService = Depends(get_user_service)):
    user = user_service.load_user_with_first_name(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credential')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')

    access_token = oauth2.create_access_token(data={'sub': request.username})

    return {
        'access_token': access_token,
        'type_token': 'bearer'
    }
