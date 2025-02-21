# EsafenetCheater
亿赛通加密破解

EsafenetCheater is a Python-based tool designed to detect and decrypt files that have been encrypted with a custom signature ("Esafenet"). The project provides both a graphical user interface (GUI) using Tkinter and a command-line (CLI) mode. The software is packaged as a Windows installer built using NSIS.

## Features

- **Detection:** Scans files or directories and uses PowerShell to detect if a file is encrypted.
- **Decryption:** Decrypts files by transferring contents through temporary files, preserving metadata, and renaming files using PowerShell.
- **Interface:**  
  - GUI mode via [`esafenet_cheater_ui.py`](./esafenet_cheater_ui.py)
  - CLI mode for batch processing.
- **Installer:** Windows installer built using NSIS.

## Project Structure

- [`.gitignore`](./.gitignore) – Git ignore rules.
- [`esafenet_cheater_ui.py`](./esafenet_cheater_ui.py) – Main UI application.
- [`esafenet_cheater_cli.py`](./esafenet_cheater_cli.py) – CLI decryption tool.
- [`installer.nsi`](./installer.nsi) – NSIS installer script.
- [`requirements.txt`](./requirements.txt) – Required Python packages.
- Additional directories like `dist` and `build` for build outputs and scripts.

## Installation

1. **Prerequisites:**  
   - Python 3.x  
   - PowerShell (for decryption and build commands)  
   - NSIS (to build the Windows installer)

2. **Install Dependencies:**  
   Run the following command in your terminal:
   ```sh
   pip install -r requirements.txt
   ```

## Build Instructions

1. **Build EXE with PyInstaller**
   ```sh
   pyinstaller --distpath dist esafenet_cheater_ui.spec
   ```

2. **Build NSIS installer**
   ```powershell
   & "C:\Program Files (x86)\NSIS\makensis" "installer.nsi"
   ```

3. **Move the NSIS installer to the dist folder**
   ```powershell
   Move-Item -Path "EsafenetCheaterSetup.exe" -Destination "dist\EsafenetCheaterSetup.exe" -Force
   ```

## Disclaimer

This software is provided "as-is", without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use or inability to use the software.

## License

MIT License

Copyright (c) [2025] [VicBioDev]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.