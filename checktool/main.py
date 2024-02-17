import discordwebhook
import schedule
import time
import cinfo_exec

TMP_RES = ""


def job():
    global TMP_RES
    # ウェブフックURL
    discord = discordwebhook.Discord(
        url="https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )

    # BonDriverProxyExのIPアドレスとポート番号
    res = cinfo_exec.startCinfo("127.0.0.1", 1192)

    # 文字列がからであれば通知しない
    if not res:
        pass
    # 以前通知した内容から変化がなければ通知しない
    if res == TMP_RES:
        pass
    else:
        # 投稿する
        discord.post(content=res)
        TMP_RES = res


# 5分おきに実行する
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()  # 3. 指定時間が来てたら実行、まだなら何もしない
    time.sleep(10)  # 待ち
