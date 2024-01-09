from ibapi.contract import Contract


def stock(symbol: str, currency: str = "USD", exchange: str = "SMART") -> Contract:
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = currency
    contract.exchange = exchange
    return contract
