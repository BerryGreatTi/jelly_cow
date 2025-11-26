from dataclasses import dataclass
from typing import List, Optional
from .endpoint import Endpoint


real_endpoint = Endpoint(
    method='GET',
    url='/uapi/domestic-futureoption/v1/trading/inquire-balance',
    domain='https://openapi.koreainvestment.com:9443',
    tr_id='CTFO6118R',
)

test_endpoint = Endpoint(
    method='GET',
    url='/uapi/domestic-futureoption/v1/trading/inquire-balance',
    domain='https://openapivts.koreainvestment.com:29443',
    tr_id='VTFO6118R',
)


## Request

@dataclass
class RequestHeader:
    # content-type: Optional[str] = None    #컨텐츠타입
    authorization: str    #접근토큰
    appkey: str    #앱키 
    appsecret: str    #앱시크릿키
    personalseckey: Optional[str] = None    #고객식별키
    tr_id: str    #거래ID
    tr_cont: Optional[str] = None    #연속 거래 여부
    custtype: Optional[str] = None    #고객타입
    seq_no: Optional[str] = None    #일련번호
    mac_address: Optional[str] = None    #맥주소
    phone_number: Optional[str] = None    #핸드폰번호
    ip_addr: Optional[str] = None    #접속 단말 공인 IP
    gt_uid: Optional[str] = None    #Global UID

@dataclass
class RequestQueryParam:
    CANO: str    #종합계좌번호
    ACNT_PRDT_CD: str    #계좌상품코드
    MGNA_DVSN: str    #증거금 구분
    EXCC_STAT_CD: str    #정산상태코드
    CTX_AREA_FK200: str    #연속조회검색조건200
    CTX_AREA_NK200: str    #연속조회키200

## Response

@dataclass
class ResponseHeader:
    # content-type: str    #컨텐츠타입
    tr_id: str    #거래ID
    tr_cont: str    #연속 거래 여부
    gt_uid: str    #Global UID


@dataclass
class ResponseBodyoutput1:
    cano: str    #종합계좌번호
    acnt_prdt_cd: str    #계좌상품코드
    pdno: str    #상품번호
    prdt_type_cd: str    #상품유형코드
    shtn_pdno: str    #단축상품번호
    prdt_name: str    #상품명
    sll_buy_dvsn_name: str    #매도매수구분명
    cblc_qty: str    #잔고수량
    excc_unpr: str    #정산단가
    ccld_avg_unpr1: str    #체결평균단가1
    idx_clpr: str    #지수종가
    pchs_amt: str    #매입금액
    evlu_amt: str    #평가금액
    evlu_pfls_amt: str    #평가손익금액
    trad_pfls_amt: str    #매매손익금액
    lqd_psbl_qty: str    #청산가능수량

@dataclass
class ResponseBodyoutput2:
    dnca_cash: str    #예수금현금
    frcr_dncl_amt: str    #외화예수금액
    dnca_sbst: str    #예수금대용
    tot_dncl_amt: str    #총예수금액
    tot_ccld_amt: str    #총체결금액
    cash_mgna: str    #현금증거금
    sbst_mgna: str    #대용증거금
    mgna_tota: str    #증거금총액
    opt_dfpa: str    #옵션차금
    thdt_dfpa: str    #당일차금
    rnwl_dfpa: str    #갱신차금
    fee: str    #수수료
    nxdy_dnca: str    #익일예수금
    nxdy_dncl_amt: str    #익일예수금액
    prsm_dpast: str    #추정예탁자산
    prsm_dpast_amt: str    #추정예탁자산금액
    pprt_ord_psbl_cash: str    #적정주문가능현금
    add_mgna_cash: str    #추가증거금현금
    add_mgna_tota: str    #추가증거금총액
    futr_trad_pfls_amt: str    #선물매매손익금액
    opt_trad_pfls_amt: str    #옵션매매손익금액
    futr_evlu_pfls_amt: str    #선물평가손익금액
    opt_evlu_pfls_amt: str    #옵션평가손익금액
    trad_pfls_amt_smtl: str    #매매손익금액합계
    evlu_pfls_amt_smtl: str    #평가손익금액합계
    wdrw_psbl_tot_amt: str    #인출가능총금액
    ord_psbl_cash: str    #주문가능현금
    ord_psbl_sbst: str    #주문가능대용
    ord_psbl_tota: str    #주문가능총액
    pchs_amt_smtl: str    #매입금액합계
    evlu_amt_smtl: str    #평가금액합계

@dataclass
class ResponseBody:
    rt_cd: str    #성공 실패 여부
    msg_cd: str    #응답코드
    msg1: str    #응답메세지
    ctx_area_fk200: str    #연속조회검색조건200
    ctx_area_nk200: str    #연속조회키200
    output1: List[ResponseBodyoutput1]    #응답상세1
    output2: ResponseBodyoutput2    #응답상세2
