from fastapi import FastAPI,Depends, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from config.database import get_db
from routes import auth_router, user_router, admin_router
import os
from dotenv import load_dotenv
import jwt
from starlette import status
load_dotenv()


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

@app.middleware("http")
async def intercept_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")
    path = request.url.path

    # Routes 
    open_routes = ['/','/auth/signout', '/auth/refresh', '/auth/signup', '/auth/signin', '/docs','/openapi.json','/redoc']
    admin_routes = ['/admin/add-admin', '/admin/users', '/admin/passages', '/admin/admins']
    user_route_patterns = [
        '/user/add-passage',
        '/user/get-passage/',
        '/user/update-passage',
        '/user/delete-passage/'
    ]

    # Check if it's an open route
    if path in open_routes:
        return await call_next(request)

    # If no token, return unauthorized
    if not token:
        return JSONResponse(
            {"detail": "Authentication required"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Decode and validate token
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]  # type: ignore
        )
        #set state so that the endpoint can use it
        request.state.id = payload.get('id')

        role = payload.get('role')
        print(role)
        # Check admin routes
        if path in admin_routes:
            if role == 'admin':
                return await call_next(request)
            else:
                return JSONResponse(
                    {"detail": "Admin access required"},
                    status_code=status.HTTP_403_FORBIDDEN
                )
        
        # Check user routes (including parameterized ones)
        is_user_route = any(path.startswith(pattern) for pattern in user_route_patterns)
        if is_user_route:
            if role == 'user':
                return await call_next(request)
            else:
                return JSONResponse(
                    {"detail": "User access required"},
                    status_code=status.HTTP_403_FORBIDDEN
                )
        
        # If route is not in any category, allow access for valid token holders
        return await call_next(request)

    except jwt.ExpiredSignatureError:
        return JSONResponse(
            {"detail": "Token expired"}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            {"detail": "Invalid token"}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            {"detail": "Authentication error"}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )


    


@app.get('/')
def get_home(db:Session = Depends(get_db)):
    return {'status':'server is running'}

