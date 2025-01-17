
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
  WriteRegStr HKCR "*\shell\����ͨ����" "" "����ͨ����"
  WriteRegStr HKCR "*\shell\����ͨ����" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "*\shell\����ͨ����\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteRegStr HKCR "Directory\shell\����ͨ����" "" "����ͨ����"
  WriteRegStr HKCR "Directory\shell\����ͨ����" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "Directory\shell\����ͨ����\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteRegStr HKCR "Directory\Background\shell\����ͨ����" "" "����ͨ����"
  WriteRegStr HKCR "Directory\Background\shell\����ͨ����" "Icon" "$INSTDIR\winword.exe"
  WriteRegStr HKCR "Directory\Background\shell\����ͨ����\command" "" '"$INSTDIR\winword.exe" "%1"'
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove program files
    Delete "$INSTDIR\winword.exe"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKCR "*\shell\����ͨ����"
    DeleteRegKey HKCR "Directory\shell\����ͨ����"
    DeleteRegKey HKCR "Directory\Background\shell\����ͨ����"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater"
    
    ; Refresh shell
SectionEnd

Function .onInit
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\EsafenetCheater" "UninstallString"
    ${If} $R0 != ""
        MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
            "�����Ѿ���װ��$\n$\n��� 'ȷ��' ɾ���Ѱ�װ�汾������ 'ȡ��' ��ֹ��װ��" \
            IDOK uninst
        Abort
        
    uninst:
        ExecWait '$R0 _?=$INSTDIR'
    ${EndIf}
FunctionEnd