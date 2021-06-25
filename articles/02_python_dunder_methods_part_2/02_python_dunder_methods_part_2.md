# Python Dunder Methods: Part 2

## Introduction

Welcome back, to the second part of the article about Python dunder methods. Let's continue our journey.

## Methods

### Operator Overloading for Comparing Portfolios

A lot of times there is a need to compare Python objects. If we try this with for example integers or strings is working out of the box.

```python
5 < 10
>> True

'a' > 'b'
>> False
```

This feels completely natural, but it’s actually quite amazing what happens behind the scenes. This is possible because the object implements one or more comparison dunder methods (`__eq__`, `__gt__` ...).

We can list these methods with the dir() function:

```python
dir(3)

>> ... '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', 
'__ge__', '__getattribute__', '__getnewargs__', '__gt__',...
```

Let's now compare our two `CryptoPortfolio` objects.

```python
btc_portfolio = CryptoPortfolio("bitcoin")
eth_portfolio = CryptoPortfolio("ethereum", amount=80)
btc_portfolio.buy(100)
print(btc_portfolio > eth_portfolio)

>> TypeError: '>' not supported between instances of 'CryptoPortfolio' 
and 'CryptoPortfolio'
```

We got a TypeError because we have not implemented any comparison dunder methods nor inherited them from a parent class.

Let's implement the need dunder methods. Because we don't want to implement all of the comparison dunder methods, we can use the `functools.total_ordering` decorator. This decorator allows us to define all the comparison dunder methods with only implementing `__eq__` and `__lt__`.

```python
from functools import total_ordering

@total_ordering
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""

	# ...

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance
```

And now we can compare `CryptoPortfolio` instances:

```python
if __name__ == "__main__":

    btc_portfolio = CryptoPortfolio("bitcoin")
    eth_portfolio = CryptoPortfolio("ethereum", amount=80)
    btc_portfolio.buy(100)

    print(btc_portfolio > eth_portfolio)
    print(btc_portfolio < eth_portfolio)
    print(btc_portfolio == eth_portfolio)
    print(btc_portfolio != eth_portfolio)

>> True
>> False
>> False
>> True
```

### Operator Overloading for Adding Portfolios

In Python, everything is an object. So we are completely fine adding two objects. But first, we need to implement the `__add__` method to be able to merge two portfolios.

```python
@total_ordering
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""

		# ...
		def __add__(self, other):
        coin = f"{self.coin}&{other.coin}"
        start_amount = self.amount + other.amount
        portfolio = CryptoPortfolio(coin, start_amount)
        for t in list(self) + list(other):
            portfolio.buy(t)
        return portfolio
```
It's a little more complicated than the other methods do far. But it should do exactly we expect:

```python
if __name__ == "__main__":
		btc_portfolio = CryptoPortfolio("bitcoin")
    eth_portfolio = CryptoPortfolio("ethereum", amount=80)

    btc_portfolio.buy(100)
    btc_portfolio.buy(20)
    btc_portfolio.sell(30)
    eth_portfolio.buy(120)

    joined_portfolio = btc_portfolio + eth_portfolio
    print(joined_portfolio)
    print(f"Balance: {joined_portfolio.balance}")
    print(f"Trades: {list(joined_portfolio)}")

>> Portfolio for bitcoin&ethereum with starting amount: 80
>> Balance: 290
>> Trades: [100, 20, -30, 120]
```

### Context Manager Support

Let's use context manager support to export our trades into a text file. We can leverage the Pythonic with statement by adding two more dunder methods.

```python
@total_ordering
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""
		
    # ...

    def __enter__(self):
        self.file = open("trades.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc_vals, exc_tb):
        self.file.close()

    def export_trades(self):
        with self as file:
            for trade in self:
                file.write(f"{trade}\n")
```

We can export our trades like this.

```python
if __name__ == "__main__":

    # ...

    joined_portfolio.export_trades()
```

After running this code, a file should be created in your working directory.

## Conclusion

That's it. You should now know how to use the most common dunder methods in Python.

You can find the final code example for the second part [here](https://github.com/whiletrue-community/website-articles/blob/main/articles/02_python_dunder_methods_part_2/02_python_dunder_methods_part_2.py).

See you next time! A new post is coming in 14 days.