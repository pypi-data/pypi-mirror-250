import uvicorn

from pythonicspring import SpringApplication

app = SpringApplication()

if __name__ == '__main__':
    uvicorn.run("TestApp:app", host="0.0.0.0", port=8080, reload=True)
