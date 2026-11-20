@echo off
rem Runs RustCord with its data beside this file. Security software can deny an unsigned build any
rem write inside the user profile (ERROR_ACCESS_DENIED), and then the cache, saved logins and the
rem diagnostic log all stay read-only. Put this file next to rustcord.exe and start RustCord with it.
setlocal
set "ROOT=%~dp0"
set "EXE="
if exist "%ROOT%rustcord.exe" set "EXE=%ROOT%rustcord.exe"
if not defined EXE if exist "%ROOT%serein.exe" set "EXE=%ROOT%serein.exe"
if not defined EXE (
	echo Put this file next to rustcord.exe.
	exit /b 1
)
if not exist "%ROOT%data" mkdir "%ROOT%data"
set "RUSTCORD_DATA_DIR=%ROOT%data"
set "SEREIN_DATA_DIR=%ROOT%data"
start "" "%EXE%" %*
endlocal
