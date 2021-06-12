# Python Dunder Methods: Part 1

## 

In this article, we will look at how to use Python magic methods. In Python, a class have special methods that are invoked by special syntax. These methods are called **dunder methods** or **magic methods**. Dunder here means Double Under (Underscores). This set of predefined methods help you enrich your classes. Every Python class inherits these methods, and you can override them to modify their behaviour. They are easy to recognize because they start and end with double underscores, for example, `__init__`,  `__add__`, `__len__`. 

Dunder methods let you emulate the behaviour of built-in types. For representing how these special methods work we will write a `CryptoPortfolio` class, that would help us track the trades for a selected coin.

## Methods

### Initialization

Firstly we will look at the `__init__` constructor. The `__init__` method for initialization is invoked without any call, when an instance of a class is created. In the following example, we use this method to construct portfolio objects from the `CryptoPortfolio` class.

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""

    def __init__(self, coin: str, amount: int = 0) -> None:
        """
        This constructor lets us create objects from this class.
        """
        self.coin = coin
        self.amount = amount
        self._trades = []
```

The constructor takes care of setting up the object. It receives the coin name and an optional initial amount of the coin. We define an internal list `_trades` to keep track of all the trades.

We can instantiate a new porfolio like this:

```python
if __name__ == "__main__":
    btc_portfolio = CryptoPortfolio('bitcoin')
    eth_portfolio = CryptoPortfolio('ethereum', amount=80)
```

### Representation

It would be nice to add a string representation for our object. There are two ways how to do this using dunder methods in Pytohn.

1. `__repr__`: The “official” string representation of an object. This is how you would make an object of the class. The goal of `__repr__`is to be unambiguous.
2. `__str__`: The “informal” or nicely printable string representation of an object. This is for the enduser.

Let’s implement these methods in our `CryptoPortfolio` class:

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""

    # ...

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coin}, {self.amount})"

    def __str__(self):
        return f"Portfolio for {self.coin} with starting amount: {self.amount}"
```

We used `self.__class__.__name__` to access the class name programmatically.  Make sure you implement at least the `__repr__` method. Let's look at the result:

```python
if __name__ == "__main__":
    # ...

    print(btc_portfolio)
    print(eth_portfolio)
    print(repr(btc_portfolio))
    print(repr(eth_portfolio))
--
>> Portfolio for bitcoin with starting amount: 0
>> Portfolio for ethereum with starting amount: 80
>> CryptoPortfolio(bitcoin, 0)
>> CryptoPortfolio(ethereum, 80)
```

### Iteration

In order to iterate over our trades, we need first to add them. We can do that by adding two simple methods (buy & sell). We will also add a property to calculate the current portfolio value.

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""
		
		# ...
   
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
```

Let's do some crypto transactions:

```python
if __name__ == "__main__":
    btc_portfolio = CryptoPortfolio("bitcoin", amount=100)
    btc_portfolio.buy(100)
    btc_portfolio.sell(50)
    btc_portfolio.sell(40)
    btc_portfolio.buy(390)
    print(btc_portfolio.balance)

--
>> 500
```

How many trades we made? Maybe we can check it with the `len()` function.

```python
>> print(len(btc_portfolio))
TypeError: object of type 'CryptoPortfolio' has no len()
```

Unfortunately is not working. We just need another dunder method to make it work. The `__len__`

method!

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""
		
		# ...

		def __len__(self):
        return len(self._trades)

if __name__ == "__main__":
    btc_portfolio = CryptoPortfolio("bitcoin", amount=100)
    btc_portfolio.buy(100)
    btc_portfolio.sell(50)
    btc_portfolio.sell(40)
    btc_portfolio.buy(390)
    print(btc_portfolio.balance)
    print(len(btc_portfolio))

>> 500
>> 4
```

The `len()` function works! We can proceed with the next step. It only takes a little bit of code to make the class iterable:

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""
		
		# ...

		def __getitem__(self, position):
            return self._trades[position]
```

Now it works:

```python
if __name__ == "__main__":
    btc_portfolio = CryptoPortfolio("bitcoin", amount=100)
    btc_portfolio.buy(100)
    btc_portfolio.sell(50)
    btc_portfolio.sell(40)
    btc_portfolio.buy(390)

    for trade in btc_portfolio:
        print(trade)

    print(f"First trade: {btc_portfolio[0]}")

>> 100
>> -50
>> -40
>> 390
>> First trade: 100
```

To iterate over in the reverse order we need to add the `__reverse__` **special method.

```python
class CryptoPortfolio:
    """A simple crypto portfolio tracker class."""
		
		# ...

		def __reversed__(self):
            return self[::-1]

if __name__ == "__main__":
    btc_portfolio = CryptoPortfolio("bitcoin", amount=100)
    btc_portfolio.buy(100)
    btc_portfolio.sell(50)
    btc_portfolio.sell(40)
    btc_portfolio.buy(390)

    print(f"Trades reversed: {list(reversed(btc_portfolio))}")

>> Trades reversed: [390, -40, -50, 100]
```

Our `CryptoPortfolio` class is now looking pretty nice.

There are some more dunder methods we will look at in the next part.

You can find the final code example for the first part here ([https://github.com/whiletrue-community/website-articles/blob/main/articles/01_python_dunder_methods_part_1.py](https://github.com/whiletrue-community/website-articles/blob/main/articles/01_python_dunder_methods_part_1.py)).

See you next time! Part 2 is coming in 14 days.

Sources:

- [Enriching Your Python Classes With Dunder (Magic, Special) Methods]([https://dbader.org/blog/python-dunder-methods](https://dbader.org/blog/python-dunder-methods))
- [Python Dunder Methods]([https://dbader.org/blog/python-dunder-method](https://levelup.gitconnected.com/python-dunder-methods-ea98ceabad15))