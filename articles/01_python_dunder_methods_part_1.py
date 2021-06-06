class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""

    def __init__(self, coin: str, amount: int = 0) -> None:
        """
        This constructor lets us create objects from this calss.
        """
        self.coin = coin
        self.amount = amount
        self._trades = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coin}, {self.amount})"

    def __str__(self):
        return f"Portfolio for {self.coin} with starting amount: {self.amount}"

    def buy(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Please add a int value.")
        self._trades.append(amount)

    def sell(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Please add a int value.")
        if self.balance - amount < 0:
            raise ValueError(
                f"You cannot sell, portfolio balance to low. Balance: {self.balance}"
            )
        self._trades.append(-amount)

    @property
    def balance(self):
        return self.amount + sum(self._trades)

    def __len__(self):
        return len(self._trades)

    def __getitem__(self, position):
        return self._trades[position]

    def __reversed__(self):
        return self[::-1]


if __name__ == "__main__":

    btc_portfolio = CryptoPortfolio("bitcoin")
    eth_portfolio = CryptoPortfolio("ethereum", amount=80)

    print(btc_portfolio)
    print(eth_portfolio)
    print(repr(btc_portfolio))
    print(repr(eth_portfolio))

    btc_portfolio = CryptoPortfolio("bitcoin", amount=100)
    btc_portfolio.buy(100)
    btc_portfolio.sell(50)
    btc_portfolio.sell(40)
    btc_portfolio.buy(390)

    print(btc_portfolio.balance)
    print(len(btc_portfolio))

    for trade in btc_portfolio:
        print(trade)

    print(f"First trade: {btc_portfolio[0]}")

    print(f"Trades reversed: {list(reversed(btc_portfolio))}")
