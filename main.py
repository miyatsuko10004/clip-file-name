import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
import pyperclip
from dotenv import load_dotenv

def is_wsl():
    try:
        with open('/proc/version', 'r') as f:
            if "microsoft" in f.read().lower():
                return True
    except FileNotFoundError:
        pass
    return False

def convert_windows_path_to_wsl(path_str):
    """
    Windows形式のパスをWSLパスに変換する。
    例: "C:\\Users\\developer" -> "/mnt/c/Users/developer"
    """
    if not is_wsl():
        return path_str
        
    # すでにWSLパスっぽい、または相対パスの場合はそのまま返す
    if path_str.startswith('/') or path_str.startswith('.'):
        return path_str

    try:
        # wslpath コマンドを使用して変換
        result = subprocess.run(['wslpath', '-u', path_str], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # 変換に失敗した場合は元の文字列を返す（あるいはエラーにする）
        return path_str

def copy_to_clipboard(text):
    """
    テキストをクリップボードにコピーする。
    WSL環境の場合は clip.exe の利用を試みる。
    """
    try:
        pyperclip.copy(text)
        print("pyperclipを使用してコピーした。")
        return
    except pyperclip.PyperclipException:
        pass

    # WSL環境かつclip.exeが利用可能な場合のフォールバック
    if is_wsl() and shutil.which("clip.exe"):
        try:
            process = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE, close_fds=True)
            process.communicate(input=text.encode('utf-16')) 
            return
        except Exception as e:
            print(f"clip.exeでのコピーに失敗した: {e}")
            
            # 再試行: シンプルな subprocess run (Shift-JIS/CP932)
            try:
                subprocess.run(['clip.exe'], input=text.encode('cp932', errors='ignore'), check=True)
                print("clip.exeを使用してコピーした(cp932)。")
                return
            except Exception as e2:
                 print(f"clip.exeでの再試行にも失敗した: {e2}")

    print("クリップボードへのコピーに失敗した。xclip や xsel がインストールされているか確認して。")

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="指定したディレクトリ内のファイル名をクリップボードにコピーする")
    parser.add_argument("directory", nargs="?", default=None, help="対象のディレクトリ")
    parser.add_argument("--include-hidden", action="store_true", help="隠しファイルを含める")
    
    args = parser.parse_args()
    
    target_path_str = args.directory
    
    # 引数が指定されていない場合、環境変数をチェック
    if target_path_str is None:
        env_target = os.getenv("TARGET_DIRECTORY")
        if env_target:
            # 環境変数に値があればそれを使用（Windowsパスの可能性も考慮して変換）
            target_path_str = convert_windows_path_to_wsl(env_target)
        else:
            # 環境変数もなければカレントディレクトリ
            target_path_str = "."

    target_dir = Path(target_path_str)
    
    if not target_dir.exists():
        print(f"エラー: ディレクトリ '{target_dir}' ('{target_path_str}') が見つからない。")
        sys.exit(1)
        
    if not target_dir.is_dir():
        print(f"エラー: '{target_dir}' はディレクトリではない。")
        sys.exit(1)
        
    files = []
    for item in target_dir.iterdir():
        if item.is_file():
            if not args.include_hidden and item.name.startswith('.'):
                continue
            files.append(item.name)
            
    if not files:
        print(f"ディレクトリ '{target_dir}' にファイルが見つからない。")
        return

    # ソートして結合
    files.sort()
    text_to_copy = "\n".join(files)
    
    copy_to_clipboard(text_to_copy)
    print(f"{len(files)} 個のファイル名をクリップボードにコピーした。")

if __name__ == "__main__":
    main()