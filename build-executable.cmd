rem This script creates a single-file executable for the Python Qt application.
pipenv run pyinstaller --noconsole --distpath . --onefile -n "Aztec Arctic Circle" --icon icon.ico main_qt.py

