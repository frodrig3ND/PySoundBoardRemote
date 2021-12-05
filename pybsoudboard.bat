ECHO "STARTING SERVER PYSOUNDBOARD REMOTE"
cd D:\DevCode\PySoundBoardRemote
call D:\DevCode\PySoundBoardRemote\env\Scripts\activate.bat
uvicorn server.main:app --host 0.0.0.0 --reload
pause