# BonDriverProxyEx_webhoock_notify
## client
実際にBonDriverProxyExに接続しているクライアントの情報を収集するソフト  

## checktool
clientフォルダで生成した、client.exeを用いて、discord webhoockに情報を通知する  

main.py上にウェブフックURLとBonDriverProxyExのIPアドレスとポート番号を指定し、
チェックを実行する間隔を指定する。

```
pip install -r requirements.txt
## pyinstaller .\main.py --onefile --name checktool # Windows Defenderによって駆除される
python -m nuitka main.py --onefile --standalone --output-filename=checktool.exe
```
設定ファイル`config.template.yml`をコピーして`config.yml`を作成します。  
`start.bat`を実行すると実行されます。