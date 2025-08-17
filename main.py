from fastapi import FastAPI
import uvicorn
from api.db import setup_database
from api.routes import router as api_router
from api.services.get_bank_from_bintable import fetch_bin_codes


async def lifespan(app: FastAPI) -> None:
    await fetch_bin_codes()
    await setup_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000)
