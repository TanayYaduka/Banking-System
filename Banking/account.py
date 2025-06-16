class BankAccount:

    account_counter = 1000
    def __init__(self, name, balance=0):
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.name = name
        self.__balance = balance

    def get_balance(self):
        return self.__balance
    
    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                print(f"Withdraw of {amount} successful. Remaining balance is {self.get_balance()}")
        else:
            print("Invalid amount. Please enter a positive number.")

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposit of {amount} successful. Remaining balance is {self.get_balance()}")
        else:
            print("Invalid amount. Please enter a positive number.")

    def display_balance(self):
        print(f"Account Number: {self.account_number}, Account Holder: {self.name}, Balance: {self.get_balance()}")

class SavingsAccount(BankAccount):
    def __init__(self, name, balance=0, interest_rate=0.05):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        months = int(input("How many months to calculate intrest"))
        interest = self.__balance * self.interest_rate * months
        self.deposit(interest)
        print(f"Interest of {interest} added to your account. Remaining balance is {self.get_balance()}")

class CurrentAccount(BankAccount):
    def __init__(self, name, balance=0, overdraft_limit=100000):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit
