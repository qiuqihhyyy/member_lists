import os

import dotenv
import requests
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
from database.db import Co_builderDAO


router = APIRouter()
dotenv.load_dotenv()
MATTERMOST_URL = os.getenv("MATTERMOST_URL")
HEADERS = os.getenv("HEADERS")
BOT_USER_ID = os.getenv("BOT_USER_ID")

#функция для добавления кобилдеров в таблицу
@router.post('/')
async def post(data=Body()):
    task = BackgroundTask(Co_builderDAO.add,
                          full_name=data['full_name'],
                          AVB_email=data['AVB_email'],
                          gmail=data['gmail'],
                          post=data['post'])
    return JSONResponse({"status": "ok"}, status_code=200, background=task)


def get_dm_channel(user_id):
    url = f"{MATTERMOST_URL}/api/v4/channels/direct"
    response = requests.post(url, headers=HEADERS, json=[BOT_USER_ID, user_id])
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(
            f"⚠️ Не удалось создать DM канал: {response.status_code} - {response.text}"
        )
        return None


def send_file(channel_id):
    post_data = {"channel_id": channel_id, "filename": 'member-list', "file_size": os.path.getsize('member-list.xlsx')}
    post_url = f"{MATTERMOST_URL}/api/v4/uploads"
    response = requests.post(post_url, headers=HEADERS, json=post_data)
    if response.status_code != 201:
        print(
            f"⚠️ Не удалось отправить файл в ЛС: {response.status_code} - {response.text}"
        )