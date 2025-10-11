class BackAccount:
    def __init__(self, first_name, last_name, balance=0):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Not enough funds!")
        else:
            self.balance -= amount
            print(f"Withdrawn {amount}. Balance: {self.balance}")

    def __repr__(self):
        return f"{self.first_name} {self.last_name} {self.balance}"

account1 = BackAccount('Mohamad', 'abbasi')

print(account1.balance)
print(account1)

account1.deposit(100)
account1.withdraw(12)

