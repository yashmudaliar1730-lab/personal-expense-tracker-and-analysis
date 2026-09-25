
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL
            )
        """)

def add_expense(date, category, amount):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
            (date, category, amount)
        )
    print(f"Added expense: ${amount} for {category}")

def generate_analytics():
    conn = sqlite3.connect(DB_NAME)
    # Read directly into Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        print("No expense data found!")
        return

    # Total spend by category
    category_summary = df.groupby("category")["amount"].sum()
    print("\n--- Summary by Category ---")
    print(category_summary)

    # Plot pie chart visualization
    category_summary.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Expense Distribution by Category")
    plt.ylabel("") # Hide y-label for clean display
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    init_db()
    
    # Sample data entry
    add_expense("2026-03-01", "Groceries", 45.50)
    add_expense("2026-03-02", "Utilities", 110.00)
    add_expense("2026-03-03", "Groceries", 32.10)
    add_expense("2026-03-04", "Entertainment", 25.00)

    generate_analytics()