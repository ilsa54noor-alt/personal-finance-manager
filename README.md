# personal-finance-manager
A Python OOP-based personal finance tracker — group project (OOP Lab, UET Taxila)

## What it does
- Add, view, and categorize income, expenses, and savings goals
- Set monthly budgets per category and get over-budget warnings
- Generate a financial summary report (income, expenses, savings, balance)
- Saves data locally to a JSON file, so nothing is lost between runs

## OOP concepts applied
- **Abstraction** — `Transaction` is an abstract base class defining the shared interface
- **Inheritance** — `Income`, `Expense`, and `Saving` all inherit from `Transaction`
- **Polymorphism** — the same `show()` method behaves differently depending on the transaction type
- **Encapsulation** — `Account` keeps transaction and budget data private, exposed only through controlled methods

## Tools used
Python 3.x · JSON for data storage · (optional) Matplotlib for future visualization

## Team
Group project — OOP Lab, submitted July 2026
- **Ilsa Noor** — Design & Planning
- Memoona Rizwan — Coding (Classes & Functions)
- Imtesaal Noor — Testing & Debugging
- Haleema Sadia Khalid — Documentation & Report Writing
- Zainab Eman — Presentation Preparation

## How to run
```bash
python finance_manager.py
```
