from fastapi import APIRouter, Depends
from config import get_db
from service import AdminService
from sqlalchemy.orm import Session
from schemas import UserCreate

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_admin_service(db: Session = Depends(get_db)):
    return AdminService(db)

@router.post('/add-admin')
def add_admin(admin: UserCreate, admin_service: AdminService = Depends(get_admin_service)):

    return admin_service.add_new_admin(admin)

@router.get('/users')
def get_all_users(admin_service: AdminService = Depends(get_admin_service)):

    return admin_service.get_all_users()

@router.get('/admins')
def get_all_admins(admin_service: AdminService = Depends(get_admin_service)):

    return admin_service.get_all_admins()

@router.get('/passages')
def get_all_passages(admin_service: AdminService = Depends(get_admin_service)):
    
    return admin_service.get_all_passages()

