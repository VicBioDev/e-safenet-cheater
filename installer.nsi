
!include "MUI2.nsh"
!include "WinMessages.nsh"
!include LogicLib.nsh

; Basic Settings
Name "EsafenetCheater"
OutFile "EsafenetCheaterSetup.exe"
InstallDir "$LOCALAPPDATA\EsafenetCheater"
RequestExecutionLevel admin
Icon "icon/icon.ico"

; Modern UI Settings
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"


Section "Install"
  
  ; Check for existing installation
  ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "UninstallString"
  StrCmp $0 "" 0 +3
    ; No existing installation found
    Goto +2
  ; Uninstall the existing version silently
  ExecWait '"$0" /S'

  SetOutPath "$INSTDIR"
  File "dist\winword.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "DisplayName" "EsafenetCheater"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCR "*\shell\亿赛通解密" "" "亿赛通解密"
  WriteRegStr HKCR "*\shell\亿赛通解密" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "*\shell\亿赛通解密\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteRegStr HKCR "Directory\shell\亿赛通解密" "" "亿赛通解密"
  WriteRegStr HKCR "Directory\shell\亿赛通解密" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "Directory\shell\亿赛通解密\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteRegStr HKCR "Directory\Background\shell\亿赛通解密" "" "亿赛通解密"
  WriteRegStr HKCR "Directory\Background\shell\亿赛通解密" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "Directory\Background\shell\亿赛通解密\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove program files
    Delete "$INSTDIR\winword.exe"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKCR "*\shell\亿赛通解密"
    DeleteRegKey HKCR "Directory\shell\亿赛通解密"
    DeleteRegKey HKCR "Directory\Background\shell\亿赛通解密"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater"
    
    ; Refresh shell
SectionEnd

Function .onInit
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "UninstallString"
    ${If} $R0 != ""
        MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
            "程序已经安装。$\n$\n点击 '确定' 删除已安装版本，或点击 '取消' 终止安装。" \
            IDOK uninst
        Abort
        
    uninst:
        ExecWait '$R0 _?=$INSTDIR'
    ${EndIf}
FunctionEnd