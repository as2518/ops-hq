from operationHQ.settings import CHATWORK_API_URL,CHATWORK_API_TOKEN,ROOM_ID,WEB_URL #you must write API_TOKEN and ROOM_ID into settings.py
from pprint import pprint
from datetime import datetime
import requests

def cw_notice(title,id,mode):
    room_message = '{0}rooms/{1}/messages'.format(CHATWORK_API_URL,ROOM_ID)
    if mode == 1:
        message= '(*) 作業登録通知 (*)\n\
        作業が新たに登録されました。作業内容を確認して下さい\n\
        作業概要 : {0}\n\
        詳細URL : {1}/ops_manager/detail/{2}/'.format(title,WEB_URL,id)
    elif mode == 2:
        message= '(h) 作業確認通知 (h)\n\
        下記作業が承認されました。手順書をダウンロードし、作業を実行して下さい\n\
        作業概要 : {0}\n\
        詳細URL : {1}/ops_manager/detail/{2}/'.format(title,WEB_URL,id)

    option = {'body': message}
    headers = {'content-type':'application/json','X-ChatWorkToken':CHATWORK_API_TOKEN}
    r = requests.post(room_message,params=option,headers=headers)
    print(r.text)
    return