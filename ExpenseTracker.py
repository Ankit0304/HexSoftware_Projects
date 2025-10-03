import datetime as dt
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

connection = sqlite3.connect("Finance.db")
cursor = connection.cursor()
connection.execute(
    'CREATE TABLE IF NOT EXISTS Finance (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,Date DATETIME, Category TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)
connection.commit()

root = Tk()
root.title('Personal Finance Tracker')
root.geometry('1000x700')

desc = StringVar()
amnt = DoubleVar()
category = StringVar()
MoP = StringVar(value='Cash')

main_frame = Frame(root, bg="#f7fafc")
main_frame.pack(fill=BOTH, expand=True)

title_frame = Frame(main_frame, bg="#3867d6", height=50)
title_frame.pack(fill=X, side=TOP)
Label(title_frame, text='Personal Finance Tracker', font=('Segoe UI', 20, 'bold'), fg="#fff", bg="#3867d6").pack(padx=10, pady=10)

content_frame = Frame(main_frame, bg="#f7fafc")
content_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

left_frame = LabelFrame(content_frame, text="Add / Edit Expense", bg="#f7fafc", font=('Segoe UI', 13, 'bold'), width=330, relief=RIDGE)
left_frame.pack(side=LEFT, fill=Y, padx=(0,12), pady=2)

Label(left_frame, text='Date:', bg="#f7fafc", font=('Segoe UI', 11)).pack(anchor='w', padx=12, pady=(18,2))
date = DateEntry(left_frame, date=dt.datetime.now().date(), font=('Segoe UI', 11))
date.pack(fill=X, padx=12, pady=2)

Label(left_frame, text='Category:', bg="#f7fafc", font=('Segoe UI', 11)).pack(anchor='w', padx=12, pady=(10,2))
Entry(left_frame, font=('Segoe UI', 11), textvariable=category).pack(fill=X, padx=12, pady=2)

Label(left_frame, text='Description:', bg="#f7fafc", font=('Segoe UI', 11)).pack(anchor='w', padx=12, pady=(10,2))
Entry(left_frame, font=('Segoe UI', 11), textvariable=desc).pack(fill=X, padx=12, pady=2)

Label(left_frame, text='Amount:', bg="#f7fafc", font=('Segoe UI', 11)).pack(anchor='w', padx=12, pady=(10,2))
Entry(left_frame, font=('Segoe UI', 11), textvariable=amnt).pack(fill=X, padx=12, pady=2)

Label(left_frame, text='Payment Mode:', bg="#f7fafc", font=('Segoe UI', 11)).pack(anchor='w', padx=12, pady=(10,2))
OptionMenu(left_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'UPI']).pack(fill=X, padx=12, pady=2)

entry_btn_frame = Frame(left_frame, bg="#f7fafc")
entry_btn_frame.pack(fill=X, padx=12, pady=18)

def clear_fields():
    today_date = dt.datetime.now().date()
    desc.set('')
    category.set('')
    amnt.set(0.0)
    MoP.set('Cash')
    date.set_date(today_date)
    table.selection_remove(*table.selection())
    update_total_transaction()
    
add_expense_btn = Button(entry_btn_frame, text="Add Expense", command=lambda: add_another_expense(), font=('Segoe UI', 11), bg="#20bf6b", fg="white", relief=FLAT)
add_expense_btn.pack(fill=X, pady=2)

Button(entry_btn_frame, text="Clear Fields", command=clear_fields, font=('Segoe UI', 11), bg="#5758bb", fg="white", relief=FLAT).pack(fill=X, pady=2)

total_amount_label = Label(left_frame, text="Total Transactions: ₹0.00", font=('Segoe UI', 12, 'italic'), bg="#f7fafc", fg="#3867d6")
total_amount_label.pack(pady=12, padx=12, anchor='w')

right_frame = Frame(content_frame, bg="#f7fafc")
right_frame.pack(side=LEFT, fill=BOTH, expand=True)

table_frame = Frame(right_frame, bg="#f7fafc", relief=GROOVE, bd=2)
table_frame.pack(fill=BOTH, expand=True, pady=(0,8))

table = ttk.Treeview(
    table_frame,
    columns=('ID', 'Date', 'Category', 'Description', 'Amount', 'Mode of Payment'),
    selectmode=BROWSE,
    show='headings',
    height=14
)
x_scroll = Scrollbar(table_frame, orient=HORIZONTAL, command=table.xview)
y_scroll = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
table.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
table.pack(fill=BOTH, expand=True)

table.heading('ID', text='S No.')
table.heading('Date', text='Date')
table.heading('Category', text='Category')
table.heading('Description', text='Description')
table.heading('Amount', text='Amount')
table.heading('Mode of Payment', text='Mode')

table.column('ID', width=70, anchor='center')
table.column('Date', width=100, anchor='center')
table.column('Category', width=110, anchor='center')
table.column('Description', width=230, anchor='center')
table.column('Amount', width=90, anchor='center')
table.column('Mode of Payment', width=110, anchor='center')

