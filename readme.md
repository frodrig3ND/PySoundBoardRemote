# PySoundBoardRemote

Quick and dirty websocket service based on FastAPI and associated vue frontend.
Set up button grid so send hotkeys to host PC.

Set up to work with SounPad running on host PC.

SoundPad is set up to allow for Ctrl-Alt-Numpad keys.
Frontend sends the num to be used in the hotkey.

Works properly on Raspberry Pi with display and Android.
Might have issues on Safari due to dropped websocket behaviour on unfocusing from page.

To run the FastApi service on host PC.

```bash
uvicorn server.main:app --host 0.0.0.0 --reload
```

to run webserver

```java
npm run serve
```
