import discordwebhook
import schedule
import time
import cinfo_exec
from readSetting import ReadConfig, logging

logger = logging()
config = ReadConfig(logger=logger)

TMP_RES = ""


def job():
    global TMP_RES
    # ウェブフックURL
    discord = discordwebhook.Discord(url=config.webhookURL)

    # BonDriverProxyExのIPアドレスとポート番号
    try:
        res = cinfo_exec.startCinfo(str(config.ProxyEx_IP), int(config.ProxyEx_Port))
    except Exception as e:
        logger.error("client.exeの実行時にエラーが発生しました。")
        logger.error(e)
        return

    # logger.debug(f"res: {res}")
    # 文字列が空の場合
    if not res:
        if res == TMP_RES:
            pass
        else:
            # 接続状態がなくなった場合
            discord.post(content="接続が無くなりました。")
            TMP_RES = res
    # 以前通知した内容から変化がなければ通知しない
    if res == TMP_RES:
        pass
    else:
        # 投稿する
        discord.post(content=res)
        TMP_RES = res


# 指定秒数おきに実行する
schedule.every(int(config.interval)).seconds.do(job)

while True:
    schedule.run_pending()  # 3. 指定時間が来てたら実行、まだなら何もしない
    time.sleep(10)  # 待ち
