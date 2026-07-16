# Personal Finance Manager
# OOP concepts: Abstraction, Encapsulation, Inheritance, Polymorphism

import json
import os
from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self, amount, description, category):
        self._amount = amount
        self._description = description
        self._category = category

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def signed_amount(self):
        pass

    def show(self):
        sign = "+" if self.signed_amount() > 0 else "-"
        print(f"[{self.get_type()}] {sign}Rs {abs(self._amount):,.0f} | {self._category} | {self._description}")


class Income(Transaction):
    def get_type(self):
        return "INCOME"

    def signed_amount(self):
        return +self._amount


class Expense(Transaction):
    def get_type(self):
        return "EXPENSE"

    def signed_amount(self):
        return -self._amount


class Saving(Transaction):
    def __init__(self, amount, goal, category):
        super().__init__(amount, f"Goal: {goal}", category)
        self._goal = goal

    def get_type(self):
        return "SAVING"

    def signed_amount(self):
        return -self._amount


class Account:
    def __init__(self, name):
        self.__name = name
        self.__transactions = []
        self.__budgets = {}
        self.__file = name.lower() + "_data.json"
        self.__load()

    @property
    def balance(self):
        return sum(t.signed_amount() for t in self.__transactions)

    def add(self, transaction):
        self.__transactions.append(transaction)
        self.__save()
        print("Saved!")

    def set_budget(self, category, limit):
        self.__budgets[category] = limit
        self.__save()
        print(f"Budget set: {category} = Rs {limit:,.0f}")

    def check_budget(self, category):
        spent = sum(t._amount for t in self.__transactions if isinstance(t, Expense) and t._category == category)
        limit = self.__budgets.get(category, 0)
        return spent, limit

    def show_all(self):
        if not self.__transactions:
            print("No transactions yet.")
            return
        for t in self.__transactions:
            t.show()

    def show_report(self):
        income = sum(t._amount for t in self.__transactions if isinstance(t, Income))
        expense = sum(t._amount for t in self.__transactions if isinstance(t, Expense))
        saving = sum(t._amount for t in self.__transactions if isinstance(t, Saving))

        print(f"\nFinancial Report for {self.__name}")
        print(f"Income:  Rs {income:,.0f}")
        print(f"Expense: Rs {expense:,.0f}")
        print(f"Savings: Rs {saving:,.0f}")
        print(f"Balance: Rs {self.balance:,.0f}")

    def __save(self):
        data = [{"kind": t.get_type(), "amount": t._amount,
                 "description": t._description, "category": t._category}
                for t in self.__transactions]
        with open(self.__file, "w") as f:
            json.dump({"budgets": self.__budgets, "transactions": data}, f, indent=2)

    def __load(self):
        if not os.path.exists(self.__file):
            return
        with open(self.__file, "r") as f:
            data = json.load(f)
        self.__budgets = data.get("budgets", {})
        for item in data.get("transactions", []):
            kind = item["kind"]
            if kind == "INCOME":
                t = Income(item["amount"], item["description"], item["category"])
            elif kind == "EXPENSE":
                t = Expense(item["amount"], item["description"], item["category"])
            else:
                t = Saving(item["amount"], item["description"], item["category"])
            self.__transactions.append(t)


class FinanceApp:
    INCOME_CATS = ["Salary", "Freelance", "Business", "Gift", "Other"]
    EXPENSE_CATS = ["Food", "Transport", "Shopping", "Utilities", "Health", "Education", "Entertainment", "Other"]

    def __init__(self):
        self.account = None

    def run(self):
        print("PERSONAL FINANCE MANAGER")
        name = input("Your name: ").strip() or "User"
        self.account = Account(name)
        print(f"Hello {name}! Balance: Rs {self.account.balance:,.0f}")
        self.menu()

    def menu(self):
        while True:
            print(f"""
Balance: Rs {self.account.balance:,.0f}
1. Add Income
2. Add Expense
3. Add Saving Goal
4. View All Transactions
5. View Report
6. Set Budget
7. Check Budget
8. Exit""")
            choice = input("Choose (1-8): ").strip()

            if choice == "1": self.add_income()
            elif choice == "2": self.add_expense()
            elif choice == "3": self.add_saving()
            elif choice == "4": self.account.show_all()
            elif choice == "5": self.account.show_report()
            elif choice == "6": self.set_budget()
            elif choice == "7": self.check_budget()
            elif choice == "8":
                print("Goodbye! Data saved.")
                break
            else:
                print("Invalid choice.")

    def add_income(self):
        amount = self.get_number("Amount (Rs): ")
        cat = self.pick_category(self.INCOME_CATS)
        desc = input("Description: ").strip() or "Income"
        self.account.add(Income(amount, desc, cat))

    def add_expense(self):
        amount = self.get_number("Amount (Rs): ")
        cat = self.pick_category(self.EXPENSE_CATS)
        desc = input("Description: ").strip() or "Expense"
        self.account.add(Expense(amount, desc, cat))
        spent, limit = self.account.check_budget(cat)
        if limit > 0:
            pct = (spent / limit) * 100
            if pct > 100:
                print(f"WARNING: Over budget for {cat}! ({pct:.0f}% used)")
            elif pct > 80:
                print(f"Caution: {pct:.0f}% of {cat} budget used.")

    def add_saving(self):
        goal = input("Goal name (e.g. Laptop): ").strip() or "Savings"
        amount = self.get_number("Amount to save (Rs): ")
        self.account.add(Saving(amount, goal, "Savings"))

    def set_budget(self):
        cat = self.pick_category(self.EXPENSE_CATS)
        limit = self.get_number(f"Monthly limit for {cat} (Rs): ")
        self.account.set_budget(cat, limit)

    def check_budget(self):
        cat = self.pick_category(self.EXPENSE_CATS)
        spent, limit = self.account.check_budget(cat)
        if limit == 0:
            print(f"No budget set for {cat}. Use option 6 first.")
            return
        pct = (spent / limit) * 100
        status = "OVER BUDGET!" if pct > 100 else "OK"
        print(f"{cat}: {pct:.0f}% used ({status})")
        print(f"Limit: Rs {limit:,.0f} | Spent: Rs {spent:,.0f} | Left: Rs {limit - spent:,.0f}")

    def get_number(self, prompt):
        while True:
            try:
                val = float(input(prompt))
                if val > 0:
                    return val
                print("Enter a positive number.")
            except ValueError:
                print("Numbers only please.")

    def pick_category(self, cats):
        for i, c in enumerate(cats, 1):
            print(f"  {i}. {c}")
        while True:
            try:
                idx = int(input(f"Choose (1-{len(cats)}): ")) - 1
                if 0 <= idx < len(cats):
                    return cats[idx]
            except ValueError:
                pass
            print("Invalid.")


if __name__ == "__main__":
    app = FinanceApp()
    app.run()
