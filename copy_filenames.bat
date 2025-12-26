@echo off
setlocal EnableDelayedExpansion

REM バッチファイルのあるディレクトリに移動
cd /d "%~dp0"

REM 引数がある場合（フォルダをドラッグ＆ドロップされた場合）
if not "%~1"=="" (
    REM WindowsパスをWSLパスに変換
    for /f "usebackq delims=" %%A in (`wsl wslpath -u "%~1"`) do set "TARGET_DIR=%%A"
    echo 対象ディレクトリ: %~1
    echo WSLパス: !TARGET_DIR!
    echo.
    
    REM 変換したパスを引数に渡して実行
    wsl uv run main.py "!TARGET_DIR!"
) else (
    REM 引数がない場合はカレントディレクトリ（バッチファイルのある場所）を対象に実行
    echo 対象ディレクトリ: カレントディレクトリ
    echo.
    wsl uv run main.py
)

echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] ファイル名をクリップボードにコピーしました。
) else (
    echo [ERROR] エラーが発生しました。
)

echo.
echo 何かキーを押すと終了します...
pause >nul
