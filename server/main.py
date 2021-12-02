from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pynput.keyboard import Key, Controller, KeyCode
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Integer, Column, String

from pydantic import BaseModel

from fastapi_crudrouter import SQLAlchemyCRUDRouter


app = FastAPI()

origins = [
    "http://localhost",
    "http://192.168.1.181",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.1.181:8081",
    "http://192.168.1.181:8080",
    "http://192.168.1.181:8000",
    "*"
]

origins_all = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_all,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

keyboard = Controller()

NUMPAD_VK = {}
for n in range(0, 10):
    NUMPAD_VK[str(n)] = 96+n

print(NUMPAD_VK)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>PySoundPadRemote Test</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <button type="button" value="1" onclick="sendBtn(this); return false;">
         Audio 1</button>

        <button type="button" value="2" onclick="sendBtn(this); return false;">
         Audio 2</button>

        <button type="button" value="3" onclick="sendBtn(this); return false;">
         Audio 3</button>


        <ul id='messages'>
        </ul>



        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            };
            function sendBtn(btn) {
                var btn_val=btn.value;
                ws.send(btn_val);
            };
        </script>
    </body>
</html>
"""

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class Buttons(Base):
    __tablename__ = "buttonlist"

    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    num = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)


class ButtonBase(BaseModel):
    order: int
    name: str
    num: int


class Button(ButtonBase):
    id: int

    class Config:
        orm_mode = True


class ButtonCreate(ButtonBase):
    pass


button_router = SQLAlchemyCRUDRouter(
    schema=Button,
    create_schema=ButtonCreate,
    db_model=Buttons,
    db=get_db,
    prefix='buttons'
)

app.include_router(button_router)


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        with keyboard.pressed(Key.ctrl):
            with keyboard.pressed(Key.alt):
                for n in data:
                    keyboard.press(KeyCode.from_vk(NUMPAD_VK[n]))
                    keyboard.release(KeyCode.from_vk(NUMPAD_VK[n]))

        await websocket.send_text(f"Message text was: {data}")
