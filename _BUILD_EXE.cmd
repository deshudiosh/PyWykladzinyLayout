call "./venv/Scripts/activate"
pyinstaller --onefile -w PyWykladzinyLayout.spec --additional-hooks-dir=. --collect-all tkinterdnd2

rmdir build /s /q
rmdir dist /s /q
pause