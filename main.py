from fastapi import FastAPI
from route.routes import router
from core.database import get_db, engine
from core.connect_rabbitmq import connect_rabbitmq
from features.user.model import Base
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from features.user.route import router as user_route
from route.routes import router
import pika
app = FastAPI()
app.include_router(router)
app.include_router(user_route)



origins = [
    "http://183.87.168.3:3000",
    "http://10.155.219.131:3000",
    "http://localhost:3000", 
    "http://106.193.132.91:3000", 
    "http://103.172.86.182:3000",
    "http://172.23.0.2:3000",
    "http://192.168.1.106:3000",
    "http://192.168.1.106:3000",
    "http://host.docker.internal:3000" #for dockerised frontend next js application 
    #Use your frontend's actual IP/port here
]

# Created the socket server here and passing these in the socket events
# sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
# socket_app = socketio.ASGIApp(sio, app)
# register_socket_events(sio)     

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Required for CORS, you can set it to ["*"] to allow all origins, but it's better to specify your frontend's URL
    allow_credentials=True,        #Required for cookies, so keep it now, If you don't need cookies, you can set it to False, but I am using it for authentication, so please keep it True
    allow_methods=["*"],        # Required for CORS, you can set it to ["*"] to allow all methods, but it's better to specify the methods you need
    allow_headers=["*"],    # Required for CORS, you can set it to ["*"] to allow all headers, but it's better to specify the headers you need
)

# RabbitMQ connection
connection, channel = connect_rabbitmq()

@app.get("/")
def health_check():
    return JSONResponse({"data":"heath good"})

Base.metadata.create_all(bind=engine)