def reset_search():
    list_all_expenses() 

actions_frame = Frame(right_frame, bg="#f7fafc")
actions_frame.pack(fill=X, padx=5, pady=5)

Button(actions_frame, text="Edit", command=lambda: edit_expense(), font=('Segoe UI', 11), width=10, bg="#fd9644", fg="white", relief=FLAT).pack(side=LEFT, padx=3)
Button(actions_frame, text="Delete", command=lambda: remove_expense(), font=('Segoe UI', 11), width=10, bg="#eb3b5a", fg="white", relief=FLAT).pack(side=LEFT, padx=3)
Button(actions_frame, text="Delete All", command=lambda: remove_all_expenses(), font=('Segoe UI', 11), width=12, bg="#8854d0", fg="white", relief=FLAT).pack(side=LEFT, padx=3)
Button(actions_frame, text="Search Expenses", command=lambda: search_expenses_popup(), font=('Segoe UI', 11), bg="#3867d6", fg="white", relief=FLAT, width=17).pack(side=LEFT, padx=3)

utility_frame = Frame(right_frame, bg="#f7fafc")
utility_frame.pack(fill=X, padx=5, pady=3)

Button(utility_frame, text="Monthly Summary", command=lambda: monthly_summary(), font=('Segoe UI', 11), bg="#20bf6b", fg="white", relief=FLAT, width=17).pack(side=LEFT, padx=3)
Button(utility_frame, text="Export PDF", command=lambda: generate_transaction_pdf(), font=('Segoe UI', 11), bg="#fd9644", fg="white", relief=FLAT, width=17).pack(side=LEFT, padx=3)
Button(utility_frame, text="Show All Expenses", font=('Segoe UI', 11), bg="#3867d6", fg="white", relief=FLAT, width=17, command=reset_search).pack(side=LEFT, padx=3)

def list_all_expenses():
    try:
        table.delete(*table.get_children())
        all_data = connection.execute('SELECT * FROM Finance')
        data = all_data.fetchall()
        update_total_transaction()
        for values in data:
            table.insert('', END, values=values)
    except sqlite3.Error as e:
        mb.showerror('Database Error', f'An error occurred while listing expenses: {e}')

def view_expense_details():
    if not table.selection():
        mb.showerror('No Expense Selected', 'Please select an expense to view its details')
        return
    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']
    expenditure_date = dt.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
    date.set_date(expenditure_date)
    category.set(values[2])
    desc.set(values[3])
    amnt.set(values[4])
    MoP.set(values[5])
    update_total_transaction()

def remove_expense():
    if not table.selection():
        mb.showerror('No Record Selected!', 'Please select a record to delete!')
        return
    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']
    surety = mb.askyesno('Are you Sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')
    if surety:
        try:
            connection.execute('DELETE FROM Finance WHERE ID=?', (values_selected[0],))
            connection.commit()
            list_all_expenses()
            update_total_transaction()
            mb.showinfo('Record deleted successfully!', 'The record has been deleted successfully!')
        except sqlite3.Error as e:
            mb.showerror('Database Error', f'An error occurred while deleting the expense: {e}')

def remove_all_expenses():
    surety = mb.askyesno('Are you sure?', 'Are sure that you want to delete all the expense items from the database?', icon='warning')
    if surety:
        try:
            table.delete(*table.get_children())
            connection.execute('DELETE FROM Finance')
            connection.commit()
            clear_fields()
            list_all_expenses()
            update_total_transaction()
            mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
        except sqlite3.Error as e:
            mb.showerror('Database Error', f'An error occurred while deleting all expenses: {e}')
    else:
        mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

def add_another_expense():
    if not date.get() or not category.get() or not desc.get() or not amnt.get() or not MoP.get():
        mb.showerror('Fields Empty!', 'Please fill all the missing fields before pressing the add button!')
    else:
        try:
            connection.execute('INSERT INTO Finance(Date, Category, Description, Amount, ModeOfPayment) VALUES(?,?,?,?,?)',
                               (dt.datetime.strptime(date.get(), "%m/%d/%y").strftime("%Y-%m-%d"), category.get(), desc.get(), amnt.get(), MoP.get()))
            connection.commit()
            clear_fields()
            list_all_expenses()
            update_total_transaction()
            mb.showinfo('Expense added', 'The expense has been added to the database')
        except sqlite3.Error as e:
            mb.showerror('Database Error', f'An error occurred while adding the expense: {e}')

