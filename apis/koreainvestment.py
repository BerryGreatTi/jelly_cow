import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import json

kst = ZoneInfo('Asia/Seoul')


class KoreaInvestmentAPI:
    def __init__(self, profile_path):
        with open(profile_path) as json_file:
            profile = json.load(json_file)
        self.__appkey = profile['appkey']
        self.__appsecret = profile['appsecret']
        self.__cano = profile['cano']
        self.__acnt_prdt_cd = profile['acnt_prdt_cd']
        self.__access_token = ''
        self.access_token_expired = datetime(year=2000, month=1, day=1, tzinfo=kst)
        self.__is_test = profile['is_test'] # 모의거래인 경우 True, 실거래인 경우 False

    def is_access_token_valid(self):
        if self.access_token_expired >= datetime.now(tz=kst) + timedelta(minutes=15) and self.__access_token:
            return True
        else:
            return False
    
    def __inquire_access_token(self):
        if self.is_access_token_valid():
            return {
                'status_code': 200,
                'message': 'Current access token is valid.'
            }
        
        if self.__is_test:
            domain = "https://openapivts.koreainvestment.com:29443"
        else:
            domain = "https://openapi.koreainvestment.com:9443"

        url = domain + '/oauth2/tokenP'
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
            self.access_token_expired = datetime.strptime(res.json()['access_token_token_expired'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=kst)
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
        """
        Inquires about the user's investment account balance from the Korea Investment API.

        This method retrieves the current balance of the account specified by `self.__cano`
        and `self.__acnt_prdt_cd`. It first ensures a valid access token is available.
        This API is not supported in the test environment.

        Parameters:
            self: The instance of the KoreaInvestmentAPI class. (Implicitly uses `self.__cano`
                  and `self.__acnt_prdt_cd` for the query.)

        Returns:
            dict: A dictionary containing the status code and the API response message.
                  The 'message' field contains a JSON string with the account balance details.
                  Example structure of the JSON string in 'message':
                  {
                      "rt_cd": "성공 실패 여부 (Success/Failure code)",
                      "msg_cd": "응답코드 (Response code)",
                      "msg1": "응답메세지 (Response message)",
                      "Output1": [
                          {
                              "pchs_amt": "매입금액 (Purchase amount)",
                              "evlu_amt": "평가금액 (Evaluation amount)",
                              "evlu_pfls_amt": "평가손익금액 (Evaluation profit/loss amount)",
                              "crdt_lnd_amt": "신용대출금액 (Credit loan amount)",
                              "real_nass_amt": "실제순자산금액 (Real net asset amount)",
                              "whol_weit_rt": "전체비중율 (Overall weight ratio)"
                          },
                          ... (other asset categories)
                      ],
                      "Output2": {
                          "pchs_amt_smtl": "매입금액합계 (Total purchase amount)",
                          "nass_tot_amt": "순자산총금액 (Total net asset amount)",
                          "loan_amt_smtl": "대출금액합계 (Total loan amount)",
                          "evlu_pfls_amt_smtl": "평가손익금액합계 (Total evaluation profit/loss amount)",
                          "evlu_amt_smtl": "평가금액합계 (Total evaluation amount)",
                          "tot_asst_amt": "총자산금액 (Total asset amount)",
                          "tot_lnda_tot_ulst_lnda": "총대출금액총융자대출금액",
                          "cma_auto_loan_amt": "CMA자동대출금액",
                          "tot_mgln_amt": "총담보대출금액",
                          "stln_evlu_amt": "대주평가금액",
                          "crdt_fncg_amt": "신용융자금액",
                          "ocl_apl_loan_amt": "OCL_APL대출금액",
                          "pldg_stup_amt": "질권설정금액",
                          "frcr_evlu_tota": "외화평가총액",
                          "tot_dncl_amt": "총예수금액",
                          "cma_evlu_amt": "CMA평가금액",
                          "dncl_amt": "예수금액",
                          "tot_sbst_amt": "총대용금액",
                          "thdt_rcvb_amt": "당일미수금액",
                          "ovrs_stck_evlu_amt1": "해외주식평가금액1",
                          "ovrs_bond_evlu_amt": "해외채권평가금액",
                          "mmf_cma_mgge_loan_amt": "MMFCMA담보대출금액",
                          "sbsc_dncl_amt": "청약예수금액",
                          "pbst_sbsc_fnds_loan_use_amt": "공모주청약자금대출사용금액",
                          "etpr_crdt_grnt_loan_amt": "기업신용공여대출금액"
                      }
                  }
        """
        self.__inquire_access_token()
    
        if self.__is_test:
            return {
                'status_code': 405,
                'message': 'The method is not allowed for test domain.'
            }
        else:
            domain = "https://openapi.koreainvestment.com:9443"
            tr_id = "CTRP6548R"

        path = '/uapi/domestic-stock/v1/trading/inquire-account-balance'
        url = domain + path
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.__access_token,
            'appkey': self.__appkey,
            'appsecret': self.__appsecret,
            'tr_id': tr_id,
            'custtype' : 'P',
        }
        params = {
            'CANO': self.__cano,
            'ACNT_PRDT_CD': self.__acnt_prdt_cd,
            'INQR_DVSN_1': '',
            'BSPR_BF_DT_APLY_YN': '',
        }

        res = requests.get(url, headers=headers, params=params)
        return {
            'status_code': res.status_code,
            'message': res.text,
        }
    

    def inquire_domestic_stock_balance(self):
        """
        Inquires about the user's domestic stock balance from the Korea Investment API.

        This method retrieves a list of domestic stocks held in the account, including details
        such as the ticker, quantity, purchase price, and current valuation. It also returns
        a summary of the account's overall financial status. This function works for both
        real and mock investment accounts.

        Parameters:
            self: The instance of the KoreaInvestmentAPI class. (Implicitly uses `self.__cano`
                  and `self.__acnt_prdt_cd` for the query.)

        Returns:
            dict: A dictionary containing the status code and the API response message.
                  The 'message' field contains a JSON string with the domestic stock balance details.
                  Example structure of the JSON string in 'message':
                  {
                      "rt_cd": "성공 실패 여부 (0: 성공, 0 이외: 실패)",
                      "msg_cd": "응답코드",
                      "msg1": "응답메세지",
                      "ctx_area_fk100": "연속조회검색조건100",
                      "ctx_area_nk100": "연속조회키100",
                      "output1": [
                          {
                              "pdno": "상품번호 (종목번호)",
                              "prdt_name": "상품명 (종목명)",
                              "hldg_qty": "보유수량",
                              "ord_psbl_qty": "주문가능수량",
                              "pchs_avg_pric": "매입평균가격",
                              "pchs_amt": "매입금액",
                              "prpr": "현재가",
                              "evlu_amt": "평가금액",
                              "evlu_pfls_amt": "평가손익금액",
                              "evlu_pfls_rt": "평가손익율"
                          },
                          ... (other stock holdings)
                      ],
                      "output2": [
                          {
                              "dnca_tot_amt": "예수금총금액",
                              "scts_evlu_amt": "유가평가금액",
                              "tot_evlu_amt": "총평가금액",
                              "nass_amt": "순자산금액",
                              "pchs_amt_smtl_amt": "매입금액합계금액",
                              "evlu_amt_smtl_amt": "평가금액합계금액",
                              "evlu_pfls_smtl_amt": "평가손익합계금액"
                          }
                      ]
                  }
        """
        self.__inquire_access_token()

        if self.__is_test:
            domain = "https://openapivts.koreainvestment.com:29443"
            tr_id = "VTTC8434R"
        else:
            domain = "https://openapi.koreainvestment.com:9443"
            tr_id = "TTTC8434R"

        path = '/uapi/domestic-stock/v1/trading/inquire-balance'
        url = domain + path
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.__access_token,
            'appkey': self.__appkey,
            'appsecret': self.__appsecret,
            'tr_id': tr_id,
            'custtype' : 'P',
        }
        params = {
            'CANO': self.__cano,
            'ACNT_PRDT_CD': self.__acnt_prdt_cd,
            'AFHR_FLPR_YN': 'N',
            'INQR_DVSN': '02',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '00',
            'OFL_YN': '',
            'CTX_AREA_FK100': '',
            'CTX_AREA_NK100': '',
        }

        res = requests.get(url, headers=headers, params=params)
        return {
            'status_code': res.status_code,
            'message': res.text,
        }
    

    def inquire_overseas_stock_balance(self):
        """
        Inquires about the user's overseas stock balance from the Korea Investment API.

        This method retrieves a list of overseas stocks held in the account, including details
        such as the ticker, quantity, purchase price, and current valuation. It also returns
        a summary of the account's overall financial status. This function works for both
        real and mock investment accounts.

        Parameters:
            self: The instance of the KoreaInvestmentAPI class. (Implicitly uses `self.__cano`
                  and `self.__acnt_prdt_cd` for the query.)

        Returns:
            dict: A dictionary containing the status code and the API response message.
                  The 'message' field contains a JSON string with the overseas stock balance details.
                  Example structure of the JSON string in 'message':
                  {
                      "rt_cd": "성공 실패 여부 (0: 성공, 0 이외: 실패)",
                      "msg_cd": "응답코드",
                      "msg1": "응답메세지",
                      "ctx_area_fk200": "연속조회검색조건200",
                      "ctx_area_nk200": "연속조회키200",
                      "output1": [
                          {
                              "cano": "종합계좌번호",
                              "acnt_prdt_cd": "계좌상품코드",
                              "ovrs_pdno": "해외상품번호 (종목번호)",
                              "ovrs_item_name": "해외종목명",
                              "frcr_evlu_pfls_amt": "외화평가손익금액",
                              "evlu_pfls_rt": "평가손익율",
                              "pchs_avg_pric": "매입평균가격",
                              "ovrs_cblc_qty": "해외잔고수량",
                              "ord_psbl_qty": "주문가능수량",
                              "frcr_pchs_amt1": "외화매입금액1",
                              "ovrs_stck_evlu_amt": "해외주식평가금액",
                              "now_pric2": "현재가격2",
                              "tr_crcy_cd": "거래통화코드",
                              "ovrs_excg_cd": "해외거래소코드"
                          },
                          ... (other overseas stock holdings)
                      ],
                      "output2": {
                          "frcr_pchs_amt1": "외화매입금액1",
                          "ovrs_rlzt_pfls_amt": "해외실현손익금액",
                          "ovrs_tot_pfls": "해외총손익",
                          "rlzt_erng_rt": "실현수익율",
                          "tot_evlu_pfls_amt": "총평가손익금액",
                          "tot_pftrt": "총수익률",
                          "frcr_buy_amt_smtl1": "외화매수금액합계1",
                          "ovrs_rlzt_pfls_amt2": "해외실현손익금액2",
                          "frcr_buy_amt_smtl2": "외화매수금액합계2"
                      }
                  }
        """
        self.__inquire_access_token()

        if self.__is_test:
            domain = "https://openapivts.koreainvestment.com:29443"
            tr_id = "VTTS3012R"
        else:
            domain = "https://openapi.koreainvestment.com:9443"
            tr_id = "TTTS3012R"

        path = '/uapi/overseas-stock/v1/trading/inquire-balance'
        url = domain + path
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + self.__access_token,
            'appkey': self.__appkey,
            'appsecret': self.__appsecret,
            'tr_id': tr_id,
            'custtype' : 'P',
        }
        params = {
            'CANO': self.__cano,
            'ACNT_PRDT_CD': self.__acnt_prdt_cd,
            'OVRS_EXCG_CD': 'NASD',
            'TR_CRCY_CD': 'USD',
            'CTX_AREA_FK200': '',
            'CTX_AREA_NK200': '',
        }

        res = requests.get(url, headers=headers, params=params)
        return {
            'status_code': res.status_code,
            'message': res.text,
        }


    def inquire_domestic_option_balance(self):
        pass

    def inquire_overseas_option_balance(self):
        pass


class KoreaInvestmentAPI_mockup:
    def __init__(self, profile_path):
        self.account = {
            "stocks": {
                "006800.KS": 34,  # 미래에셋증권
                "LMT": 1,   # 록히드마틴                                                                                                                               │
                "NVDA": 5,   # 엔비디아
                "IRDM": 8,   # 이리디움 커뮤니케이션스
                "CRCL": 2,   # 서클 인터넷 그룹
                "FIS": 4,   # 피델리티 내셔널 인포메이션 서비시스
            },
            "cash": {
                "KRW": 12_421 + 9_982,
                "USD": 5.55 + 46.67,
            }
        }
    
    def inquire_account_balance(self):
        return {
            'status_code': 200,
            'message': self.account
        }
    
    def is_access_token_valid(self):
        return True
    
    def send_order(self, ticker, price, volume, currency):
        cost = price * volume
        if self.account['cash'][currency] < cost:
            return {
                'status_code': 204,
                'message': 'Insufficient funds.',
            }
        
        self.account['cash'][currency] -= cost
        if self.account['stocks'].get(ticker):
            self.account['stocks'][ticker] += volume
        else:
            self.account['stocks'][ticker] = volume
        
        return {
            'status_code': 200,
            'message': 'Order sent successfully.',
        }