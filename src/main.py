from fastapi import FastAPI
import uvicorn

from routers import main_router


app = FastAPI()

app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
