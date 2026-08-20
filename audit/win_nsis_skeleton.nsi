; openOODA Windows installer skeleton (NSIS 3.12)
; DRAFT -- tooling lane owns the final script.
; Source: openOODA/audit/win_installer_options.oot section 6.
;
; Usage:
;   1. Copy this file to install/windows/openooda.nsi.
;   2. Fill in BIN_DIR, STD_DIR, FIX_DIR with the staged build paths.
;   3. Drop LICENSE.rtf next to the .nsi script (RTF required by MUI_PAGE_LICENSE).
;   4. Set the signtool finalize command at the bottom of this file.
;   5. Run: makensis openooda.nsi
; Build hosts: Windows (native) or Linux (makensis under Wine).
;
; Design choices (documented in the script so the tooling lane can change them):
;   - HKCU\Environment only, no UAC, no system PATH edit.
;   - $LOCALAPPDATA, not $PROGRAMFILES, so no admin needed.
;   - No compiler invocation; binaries are staged by the host build.
;   - signtool finalize for both installer and uninstaller.
;   - Per-user Add/Remove Programs entry under HKCU\...\Uninstall.

Unicode true
SetCompressor /SOLID lzma

; --- Product metadata (placeholders; tooling lane may override) ---
!define PRODUCT_NAME      "openOODA"
!define PRODUCT_VERSION   "0.205.0-beta"
!define PRODUCT_PUBLISHER "openOODA"
!define PRODUCT_WEB_SITE  "https://openooda.org"
!define LICENSE_RTF       "LICENSE.rtf"
!define UNINST_KEY        "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

; --- Build inputs (relative to this .nsi file) ---
!define BIN_DIR  "..\..\stage\bin"
!define STD_DIR  "..\..\stage\std"
!define FIX_DIR  "..\..\stage\fixtures"

; $BOOTSTRAP_PIN holds the pin the first `ooda update` should fetch. Set from
; /OODA_PIN=... on the install command line in .onInit below.
Var BOOTSTRAP_PIN

; --- Standard NSIS metadata ---
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "openooda-setup-${PRODUCT_VERSION}.exe"
InstallDir "$LOCALAPPDATA\${PRODUCT_NAME}"
RequestExecutionLevel user
BrandingText "${PRODUCT_NAME} ${PRODUCT_VERSION}"
VIProductVersion "${PRODUCT_VERSION}.0"
VIAddVersionKey "ProductName"    "${PRODUCT_NAME}"
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION}"
VIAddVersionKey "CompanyName"    "${PRODUCT_PUBLISHER}"
VIAddVersionKey "FileVersion"    "${PRODUCT_VERSION}"
VIAddVersionKey "LegalCopyright" ""

; --- Includes ---
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"
!include "StrFunc.nsh"

; --- MUI2 page settings ---
!define MUI_ABORTWARNING
!define MUI_ICON  "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_WELCOMEPAGE_TITLE "${PRODUCT_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT  "This wizard installs ${PRODUCT_NAME} ${PRODUCT_VERSION}.$\r$\n$\r$\nClick Next to continue."
!define MUI_FINISHPAGE_TITLE  "${PRODUCT_NAME} installed"
!define MUI_FINISHPAGE_TEXT   "${PRODUCT_NAME} has been installed. Open a new terminal to use ooda and oodac."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${LICENSE_RTF}"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Reserve the license RTF so the wizard paints it fast on slow disks.
ReserveFile "${LICENSE_RTF}" RSP_LICENSE

; --- Section descriptions for the MUI2 components page ---
LangString DESC_SEC_BIN  ${LANG_ENGLISH} "Install ooda.exe, oodac.exe, and the chs_rt runtime DLLs to $INSTDIR\bin."
LangString DESC_SEC_STD  ${LANG_ENGLISH} "Install the openOODA standard library tree to $INSTDIR\share\ooda\std."
LangString DESC_SEC_FIX  ${LANG_ENGLISH} "Install the openOODA hello fixture for smoke-testing the toolchain."
LangString DESC_SEC_PATH ${LANG_ENGLISH} "Prepend $INSTDIR\bin to the current user PATH. No admin, no logoff."
LangString DESC_SEC_ENV  ${LANG_ENGLISH} "Set OODA_INSTALL and OODA_FS_WRITEDIR in the current user environment."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_BIN}  $(DESC_SEC_BIN)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_STD}  $(DESC_SEC_STD)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_FIX}  $(DESC_SEC_FIX)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_PATH} $(DESC_SEC_PATH)
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_ENV}  $(DESC_SEC_ENV)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; --- Install: binaries (required, cannot be unchecked) ---
Section "openOODA binaries" SEC_BIN
  SectionIn RO
  SetOutPath "$INSTDIR\bin"
  ; Tooling lane replaces this with explicit File statements for ooda.exe,
  ; oodac.exe, and the chs_rt runtime DLLs. The /r keeps the staged tree shape.
  File /r "${BIN_DIR}\*"
SectionEnd

; --- Install: std library (required) ---
Section "openOODA std library" SEC_STD
  SectionIn RO
  SetOutPath "$INSTDIR\share\ooda\std"
  ; Tooling lane replaces this with explicit File statements for the .oo files.
  File /r "${STD_DIR}\*"
SectionEnd

; --- Install: fixtures (one file: hello.oo) ---
Section "openOODA fixtures" SEC_FIX
  SectionIn RO
  SetOutPath "$INSTDIR\share\ooda\fixtures"
  ; Only one fixture ships with the install: hello.oo. The full fixtures tree
  ; is built and run by CI; the install only carries the smoke-test fixture.
  File "${FIX_DIR}\hello.oo"
