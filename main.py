from fastapi import FastAPI

app = FastAPI(
    title="Intelligent PsychoAnalysis API",
    description="Бекенд для системи аналізу психологічних текстів"
)

@app.get("/")
def read_root():
    return {"message": "Сервер успішно запущено! Система готова до роботи."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)