call "./venv/Scripts/activate"
pyinstaller --onefile --noconsole -w PyWykladzinyLayout.spec

rmdir build /s /q
rmdir dist /s /q
pause