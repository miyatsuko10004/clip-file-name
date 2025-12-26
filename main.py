import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
import pyperclip

def is_wsl():
    try:
        with open('/proc/version', 'r') as f:
            if "microsoft" in f.read().lower():
                return True
    except FileNotFoundError:
        pass
    return False

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
            process.communicate(input=text.encode('utf-16')) # clip.exeはUTF-16を期待することがあるが、通常はcp932等が無難だが単純なパイプならutf-8でもいける場合がある。
            # しかしPythonのsubprocessからclip.exeへはエンコーディング注意。
            # 一般的には text.encode('cp932') だが、日本語ファイル名を含むなら注意が必要。
            # ここではシンプルに text.encode('utf-8') ではなく、システムのロケールに依存するが...
            # 実は clip.exe は標準入力からのデータをANSI(CP932)で受け取ることが多い。
            
            # 再試行: シンプルな subprocess run
            subprocess.run(['clip.exe'], input=text.encode('cp932', errors='ignore'), check=True)
            print("clip.exeを使用してコピーした。")
            return
        except Exception as e:
            print(f"clip.exeでのコピーに失敗した: {e}")

    print("クリップボードへのコピーに失敗した。xclip や xsel がインストールされているか確認して。")

def main():
    parser = argparse.ArgumentParser(description="指定したディレクトリ内のファイル名をクリップボードにコピーする")
    parser.add_argument("directory", nargs="?", default=".", help="対象のディレクトリ (デフォルト: カレントディレクトリ)")
    parser.add_argument("--include-hidden", action="store_true", help="隠しファイルを含める")
    
    args = parser.parse_args()
    
    target_dir = Path(args.directory)
    
    if not target_dir.exists():
        print(f"エラー: ディレクトリ '{target_dir}' が見つからない。")
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
        print("ファイルが見つからない。")
        return

    # ソートして結合
    files.sort()
    text_to_copy = "\n".join(files)
    
    copy_to_clipboard(text_to_copy)
    print(f"{len(files)} 個のファイル名をクリップボードにコピーした。")

if __name__ == "__main__":
    main()