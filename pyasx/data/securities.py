"""
Functions to pull information on ASX listed securities via the ASX.com.au API.
"""


import requests
import pyasx.config


# def get_listed_securities() - XLS download


# normalise security indicies list as part of get_security_info()
def _normalise_security_indices_info(raw):

    indices = []

    if 'indices' in raw:

        for index in raw['indices']:

            code = index['index_code'] if 'index_code' in index else ''
            name = index['name_full'] if 'name_full' in index else ''

            if len(code) and len(name):

                indices.append({
                    'code': code,
                    'name': name
                })

    return indices


def _normalise_security_info(raw):
    """
    Normalise the share info returned from ASX, ensure missing fields are
    always present, cleanup names etc.
    """

    security_info = {}

    security_info['ticker'] = raw['code'] if 'code' in raw else ''
    security_info['isin'] = raw['isin_code'] if 'isin_code' in raw else ''
    security_info['type'] = raw['desc_full'] if 'desc_full' in raw else ''
    security_info['open_price'] = raw['open_price'] if 'open_price' in raw else ''
    security_info['last_price'] = raw['last_price'] if 'last_price' in raw else ''
    security_info['bid_price'] = raw['bid_price'] if 'bid_price' in raw else ''
    security_info['offer_price'] = raw['offer_price'] if 'offer_price' in raw else ''
    security_info['last_trade_date'] = raw['last_trade_date'] if 'last_trade_date' in raw else ''
    security_info['day_high_price'] = raw['day_high_price'] if 'day_high_price' in raw else ''
    security_info['day_low_price'] = raw['day_low_price'] if 'day_low_price' in raw else ''
    security_info['day_change_price'] = raw['change_price'] if 'change_price' in raw else ''
    security_info['day_change_percent'] = raw['change_in_percent'] if 'change_in_percent' in raw else ''
    security_info['day_volume'] = raw['volume'] if 'volume' in raw else ''
    security_info['prev_day_close_price'] = raw['previous_close_price'] if 'previous_close_price' in raw else ''
    security_info['prev_day_change_percent'] = raw['previous_day_percentage_change'] if 'previous_day_percentage_change' in raw else ''
    security_info['year_high_price'] = raw['year_high_price'] if 'year_high_price' in raw else ''
    security_info['year_high_date'] = raw['year_high_date'] if 'year_high_date' in raw else ''
    security_info['year_low_price'] = raw['year_low_price'] if 'year_low_price' in raw else ''
    security_info['year_low_date'] = raw['year_low_date'] if 'year_low_date' in raw else ''
    security_info['year_open_price'] = raw['year_open_price'] if 'year_open_price' in raw else ''
    security_info['year_change_price'] = raw['year_change_price'] if 'year_change_price' in raw else ''
    security_info['year_change_percent'] = raw['year_change_in_percentage'] if 'year_change_in_percentage' in raw else ''
    security_info['average_daily_volume'] = raw['average_daily_volume'] if 'average_daily_volume' in raw else ''
    security_info['pe'] = raw['pe'] if 'pe' in raw else ''
    security_info['eps'] = raw['eps'] if 'eps' in raw else ''
    security_info['annual_dividend_yield'] = raw['annual_dividend_yield'] if 'annual_dividend_yield' in raw else ''
    security_info['securities_outstanding'] = raw['number_of_shares'] if 'number_of_shares' in raw else ''
    security_info['market_cap'] = raw['market_cap'] if 'market_cap' in raw else ''
    security_info['is_suspended'] = raw['suspended'] if 'suspended' in raw else ''

    security_info['indices'] = _normalise_security_indices_info(raw)

    return security_info


def get_security_info(ticker):
    """
    Pull information on the security with the given ticker symbol. This can be
    for any type of listed security, such as company stock, bonds, ETFs etc.
    :param ticker: The ticker symbol of the security to lookup.
    """

    assert(len(ticker) >= 3)

    # build the endpoint to pull security info
    endpoint_pattern = pyasx.config.get('asx_single_json')
    endpoint = endpoint_pattern % ticker.upper()

    # GET the share info
    response = requests.get(endpoint)
    response.raise_for_status()  # throw exception for bad status codes

    # parse response & normalise

    raw_info = response.json()

    security_info = _normalise_security_info(raw_info)

    return security_info
