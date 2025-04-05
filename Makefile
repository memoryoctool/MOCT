build:
    pyinstaller --noconsole --icon assets/moct.ico --name moct --onefile --uac-admin main.py

requirements:
    pip freeze > requirements.txt
