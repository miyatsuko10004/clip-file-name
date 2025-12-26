# Clip Filenames

指定したディレクトリ内のファイル名をクリップボードにコピーするユーティリティツール。

## 必要要件

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## インストール

```bash
git clone <repository-url>
cd clip-file-name
uv sync
```

## 使い方

```bash
# カレントディレクトリのファイル名をコピー
uv run main.py

# 指定したディレクトリのファイル名をコピー
uv run main.py /path/to/directory

# 隠しファイルも含めてコピー
uv run main.py /path/to/directory --include-hidden
```

## 動作環境

- Linux (xclip/xselが必要)
- Windows (WSL含む)
- macOS
