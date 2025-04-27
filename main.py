import asyncio
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Body
import pandas as pd
from starlette.responses import JSONResponse

from database.db import Co_builderDAO
from heandlers.heandlers import router


async def repeat_task():
    # взятие значений с базы данных
    data = await Co_builderDAO.find_all()
    # изменение их с помощью pandas
    df = pd.DataFrame.from_records([row.to_dict() for row in data])
    # добавление данных в таблицу member-list
    df.to_excel('member-list.xlsx', index=False)
    # отправление файла
    # очистка файла
    with open('member-list.xlsx', 'w') as file: pass
    # очистка базы данных
    await Co_builderDAO.delete()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ежедневное выполнение repeat_task в 00:00
    scheduler = AsyncIOScheduler()
    scheduler.add_job(repeat_task, 'cron', hour=0, minute=0)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)