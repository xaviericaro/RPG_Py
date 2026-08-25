@echo off
setlocal

echo ============================================
echo   Gerando o executavel do StormStand...
echo ============================================
echo.

echo Verificando Python...
py --version

if errorlevel 1 (
    echo.
    echo Python nao foi encontrado.
    pause
    exit /b 1
)

echo.
echo Instalando/atualizando PyInstaller...
py -m pip install --upgrade pyinstaller

if errorlevel 1 (
    echo.
    echo Falha ao instalar o PyInstaller.
    echo Veja a mensagem de erro acima.
    pause
    exit /b 1
)

echo.
echo Gerando executavel...
py -m PyInstaller --onefile --console --name StormStand --add-data "data;data" main.py

if errorlevel 1 (
    echo.
    echo Erro ao gerar o executavel.
    echo Veja a mensagem acima.
    pause
    exit /b 1
)

echo.
if exist "dist\StormStand.exe" (
    echo ============================================
    echo   PRONTO! EXECUTAVEL GERADO COM SUCESSO!
    echo.
    echo   Local:
    echo   dist\StormStand.exe
    echo ============================================
) else (
    echo.
    echo O PyInstaller terminou, mas o arquivo nao foi encontrado.
)

echo.
pause