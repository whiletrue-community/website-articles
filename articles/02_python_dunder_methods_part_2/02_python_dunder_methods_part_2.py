from functools import total_ordering


@total_ordering
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

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __add__(self, other):
        coin = f"{self.coin}&{other.coin}"
        start_amount = self.amount + other.amount
        portfolio = CryptoPortfolio(coin, start_amount)
        for t in list(self) + list(other):
            portfolio.buy(t)
        return portfolio

    def __enter__(self):
        self.file = open("trades.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def export_trades(self):
        with self as file:
            for trade in self:
                file.write(f"{trade}\n")


if __name__ == "__main__":

    btc_portfolio = CryptoPortfolio("bitcoin")
    eth_portfolio = CryptoPortfolio("ethereum", amount=80)
    btc_portfolio.buy(100)

    # Operator Overloading for Comparing Portfolios
    print(btc_portfolio > eth_portfolio)
    print(btc_portfolio < eth_portfolio)
    print(btc_portfolio == eth_portfolio)
    print(btc_portfolio != eth_portfolio)

    # Operator Overloading for Adding Portfolios
    btc_portfolio.buy(20)
    btc_portfolio.sell(30)
    eth_portfolio.buy(120)
    joined_portfolio = btc_portfolio + eth_portfolio
    print(joined_portfolio)
    print(f"Balance: {joined_portfolio.balance}")
    print(f"Trades: {list(joined_portfolio)}")

    # Context Manager Support
    joined_portfolio.export_trades()
