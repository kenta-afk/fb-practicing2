from fastapi import APIRouter
from routers import TodoInputView

router = APIRouter()

router.include_router(TodoInputView.TodoInputView_router, prefix="/TodoInputView")


