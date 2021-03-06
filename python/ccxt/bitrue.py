# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import time
import hashlib

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class bitrue(Exchange):

    def describe(self):
        return self.deep_extend(super(bitrue, self).describe(), {
            'id': 'bitrue',
            'name': 'Bitrue',
            'countries': ['US'],
            'version': 'v1',
            'rateLimit': 3000,
            'diff_millis': None,
            'urls': {
                'logo': 'https://www.bitrue.com/includes/assets/346c710f38975f71fa8ea90f9f7457a3.svg',
                'api': 'https://www.bitrue.com/api',
                'www': 'https://bitrue.com',
                'doc': 'https://github.com/Bitrue/bitrue-official-api-docs',
                'referral': 'https://www.bitrue.com/activity/task/task-landing?inviteCode=TAEZWW&cn=900000',
            },
            'has': {
                'fetchMarkets': True,
                'fetchCurrencies': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': False,
                'fetchTrades': True,
                'fetchTradingLimits': False,
                'fetchTradingFees': False,
                'fetchAllTradingFees': False,
                'fetchFundingFees': False,
                'fetchTime': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchBalance': True,
                'createMarketOrder': True,
                'createOrder': True,
                'cancelOrder': True,
                'cancelOrders': False,
                'cancelAllOrders': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '4h': '4h',
                '12h': '12h',
                '1d': '1d',
                '1w': '1w',
            },
            'api': {
                'public': {
                    'get': [
                        'exchangeInfo',
                        'ticker/24hr',
                        'ticker/24hr',
                        'depth',
                        'trades',
                        'time',
                    ],
                },
                'private': {
                    'get': [
                        'account',
                        'order',
                        'openOrders',
                        'myTrades',
                        "allOrders",
                    ],
                    'post': [
                        'order',
                    ],
                    'delete':[
                        'order',
                    ]
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'PLA': 'Plair',
            },
            'exceptions': {
                'codes': {
                    '-1': BadRequest,
                    '-2': BadRequest,
                    '1001': BadRequest,
                    '1004': ArgumentsRequired,
                    '1006': AuthenticationError,
                    '1008': AuthenticationError,
                    '1010': AuthenticationError,
                    '1011': PermissionDenied,
                    '2001': AuthenticationError,
                    '2002': InvalidOrder,
                    '2004': OrderNotFound,
                    '9003': PermissionDenied,
                },
                'exact': {
                    'market does not have a valid value': BadRequest,
                    'side does not have a valid value': BadRequest,
                    'Account::AccountError: Cannot lock funds': InsufficientFunds,
                    'The account does not exist': AuthenticationError,
                },
            },
        })

    def fetch_markets(self, params={}):
        request = {'show_details': True}
        response = self.publicGetExchangeInfo(self.extend(request, params))
        result = []
        # symbols = self.safe_value(response, 'symbols')
        markets = self.safe_value(response, 'symbols')
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_value(market, 'symbol').lower()
            base = self.safe_value(market, 'baseAsset').upper()
            quote = self.safe_value(market, 'quoteAsset').upper()
            name = base + '/' + quote
            baseId = base.lower()
            quoteId = quote.lower()
            symbol = base + '/' + quote
            filters = self.safe_value(market, "filters")
            price_filter = filters[0]
            volume_filter = filters[1]
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'info': market,
                'precision': {
                    'amount': self.safe_value(volume_filter, 'volumeScale'),
                    'price': self.safe_value(price_filter, 'priceScale'),
                    'base': self.safe_value(volume_filter, 'volumeScale'),
                    'quote': self.safe_value(price_filter, 'priceScale'),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_value(volume_filter, 'minQty'),
                        'max': self.safe_value(volume_filter, 'maxQty'),
                    },
                    'price': {
                        'min': self.safe_value(price_filter, 'minPrice'),
                        'max': self.safe_value(price_filter, 'maxPrice'),
                    },
                    'cost': {
                        'min': self.safe_value(volume_filter, 'minQty'),
                        'max': self.safe_value(volume_filter, 'maxQty')
                    },
                },
            })
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTicker24hr(self.extend(request, params))
        data = response[0] if response and len(response) > 0 else None
        return self.parse_ticker(data, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        request = {}
        response = self.publicGetTicker24hr(self.extend(request, params))
        data = response if response and len(response) > 0 else []
        result = {}
        for i in range(0, len(data)):
            ticker = data[i]
            marketId = self.safe_string(ticker, 'symbol').lower()
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def parse_ticker(self, data, market=None):
        timestamp = self.safe_timestamp(data, 'closeTime')
        if timestamp is None or timestamp == 0:
            timestamp = int(time.time() * 1000)
        return {
            'symbol': market['symbol'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(data, 'highPrice'),
            'low': self.safe_float(data, 'lowPrice'),
            'bid': self.safe_float(data, 'bidPrice'),
            'bidVolume': None,
            'ask': self.safe_float(data, 'askPrice'),
            'askVolume': None,
            'vwap': self.safe_float(data, 'weightedAvgPrice'),
            'open': self.safe_float(data, 'openPrice'),
            'close': self.safe_float(data, 'lastPrice'),
            'last': self.safe_float(data, 'lastPrice'),
            'previousClose': self.safe_float(data, 'prevClosePrice'),
            'change': self.safe_float(data, 'priceChange'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(data, 'volume'),
            'quoteVolume': self.safe_float(data, "quoteVolume"),
            'info': data,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetDepth(self.extend(request, params))
        
        orderbook = response if response else {}
        timestamp = self.safe_timestamp(orderbook, 'lastUpdateId') // 1000
        return self.parse_order_book(orderbook, timestamp)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTrades(self.extend(request, params))
        data = response if isinstance(response, (list,)) else []
        return self.parse_trades(data, market, since, limit)

    def parse_trade(self, trade, market=None):
        is_buy_maker = self.safe_value(trade, 'isBuyerMaker')
        is_best_match = self.safe_value(trade, 'isBestMatch')
        if not is_buy_maker and is_best_match:
            side = 'buy'
        elif is_buy_maker and is_best_match:
            side = 'sell'
        symbol = None
        
        if market is not None:
            marketId = market['id']
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                symbol = marketId
        if symbol is None:
            if market is None:
                market = self.markets_by_id[self.safe_string(trade, 'symbol').lower()]
            symbol = market['symbol']

        timestamp = self.safe_timestamp(trade, 'time') // 1000
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(trade, 'time'))
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'id'),
            'order': None,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'qty'),
            'cost': None,
            'fee': None,
        }
    
    def load_time_diff(self):
        if self.diff_millis is None:
            self.fetch_time()

    def fetch_time(self, params={}):
        response = self.publicGetTime(params)
        server_millis = self.safe_integer(response, 'serverTime')
        local_millis = self.milliseconds()
        self.diff_millis = server_millis - local_millis
        return server_millis

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccount(params)
        balances = self.safe_value(response, 'balances')
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_value(balance, 'asset')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'free')
            account['used'] = self.safe_float(balance, 'locked')
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, side, amount, ord_type='LIMIT', price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'side': side,
            'type': ord_type,
            'quantity': self.amount_to_precision(symbol, amount),
        }
        if ord_type == 'LIMIT':
            request['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrder(self.extend(request, params))
        return self.parse_order(response, market)
        

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {'orderId': id, 'symbol': market['id']}
        response = self.privateGetOrder(self.extend(request, params))
        if "orderId" not in response:
            raise OrderNotFound(self.id + ' could not found matching order')
        return self.parse_order(response, market)

    def fetch_open_orders(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id']
        }
        response = self.privateGetOpenOrders(self.extend(request, params))
        orders = response if isinstance(response, (list)) else []
        result = self.parse_orders(orders, market, None, None, params={})
        return result


    def fetch_closed_orders(self, symbol=None, start_id=None, limit=None, params={}):
        self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
        request = {}
        if symbol is not None:
            request['symbol'] = market['id']
        if start_id is not None:
            request['fromId'] = start_id
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetMyTrades(self.extend(request, params))
        trades = response if isinstance(response, (list)) else []
        result = []
        for i in range(0, len(trades)):
            trade = self.parse_trade(trades[i], None)
            result.append(trade)
        return result

    def fetch_orders(self, symbol=None, orderId=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        states = self.safe_value(params, 'states', [])  # 'NEW', 'PARTIALLY_FILLED', 'CANCELED', 'FILLED'
        query = self.omit(params, 'states')
        request = {
            'symbol': market['id'],
        }
        if orderId is not None:
            request['orderId'] = orderId
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetAllOrders(self.extend(request, query))
        orders = response if isinstance(response, (list)) else []
        result = self.parse_orders(orders, market, orderId, limit, {})
        return result

    def parse_order(self, order, market=None):
        #{
        #   "symbol": "BATBTC",
        #   "orderId": "194601105",
        #   "clientOrderId": "",
        #   "price": "0.0000216600000000",
        #   "origQty": "155.0000000000000000",
        #   "executedQty": "0.0000000000000000",
        #   "cummulativeQuoteQty": "0.0000000000000000",
        #   "status": "NEW",
        #   "timeInForce": "",
        #   "type": "LIMIT",
        #   "side": "BUY",
        #   "stopPrice": "",
        #   "icebergQty": "",
        #   "time": 1590637046000,
        #   "updateTime": 1590637046000,
        #   "isWorking": "False"
        # }
        status = self.parse_order_status(self.safe_value(order, 'status'))
        symbol = None
        if market is not None:
            symbol = market['symbol']
        else:
            market = self.markets_by_id[self.safe_string(order, 'symbol').lower()]
        timestamp = self.safe_integer_2(order, 'time', 'transactTime')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(order, 'updateTime'))
        execute_qty = self.safe_float(order, 'executedQty')
        orig_qty = self.safe_float(order, 'origQty')
        if execute_qty is None:
            execute_qty = 0
        return {
            'info': order,
            'id': self.safe_string(order, 'orderId'),
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': self.safe_value(order, 'type'),
            'side': self.safe_value(order, 'side'),
            'price': self.safe_float(order, 'price'),
            'average': self.safe_float(order, 'cummulativeQuoteQty')/ execute_qty if execute_qty > 0 else .0,
            'amount': orig_qty,
            'remaining': orig_qty - execute_qty if orig_qty else None,
            'filled': execute_qty,
            'status': status,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    def parse_order_status(self, status):
        statuses = {
            'NEW': 'open',
            'PARTIALLY_FILLED': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
            'PENDING_CANCEL': 'canceled',
            'REJECTED': 'failed',
            'EXPIRED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'orderId': id,
        }
        response = self.privateDeleteOrder(self.extend(request, params))
        return response

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            self.load_time_diff()
            timestamp = self.milliseconds() + self.diff_millis if self.diff_millis is not None else 0
            query = self.extend({'timestamp':timestamp}, query)
            sign_str = "&".join(["%s=%s" % (key, query[key]) for key in sorted(query.keys())])
            signature = self.hmac(self.encode(sign_str), self.encode(self.secret), hashlib.sha256)
            query = self.extend({'signature': signature}, query)
            if method == 'GET':
                url += "?" + sign_str + "&signature=" + signature
            else:
                body = sign_str + "&signature=" + signature
        headers = {'Content-Type': 'application/json', 'X-MBX-APIKEY': self.apiKey}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        #
        #     {"code":1011,"message":"This IP '5.228.233.138' is not allowed","data":{}}
        #
        if response is None:
            return
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'message')
        if (errorCode is not None) and (errorCode != '0'):
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['codes'], errorCode, feedback)
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            raise ExchangeError(response)
