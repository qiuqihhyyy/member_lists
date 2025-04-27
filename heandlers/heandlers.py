from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from database.db import Co_builderDAO


router = APIRouter()

#функция для добавления кобилдеров в таблицу
@router.post('/')
async def post(data=Body()):
    print(data)
    await Co_builderDAO.add(full_name=data['full_name'],
                            AVB_email=data['AVB_email'],
                            gmail=data['gmail'],
                            post=data['post'])
    return JSONResponse({'full_name': data['full_name'],
                        'AVB_email': data['AVB_email'],
                        'gmail': data['gmail'],
                        'post': data['post']}, status_code=201)
