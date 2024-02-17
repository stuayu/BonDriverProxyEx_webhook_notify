"""cinfo.exeを操作する関数ファイル
"""

import subprocess


def startCinfo(addr: str, port: int) -> str:
    """cinfoを実行

    Args:
        addr (str): 確認するサーバーのIPアドレス
        port (int): サーバーのポート番号

    Returns:
        str: 実行結果を文字列で返す
    """
    sp = subprocess.run(
        ["client.exe", addr, str(port)],
        capture_output=True,
        text=True,
    )

    return sp.stdout


if __name__ == "__main__":
    startCinfo("192.168.2.110", 1192)
