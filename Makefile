all: dist/labrador.exe

dist/labrador.exe: src/labrador.py src/drop_tracker.py src/operations.py
	pyinstaller src/labrador.py --onefile
