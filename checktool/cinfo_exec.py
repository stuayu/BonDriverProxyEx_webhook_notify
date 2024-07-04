"""cinfo.exeを操作する関数ファイル
"""

import os
import subprocess
import re
import socket


def get_domain_name(ip_address):
    try:
        domain_name, _, _ = socket.gethostbyaddr(ip_address)
        return domain_name
    except socket.herror:
        return None


def startCinfo(addr: str, port: int) -> tuple[str, str]:
    """cinfoを実行

    Args:
        addr (str): 確認するサーバーのIPアドレス
        port (int): サーバーのポート番号

    Returns:
        str: 実行結果を文字列で返す
    """
    path = "client.exe"
    if os.path.exists(path):
        sp = subprocess.run(
            [path, addr, str(port)],
            capture_output=True,
            text=True,
        )
    else:
        raise Exception(f"{path}が存在しません。")

    return sp.stdout, sp.stderr


def analysis(access_info: str):

    # 正規表現を使用して文字列から必要な情報を抽出
    pattern = re.compile(
        r"(\d+):\s\[(.*?)\]:\[(\d+)\]\s/\s\[(.*?)\]\[(.*?)\]\s/\sspace\[(\d+)\]\sch\[(\d+)\]"
    )
    matches = pattern.finditer(access_info)

    # 正規表現がマッチした場合にのみ処理を行う
    result_list = []
    for match in matches:
        ip_address = match.group(2)
        domain_name = get_domain_name(ip_address)
        # 抽出した情報を辞書に格納
        result_dict = {
            "index": int(match.group(1)),
            "ip_address": match.group(2),
            "domain_name": domain_name,
            "port": int(match.group(3)),
            "driver_type": match.group(4),
            "file_path": match.group(5),
            "space": int(match.group(6)),
            "channel": int(match.group(7)),
        }

        # 結果の表示
        # print(result_dict)
        result_list.append(result_dict)

    return result_list


if __name__ == "__main__":
    res, err = startCinfo("192.168.2.110", 1192)
    print(res)
    dict_list = analysis(res)

    print(len(dict_list))
