import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import json

kst = ZoneInfo('Asia/Seoul')


class KoreaInvestmentAPI:
    def __init__(self, profile_path):
        temp = json.loads(profile_path)
        self.__appkey = temp['appkey']
        self.__appsecret = temp['appsecret']
        self.domain = temp['domain']
        self.cano = temp['cano']
        self.acnt_prdt_cd = temp['acnt_prdt_cd']
        self.__access_token = ''
        self.access_token_expired = datetime(year=2000, month=1, day=1, tzinfo=kst)

    def is_access_token_valid(self):
        if self.access_token_expired >= datetime.now(tz=kst) + timedelta(hours=1) and self.__access_token:
            return True
        else:
            return False
    
    def __inquire_access_token(self):
        if self.is_access_token_valid():
            return {
                'status_code': 200,
                'message': 'Current access token is valid.'
            }
        
        url = self.domain + '/oauth2/tokenP'
        headers = {
            'content-type': 'application/json',
        }
        body = {
            'grant_type': 'client_credentials',
            'appkey': self.__appkey,
            'appsecret': self.__appsecret,
        }

        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 200:
            self.__access_token = res.json()['access_token']
            self.access_token_expired = datetime.strptime(res.json()['access_token_token_expired'], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=kst)
            return {
                'status_code': 200,
                'message': 'New access token is generated.',
            }
        else:
            return {
                'status_code': res.status_code,
                'message': res.text,
            }


    def inquire_account_balance(self):
        self.__inquire_access_token()
    
        path = '/uapi/domestic-stock/v1/trading/inquire-account-balance'
        url = self.domain + path
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + os.environ['KIS_ACCESS_TOKEN'],
            'appkey': os.environ['KIS_APPKEY'],
            'appsecret': os.environ['KIS_APPSECRET'],
            'tr_id': 'CTRP6548R',
            'custtype' : 'P',
        }
        params = {
            'CANO': self.cano,
            'ACNT_PRDT_CD': self.acnt_prdt_cd,
            'INQR_DVSN_1': '',
            'BSPR_BF_DT_APLY_YN': '',
        }

        res = requests.get(url, headers=headers, params=params)
        return {
            'status_code': res.status_code,
            'message': res.text,
        }