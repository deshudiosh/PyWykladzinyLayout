call "./venv/Scripts/activate"
pyinstaller --onefile -w PyWykladzinyLayout.spec --additional-hooks-dir=.
pause