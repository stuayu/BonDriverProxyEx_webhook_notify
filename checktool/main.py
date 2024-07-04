import os
import discordwebhook
import schedule
import time
import cinfo_exec
from readSetting import ReadConfig, clogging
import sys

logger = clogging()
config = ReadConfig(logger=logger)

TMP_RES = ""
TMP_ERR = ""


def job():
    global TMP_RES
    global TMP_ERR
    # ウェブフックURL
    discord = discordwebhook.Discord(url=config.webhookURL)

    # BonDriverProxyExのIPアドレスとポート番号
    try:
        res, err = cinfo_exec.startCinfo(
            str(config.ProxyEx_IP), int(config.ProxyEx_Port)
        )
    except Exception as e:
        discord.post(
            content="client.exeの実行時にエラーが発生しました。プログラムを終了します。\n"
            + e
        )
        logger.error("client.exeの実行時にエラーが発生しました。")
        logger.error(e)
        sys.exit(-1)

    # 取得した接続状態から解析する
    access_data_list = cinfo_exec.analysis(access_info=res)

    # エラー
    if err:
        if err == TMP_ERR:
            pass
        else:
            TMP_ERR = err
            discord.post(content=err)
    else:
        if err == TMP_ERR:
            pass
        else:
            discord.post(content="BonDriverProxyExが正常に復帰しました")
            TMP_ERR = ""
    # logger.debug(f"res: {res}")
    # 文字列が空の場合
    # 文章を生成する
    message = ""
    for access in access_data_list:
        message += f"IPアドレス: **[{access['ip_address']}]** ドメイン: {access['domain_name']} グループ名: **{access['driver_type']}** スペース: {access['space']} チャンネル: {access['channel']} Driver: {os.path.basename(access['file_path'])}\n"

    if not message:
        if message == TMP_RES:
            pass
        else:
            # 接続状態がなくなった場合
            discord.post(content="接続が無くなりました。")
            TMP_RES = message
    # 以前通知した内容から変化がなければ通知しない
    if message == TMP_RES:
        pass
    else:
        # 投稿する
        discord.post(content=message)
        TMP_RES = message


# 指定秒数おきに実行する
schedule.every(int(config.interval)).seconds.do(job)

while True:
    schedule.run_pending()  # 3. 指定時間が来てたら実行、まだなら何もしない
    time.sleep(10)  # 待ち