SectionEnd

; --- Install: prepend $INSTDIR\bin to HKCU\Environment\Path ---
Section "Add to PATH" SEC_PATH
  SectionIn
  ; Read current user PATH, prepend $INSTDIR\bin, write back. SetShellVarContext
  ; current is the key: it points at HKCU, not HKLM, so no UAC and no system edit.
  ; Documented choice: user path only. The "(or HKLM if elevated)" option from
  ; the recommendation is intentionally NOT taken; this is the no-admin pattern.
  SetShellVarContext current
  ReadRegStr $0 HKCU "Environment" "Path"
  ${If} $0 == ""
    StrCpy $0 "$INSTDIR\bin"
  ${Else}
    StrCpy $0 "$INSTDIR\bin;$0"
  ${EndIf}
  WriteRegExpandStr HKCU "Environment" "Path" "$0"
  ; Notify Explorer so new shells pick up the PATH without a logoff.
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0 "STR:Environment" /TIMEOUT=5000
SectionEnd

; --- Install: OODA env vars in HKCU\Environment ---
Section "Set OODA env" SEC_ENV
  SectionIn
  ; OODA_INSTALL is the install marker; OODA_FS_WRITEDIR is the work dir. Both
  ; match the install policy in audit/win_compiler_plan.oot (Phase 4).
  SetShellVarContext current
  WriteRegExpandStr HKCU "Environment" "OODA_INSTALL"     "$INSTDIR"
  WriteRegExpandStr HKCU "Environment" "OODA_FS_WRITEDIR" "$INSTDIR\work"
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0 "STR:Environment" /TIMEOUT=5000
SectionEnd

; --- Post-install: write the per-user Add/Remove Programs entry (hidden) ---
Section -Post
  ; HKCU\...\Uninstall is the per-user variant; Windows shows these in
  ; Settings > Apps alongside the HKLM entries. This is the no-admin choice.
  WriteRegStr   HKCU "${UNINST_KEY}" "DisplayName"     "${PRODUCT_NAME}"
  WriteRegStr   HKCU "${UNINST_KEY}" "DisplayVersion"  "${PRODUCT_VERSION}"
  WriteRegStr   HKCU "${UNINST_KEY}" "Publisher"       "${PRODUCT_PUBLISHER}"
  WriteRegStr   HKCU "${UNINST_KEY}" "URLInfoAbout"    "${PRODUCT_WEB_SITE}"
  WriteRegStr   HKCU "${UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr   HKCU "${UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr   HKCU "${UNINST_KEY}" "DisplayIcon"     "$INSTDIR\bin\ooda.exe,0"
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; --- Uninstaller: reverse each install step ---
Section "Uninstall"
  ; Remove files in reverse install order. RMDir /r recurses; safe because
  ; $INSTDIR is dedicated to openOODA.
  RMDir /r "$INSTDIR\bin"
  RMDir /r "$INSTDIR\share\ooda\std"
  RMDir /r "$INSTDIR\share\ooda\fixtures"
  RMDir /r "$INSTDIR\share\ooda"
  RMDir /r "$INSTDIR\work"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  ; Strip the prepended $INSTDIR\bin from the user PATH. StrRep replaces every
  ; occurrence (there should be only one, but be safe).
  SetShellVarContext current
  ReadRegStr $0 HKCU "Environment" "Path"
  ${StrRep} $1 $0 "$INSTDIR\bin;" ""
  ${StrRep} $1 $1 "$INSTDIR\bin"   ""
  WriteRegExpandStr HKCU "Environment" "Path" $1
  DeleteRegValue HKCU "Environment" "OODA_INSTALL"
  DeleteRegValue HKCU "Environment" "OODA_FS_WRITEDIR"
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0 "STR:Environment" /TIMEOUT=5000

  ; Remove the per-user Add/Remove Programs entry.
  DeleteRegKey HKCU "${UNINST_KEY}"
SectionEnd

; --- onInit: read /OODA_PIN=... from the install command line ---
Function .onInit
  ; The install command line passes /OODA_PIN=v0.205.0-beta. We read it into
  ; $BOOTSTRAP_PIN so the first `ooda update` after install knows which pin to
  ; fetch. (Real usage is a small wrapper script; this is the documented hook.)
  ${GetParameters} $R0
  ClearErrors
  ${GetOptions} $R0 "/OODA_PIN=" $R1
  ${IfNot} ${Errors}
    StrCpy $BOOTSTRAP_PIN $R1
  ${Else}
    StrCpy $BOOTSTRAP_PIN "${PRODUCT_VERSION}"
  ${EndIf}
FunctionEnd

; --- onVerifyInstDir: refuse system paths ---
Function .onVerifyInstDir
  ; Refuse $WINDIR and any path under %ProgramFiles%\WindowsApps. The installer
  ; would otherwise drop files into a read-only system location.
  ${If} $INSTDIR == "$WINDIR"
  ${OrIf} $INSTDIR == "$WINDIR\"
  ${OrIf} ${FileExists} "$INSTDIR\WindowsApps"
    Abort "Refusing to install into a system directory."
  ${EndIf}
FunctionEnd

; --- Code signing finalize hooks ---
; NSIS runs these after the installer/uninstaller is built. %1 is the produced
; .exe. Tooling lane fills in the actual signtool command. Use /fd SHA256 and a
; timestamp server; see audit/win_installer_options.oot section 7.
!define SIGNTOOL_CMD 'signtool.exe sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /f sign.pfx /p %PFX_PASS% "%1"'
!finalize       '${SIGNTOOL_CMD}'
!uninstfinalize '${SIGNTOOL_CMD}'
