rem Save current directory
rem 
SET BUILD_PREVIOUS_CD=%CD%
 
echo on
SET SMEX_PROJECT_PATH=%~dp0..

cd %SMEX_PROJECT_PATH%\installshield

mkdir %SMEX_PROJECT_PATH%\output\build_log\
mkdir %SMEX_PROJECT_PATH%\output\image\

echo Compile code 
call "%VS80COMNTOOLS%\..\..\VC\vcvarsall.bat" amd64
devenv %SMEX_PROJECT_PATH%\src\BuildAll.sln /rebuild "Release|x64"	> %SMEX_PROJECT_PATH%\output\build_log\build_x64.log 2>&1

rem call "%VS120COMNTOOLS%vsvars32.bat"
rem devenv %SMEX_PROJECT_PATH%\src\delegator\delegator.sln /rebuild "release|Any CPU" > %SMEX_PROJECT_PATH%\output\build_log\build_delegator_x64.log 2>&1


call Cscript %SMEX_PROJECT_PATH%\installshield\signkey.js %SMEX_PROJECT_PATH%\output\runtime\win32\release %SMEX_PROJECT_PATH%
call Cscript %SMEX_PROJECT_PATH%\installshield\signkey.js %SMEX_PROJECT_PATH%\output\runtime\x64\release %SMEX_PROJECT_PATH%
call Cscript %SMEX_PROJECT_PATH%\installshield\signkey.js %SMEX_PROJECT_PATH%\output\runtime\E15\release %SMEX_PROJECT_PATH%

call MakeDelegatorPackage.bat %SMEX_PROJECT_PATH% x64 Release

call MakeScannerPackage.bat %SMEX_PROJECT_PATH% x64 Release

echo Build installer
SET INNO_SETUP_TOOL=".\tool\Inno Setup\ISCC.exe"

call ReadTMBuild.bat %SMEX_PROJECT_PATH%

rem %INNO_SETUP_TOOL% .\MiscDelegator.iss
rem %INNO_SETUP_TOOL% .\RTDelegator.iss
rem %INNO_SETUP_TOOL% .\SPDelegator.iss
rem %INNO_SETUP_TOOL% .\SPListener.iss
%INNO_SETUP_TOOL% .\Scanner.iss
rem %INNO_SETUP_TOOL% .\OnDemandDelegator.iss

rem MOVE .\OnDemandDelegator.exe 			%SMEX_PROJECT_PATH%\output\image
rem MOVE .\MiscDelegator.exe 			%SMEX_PROJECT_PATH%\output\image
rem MOVE .\RTDelegator.exe 			%SMEX_PROJECT_PATH%\output\image
rem MOVE .\SPDelegator.exe 			%SMEX_PROJECT_PATH%\output\image
rem MOVE .\SPListener.exe 			%SMEX_PROJECT_PATH%\output\image
MOVE .\Scanner.exe 				%SMEX_PROJECT_PATH%\output\image

cd %BUILD_PREVIOUS_CD%
 