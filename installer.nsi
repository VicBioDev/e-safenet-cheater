Name "EsafenetCheater"
OutFile "EsafenetCheaterSetup.exe"
InstallDir "$LOCALAPPDATA\EsafenetCheater"
RequestExecutionLevel admin
Icon "icon/icon.ico"

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\winword.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "DisplayName" "EsafenetCheater"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCR "*\shell\����ͨ����" "" "����ͨ����"
  WriteRegStr HKCR "*\shell\����ͨ����\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\winword.exe"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCR "*\shell\����ͨ����"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater"
SectionEnd