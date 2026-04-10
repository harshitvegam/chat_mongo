from app import app
import uvicorn

def main():
    print("Hello from chat-mongo!")


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8081)
    