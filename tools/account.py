import os
import json
from apis.koreainvestment import KoreaInvestmentAPI

account = KoreaInvestmentAPI(os.environ.get('KIS_PROFILE_PATH'))

def get_current_portfolio():
    """
    Retrieves the current investment portfolio, including stocks and cash balances,
    by consolidating information from domestic, overseas, and general account balance APIs.

    Returns:
        dict: A dictionary representing the consolidated portfolio. The dictionary has keys
              'domestic_stocks', 'overseas_stocks', 'cash', and 'summary'. Returns an
              error message dictionary if any of the API calls fail.
    """
    portfolio = {
        "domestic_stocks": [],
        "overseas_stocks": [],
        "cash": {},
        "summary": {}
    }

    # Inquire Domestic Stock Balance
    domestic_res = account.inquire_domestic_stock_balance()
    if domestic_res['status_code'] == 200:
        domestic_data = json.loads(domestic_res['message'])
        if domestic_data.get('output1'):
            for stock in domestic_data['output1']:
                portfolio['domestic_stocks'].append({
                    "ticker": stock.get('pdno'),
                    "name": stock.get('prdt_name'),
                    "quantity": int(stock.get('hldg_qty', 0)),
                    "average_purchase_price": float(stock.get('pchs_avg_pric', 0.0)),
                    "current_price": float(stock.get('prpr', 0.0)),
                    "evaluation_amount": float(stock.get('evlu_amt', 0.0)),
                    "profit_loss": float(stock.get('evlu_pfls_amt', 0.0)),
                    "profit_loss_rate": float(stock.get('evlu_pfls_rt', 0.0))
                })
        if domestic_data.get('output2'):
            summary = domestic_data['output2'][0]
            portfolio['summary']['total_purchase_amount_domestic'] = float(summary.get('pchs_amt_smtl_amt', 0.0))
            portfolio['summary']['total_evaluation_amount_domestic'] = float(summary.get('evlu_amt_smtl_amt', 0.0))
            portfolio['summary']['total_profit_loss_domestic'] = float(summary.get('evlu_pfls_smtl_amt', 0.0))
            portfolio['summary']['net_asset_total'] = float(summary.get('nass_amt', 0.0))
            portfolio['cash']['krw'] = float(summary.get('dnca_tot_amt', 0.0))
    else:
        return {"status_code": domestic_res['status_code'], "message": f"Failed to get domestic balance: {domestic_res['message']}"}

    # Inquire Overseas Stock Balance
    overseas_res = account.inquire_overseas_stock_balance()
    if overseas_res['status_code'] == 200:
        overseas_data = json.loads(overseas_res['message'])
        if overseas_data.get('output1'):
            for stock in overseas_data['output1']:
                portfolio['overseas_stocks'].append({
                    "ticker": stock.get('ovrs_pdno'),
                    "name": stock.get('ovrs_item_name'),
                    "quantity": int(stock.get('ovrs_cblc_qty', 0)),
                    "average_purchase_price": float(stock.get('pchs_avg_pric', 0.0)),
                    "current_price": float(stock.get('now_pric2', 0.0)),
                    "evaluation_amount": float(stock.get('ovrs_stck_evlu_amt', 0.0)),
                    "profit_loss": float(stock.get('frcr_evlu_pfls_amt', 0.0)),
                    "profit_loss_rate": float(stock.get('evlu_pfls_rt', 0.0)),
                    "currency": stock.get('tr_crcy_cd')
                })
        if overseas_data.get('output2'):
            summary = overseas_data['output2']
            portfolio['summary']['total_purchase_amount_overseas'] = float(summary.get('frcr_pchs_amt1', 0.0))
            portfolio['summary']['total_evaluation_amount_overseas'] = float(summary.get('tot_evlu_pfls_amt', 0.0))
            portfolio['summary']['total_profit_loss_overseas'] = float(summary.get('ovrs_tot_pfls', 0.0))
    else:
        return {"status_code": overseas_res['status_code'], "message": f"Failed to get overseas balance: {overseas_res['message']}"}

    # Inquire Account Balance for Cash
    balance_res = account.inquire_account_balance()
    if balance_res['status_code'] == 200:
        balance_data = json.loads(balance_res['message'])
        if balance_data.get('Output2'):
            # This provides a more detailed cash breakdown if available
            portfolio['cash']['krw'] = float(balance_data['Output2'].get('dncl_amt', portfolio['cash'].get('krw', 0.0)))
            # Assuming 'frcr_evlu_tota' might represent foreign currency assets total value.
            # The API does not provide a clear breakdown of cash by currency.
            # This part may need refinement based on more detailed API specs.
            if not portfolio['cash'].get('usd'):
                 portfolio['cash']['usd'] = 0.0 # Placeholder
    else:
        return {"status_code": balance_res['status_code'], "message": f"Failed to get account balance: {balance_res['message']}"}


    return portfolio
