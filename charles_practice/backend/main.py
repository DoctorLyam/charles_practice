from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

app = FastAPI()

# 💡 Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить для безопасности
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

expected_rewrite = {
    "user": {
        "name": "student",
        "role": "admin",
        "settings": {
            "notifications": True,
            "theme": "light"
        }
    }
}

def deep_equal(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(deep_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(deep_equal(x, y) for x, y in zip(a, b))
    return a == b

@app.post("/api/user/data")
async def user_data(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Измени запрос"}, status_code=400)

    print(">>> [user_data] Тело запроса:", body)

    if deep_equal(body, expected_rewrite):
        return JSONResponse(content={"key": 42})

    if "user" in body:
        return JSONResponse(content={"error": "Измени запрос в соответствии с тех.заданием"})

    return JSONResponse(content={"error": "Измени запрос"})


@app.post("/api/calculate")
async def calculate(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Измени запрос"}, status_code=400)

    print(">>> [calculate] Тело запроса:", body)

    if body == {"payload": "patched"}:
        return JSONResponse(content={"key": 1008})
    return JSONResponse(content={"error": "Измени запрос в соответствии с тех.заданием"})


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=200,
        content={"error": "Измени запрос"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=200,
        content={"error": "Измени запрос"}
    )

if __name__ == "__main__":
    # Слушаем 0.0.0.0, чтобы принимать запросы из контейнеров
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
