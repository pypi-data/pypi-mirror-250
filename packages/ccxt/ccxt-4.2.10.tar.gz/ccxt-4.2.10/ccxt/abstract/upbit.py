from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_market_all = publicGetMarketAll = Entry('market/all', 'public', 'GET', {})
    public_get_candles_timeframe = publicGetCandlesTimeframe = Entry('candles/{timeframe}', 'public', 'GET', {})
    public_get_candles_timeframe_unit = publicGetCandlesTimeframeUnit = Entry('candles/{timeframe}/{unit}', 'public', 'GET', {})
    public_get_candles_minutes_unit = publicGetCandlesMinutesUnit = Entry('candles/minutes/{unit}', 'public', 'GET', {})
    public_get_candles_minutes_1 = publicGetCandlesMinutes1 = Entry('candles/minutes/1', 'public', 'GET', {})
    public_get_candles_minutes_3 = publicGetCandlesMinutes3 = Entry('candles/minutes/3', 'public', 'GET', {})
    public_get_candles_minutes_5 = publicGetCandlesMinutes5 = Entry('candles/minutes/5', 'public', 'GET', {})
    public_get_candles_minutes_15 = publicGetCandlesMinutes15 = Entry('candles/minutes/15', 'public', 'GET', {})
    public_get_candles_minutes_30 = publicGetCandlesMinutes30 = Entry('candles/minutes/30', 'public', 'GET', {})
    public_get_candles_minutes_60 = publicGetCandlesMinutes60 = Entry('candles/minutes/60', 'public', 'GET', {})
    public_get_candles_minutes_240 = publicGetCandlesMinutes240 = Entry('candles/minutes/240', 'public', 'GET', {})
    public_get_candles_days = publicGetCandlesDays = Entry('candles/days', 'public', 'GET', {})
    public_get_candles_weeks = publicGetCandlesWeeks = Entry('candles/weeks', 'public', 'GET', {})
    public_get_candles_months = publicGetCandlesMonths = Entry('candles/months', 'public', 'GET', {})
    public_get_trades_ticks = publicGetTradesTicks = Entry('trades/ticks', 'public', 'GET', {})
    public_get_ticker = publicGetTicker = Entry('ticker', 'public', 'GET', {})
    public_get_orderbook = publicGetOrderbook = Entry('orderbook', 'public', 'GET', {})
    private_get_accounts = privateGetAccounts = Entry('accounts', 'private', 'GET', {})
    private_get_orders_chance = privateGetOrdersChance = Entry('orders/chance', 'private', 'GET', {})
    private_get_order = privateGetOrder = Entry('order', 'private', 'GET', {})
    private_get_orders = privateGetOrders = Entry('orders', 'private', 'GET', {})
    private_get_withdraws = privateGetWithdraws = Entry('withdraws', 'private', 'GET', {})
    private_get_withdraw = privateGetWithdraw = Entry('withdraw', 'private', 'GET', {})
    private_get_withdraws_chance = privateGetWithdrawsChance = Entry('withdraws/chance', 'private', 'GET', {})
    private_get_deposits = privateGetDeposits = Entry('deposits', 'private', 'GET', {})
    private_get_deposit = privateGetDeposit = Entry('deposit', 'private', 'GET', {})
    private_get_deposits_coin_addresses = privateGetDepositsCoinAddresses = Entry('deposits/coin_addresses', 'private', 'GET', {})
    private_get_deposits_coin_address = privateGetDepositsCoinAddress = Entry('deposits/coin_address', 'private', 'GET', {})
    private_post_orders = privatePostOrders = Entry('orders', 'private', 'POST', {})
    private_post_withdraws_coin = privatePostWithdrawsCoin = Entry('withdraws/coin', 'private', 'POST', {})
    private_post_withdraws_krw = privatePostWithdrawsKrw = Entry('withdraws/krw', 'private', 'POST', {})
    private_post_deposits_generate_coin_address = privatePostDepositsGenerateCoinAddress = Entry('deposits/generate_coin_address', 'private', 'POST', {})
    private_delete_order = privateDeleteOrder = Entry('order', 'private', 'DELETE', {})
