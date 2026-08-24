@echo off
setlocal

echo ============================================
echo   Gerando o executavel do StormStand...
echo ============================================
echo.

python -m pip install --upgrade pyinstaller >nul
if errorlevel 1 (
    echo Falha ao instalar o PyInstaller. Verifique se o Python esta instalado
    echo e se o comando "python" funciona no seu terminal.
    pause
    exit /b 1
)

pyinstaller --onefile --console --name StormStand --add-data "data;data" main.py

echo.
if exist dist\StormStand.exe (
    echo ============================================
    echo   Pronto! O executavel esta em:
    echo   dist\StormStand.exe
    echo.
    echo   Copie StormStand.exe para a pasta "saves"
    echo   ficar do lado dele (sera criada sozinha no
    echo   primeiro "Salvar e Sair"^) e crie um atalho
    echo   dele na Area de Trabalho.
    echo ============================================
) else (
    echo Algo deu errado. Veja a mensagem de erro acima.
)

pause
