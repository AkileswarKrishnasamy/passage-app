from fastapi import APIRouter, Depends, Response, Request
from service import UserService, AuthService
from config import get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)



@router.post('/signup')
def sign_up(user: UserCreate, user_service: UserService = Depends(get_user_service)) -> None:
    return user_service.create_new_user(user=user)

@router.post('/signin')
def sign_in(user: UserLogin,request: Request,response: Response, auth_service: AuthService = Depends(get_auth_service)):

    token = request.cookies.get("access_token")
    if not token:
        [access_token, refresh_token] = auth_service.sign_in_user(user)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,         # JS can't access this cookie
            secure=True,           # Send over HTTPS only (enable in prod)
            samesite="lax",        # Prevents CSRF in most cases
            max_age=3600           # 1 hour expiry
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,        
            secure=True,
            samesite="lax",
            max_age= 30 * 24 * 60 * 60        
        )

@router.get('/refresh')
def refresh_token(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    
    refresh_token = request.cookies.get('refresh_token')
    print(request.cookies)
    [access_token, refresh_token] = auth_service.refresh_token(refresh_token) # type: ignore

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,         # JS can't access this cookie
            secure=True,           # Send over HTTPS only (enable in prod)
            samesite="lax",        # Prevents CSRF in most cases
            max_age=3600           # 1 hour expiry
        )
    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,        
            secure=True,
            samesite="lax",
            max_age= 30 * 24 * 60 * 60        
        )

@router.get('/signout')
def sign_out(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {
        'status':'success'
    }