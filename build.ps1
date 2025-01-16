# Run: powershell -ExecutionPolicy Bypass -File .\build_installer.ps1

# 1) Build EXE with PyInstaller
pyinstaller --onefile --icon="icon\icon.ico" --distpath dist winword.spec

# 2) Build NSIS installer
& "C:\Program Files (x86)\NSIS\makensis" "installer.nsi"

# Move the NSIS installer to the dist folder
Move-Item -Path "EsafenetCheaterSetup.exe" -Destination "dist\EsafenetCheaterSetup.exe"