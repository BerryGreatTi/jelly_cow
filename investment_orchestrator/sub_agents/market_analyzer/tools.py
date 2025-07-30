import json
import traceback
import yfinance as yf


def get_ohlcv(ticker: str, period: str = "1y") -> str:
    """
    yfinance 라이브러리를 이용하여 ticker와 period를 받아 ticker의 최근 period 기간 동안 OHLCV 히스토리를 받아옵니다.

    Args:
        ticker: 주식 티커 심볼 (예: "AAPL").
        period: 데이터를 가져올 기간.
                유효한 값: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max".

    Returns:
        'status'와 'message'를 포함하는 JSON 문자열.
        - 성공 시: {'status': 'success', 'message': '((일자,open,high,close,volume),...)'}
        - 실패 시: {'status': 'error', 'message': '<에러 트레이스백>'}
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"'{ticker}'에 대한 데이터를 찾을 수 없습니다 (기간: {period}).")

        # 요청된 형식(OHLCV)에 맞게 데이터 포맷팅
        ohlcv_data = tuple(
            (
                index.strftime('%Y-%m-%d'),
                row.Open,
                row.High,
                row.Close,
                int(row.Volume)
            )
            for index, row in hist[['Open', 'High', 'Close', 'Volume']].iterrows()
        )

        response = {"status": "success", "message": str(ohlcv_data)}
    except Exception:
        response = {
            "status": "error",
            "message": traceback.format_exc(),
        }

    return json.dumps(response, ensure_ascii=False)