def edit_expense():
    global table, add_expense_btn

    if not table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return
    view_expense_details()

    def confirm_edit():
        current_selected_expense = table.item(table.focus())
        contents = current_selected_expense['values']
        try:
            connection.execute('UPDATE Finance SET Date = ?, Category = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                               (dt.datetime.strptime(date.get(), "%m/%d/%y").strftime("%Y-%m-%d"),
                                category.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
            connection.commit()
            clear_fields()
            list_all_expenses()
            update_total_transaction()
            mb.showinfo('Data edited', 'We have updated the data and stored it in the database as you wanted')
        except sqlite3.Error as e:
            mb.showerror('Database Error', f'An error occurred while editing the expense: {e}')
        add_expense_btn.config(text="Add Expense", command=lambda: add_another_expense(), bg="#20bf6b")
    add_expense_btn.config(text="Confirm Edit", command=confirm_edit, bg="#fd9644")

def selected_expenses_to_words():
    if not table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return
    current_selection_expense = table.item(table.focus())
    values = current_selection_expense['values']
    message = f'Your expense can be read like : \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'
    mb.showinfo('Here\'s how to read your expense', message)

def expense_to_words_before_adding():
    if not date or not desc or not category or not amnt or not MoP:
        mb.showerror('Incomplete data', 'The data is incomplete, fill all the fields first!')
        return
    message = f'Your expense can be read like this : \n "You Paid {amnt.get()} to {category.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'
    add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')
    if add_question:
        add_another_expense()
    else:
        mb.showinfo('Ok', 'Please take your time to add this record')

def generate_transaction_pdf():
    try:
        all_data = connection.execute('SELECT * FROM Finance')
        data = all_data.fetchall()
        if not data:
            mb.showinfo("No Transactions", "There are no transactions to print.")
            return
        file_name = "Transactions.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(200, 750, "Personal Finance Tracker - Transactions Report")
        c.drawString(50, 730, "--------------------------------------------------------")
        y_position = 710
        for record in data:
            transaction_text = f"ID: {record[0]}, Date: {record[1]}, Category: {record[2]}, Description: {record[3]}, Amount: {record[4]}, Mode: {record[5]}"
            c.drawString(50, y_position, transaction_text)
            y_position -= 20
            if y_position < 50: 
                c.showPage()
                c.setFont("Helvetica", 12)
        c.save()
        mb.showinfo("PDF Generated", f"Transactions saved as {file_name}")
    except Exception as e:
        mb.showerror('PDF Generation Error', f'An error occurred while generating the PDF: {e}')

def update_total_transaction():
    try:
        total = connection.execute('SELECT SUM(Amount) FROM Finance').fetchone()[0]
        total = total if total else 0 
        total_amount_label.config(text=f"Total Transactions: ₹{total:.2f}")
    except sqlite3.Error as e:
        mb.showerror('Database Error', f'An error occurred while updating the total transactions: {e}')

def search_expenses(keyword='', start_date=None, end_date=None):
    try:
        query = "SELECT * FROM Finance WHERE 1=1"
        params = []
        if keyword:
            query += " AND (Category LIKE ? OR Description LIKE ?)"
            keyword_param = f"%{keyword}%"
            params.extend([keyword_param, keyword_param])
        if start_date and end_date:
            query += " AND Date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        table.delete(*table.get_children())
        results = connection.execute(query, params).fetchall()
        for row in results:
            table.insert('', END, values=row)
        update_total_transaction()
    except sqlite3.Error as e:
        mb.showerror('Search Error', f'An error occurred while searching: {e}')

def search_expenses_popup():
    popup = Toplevel(root)
    popup.title("Search Expenses")
    popup.geometry("400x250")
    popup.configure(bg='light yellow')
    Label(popup, text="Keyword:", font=('Segoe UI', 11), bg='light yellow').place(x=20, y=20)
    keyword_var = StringVar()
    Entry(popup, textvariable=keyword_var, font=('Segoe UI', 11), width=30).place(x=120, y=20)
    Label(popup, text="Start Date:", font=('Segoe UI', 11), bg='light yellow').place(x=20, y=70)
    start_date = DateEntry(popup, font=('Segoe UI', 11))
    start_date.place(x=120, y=70)
    Label(popup, text="End Date:", font=('Segoe UI', 11), bg='light yellow').place(x=20, y=120)
    end_date = DateEntry(popup, font=('Segoe UI', 11))
    end_date.place(x=120, y=120)
    def run_search():
        search_expenses(keyword_var.get(), start_date.get_date(), end_date.get_date())
        popup.destroy()
    Button(popup, text="Search", font=('Segoe UI', 11), bg="#3867d6", fg="white", command=run_search).place(x=150, y=180)

def monthly_summary():
    try:
        summary = connection.execute("""
            SELECT strftime('%Y-%m', Date) AS Month, SUM(Amount)
            FROM Finance
            GROUP BY Month
            ORDER BY Month DESC
        """).fetchall()
        message = "\n".join([f"{month}: ₹{amount:.2f}" for month, amount in summary])
        mb.showinfo("Monthly Summary", message)
    except sqlite3.Error as e:
        mb.showerror("Summary Error", f'An error occurred while generating summary: {e}')
 
list_all_expenses()
update_total_transaction()
root.mainloop()
