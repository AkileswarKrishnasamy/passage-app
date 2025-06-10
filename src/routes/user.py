from fastapi import APIRouter, Depends, Path, Request
from config import get_db
from sqlalchemy.orm import Session
from service import PassageService
from schemas import PassageCreate,PassageUpdate

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_passage_service(db: Session = Depends(get_db)) -> PassageService:
    
    return PassageService(db)
   
@router.get('/get-passage/{passage_id}')
def get_passage(request: Request, passage_id: int = Path(gt=0), passage_service: PassageService = Depends(get_passage_service)):
    
    return passage_service.get_passage_by_id(request.state.id, passage_id)
    
    
@router.post('/add-passage')
def add_passage(request:Request, passage: PassageCreate, passage_service: PassageService = Depends(get_passage_service)):

    return passage_service.add_new_passage(request.state.id,passage)

@router.put('/update-passage')
def update_passage(passage: PassageUpdate, passage_service: PassageService = Depends(get_passage_service)):
    
    return passage_service.update_passage(passage)


@router.delete('/delete-passage/{passage_id}')
def delete_passage(request:Request, passage_id: int = Path(gt=0), passage_service: PassageService = Depends(get_passage_service)):

    return passage_service.delete_passage(request.state.id, passage_id)
    