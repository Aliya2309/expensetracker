from tkinter import *
import sqlite3 as db
from datetime import datetime
import matplotlib.pyplot as plt
root = Tk()
root.title('Expense tracker!!')
root.geometry('400x400')
root.configure(bg='pink')

def init():
    '''
    Initialize a new database to store the
    expenditures
    '''
    conn = db.connect("spent.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql)
    conn.commit()

def submit(a_label, t_label, o_label):
    amount = a_label.get()
    category = t_label.get()
    message = o_label.get()
    date = str(datetime.now())
    data = (amount, category, message, date)
    print(data)
    conn = db.connect('spent.db')

    cur = conn.cursor()
    # insert into table
    sql = ('INSERT INTO expenses VALUES (?, ?, ?, ?)')

    cur.execute(sql,data)
    # commit changes
    conn.commit()
    # close database
    conn.close()

    #clear the text boxes
    a_label.delete(0,END)
    t_label.delete(0, END)
    o_label.delete(0, END)



def popup():
    #creating pop-up window
    root = Tk()
    root.title('Expense Tracker')
    root.geometry('400x400')
    root.configure(bg='cyan')






    # creating text boxes
    a_label_name = Label(root, text='Enter the amount spent:', bg='cyan')
    a_label_name.grid(row=0, column=0, columnspan=1, padx=20, pady=20)
    a_label = Entry(root, width=30)
    a_label.grid(row=0, column=1, columnspan=2)
    t_label_name = Label(root, text='Type of expense:', bg='cyan')
    t_label_name.grid(row=1, column=0, columnspan=1)
    t_label = Entry(root, width=30)
    t_label.grid(row=1, column=1, columnspan=2, pady=20)
    o_label_name = Label(root, text='Optional Message:', bg='cyan')
    o_label_name.grid(row=2, column=0, columnspan=1)
    o_label = Entry(root, width=30)
    o_label.grid(row=2, column=1, columnspan=2)
    s_button = Button(root, text='Submit', command=lambda:submit(a_label, t_label,o_label))
    s_button.grid(row=3, column=1, columnspan=2, pady=20)

    root.mainloop()

def view(t, category=None):

       #Returns a list of all expenditure incurred, and the total expense.
       #If a category is specified, it only returns info from that
       #category

    conn = db.connect("spent.db")
    cur = conn.cursor()
    if category:
        sql = '''
           select amount from expenses where category = '{}'
           '''.format(category)
        sql3 = '''
           select category from expenses where category = '{}'
           '''.format(category)
        sql4 = '''
           select message from expenses where category = '{}'
           '''.format(category)
        sql5 = '''
           select date from expenses where category = '{}'
           '''.format(category)
        sql6 = '''
           select * from expenses where category='{}'
           '''.format(category)
        sql2 = '''
           select sum(amount) from expenses where category = '{}'
           '''.format(category)
    else:
        sql = '''
           select amount from expenses
           '''.format(category)
        sql3 = '''
                   select category from expenses
                   '''.format(category)
        sql4 = '''
                   select message from expenses
                   '''.format(category)
        sql5 = '''
                   select date from expenses
                   '''.format(category)
        sql2 = '''
           select sum(amount) from expenses
           '''.format(category)
        sql6 = '''
                   select * from expenses
                   '''.format(category)
    cur.execute(sql)
    amounts = [item[0] for item in cur.fetchall()]
    cur.execute(sql3)
    cats = [item[0] for item in cur.fetchall()]
    cur.execute(sql4)
    msgs = [item[0] for item in cur.fetchall()]
    cur.execute(sql5)
    dates = [item[0] for item in cur.fetchall()]
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    cur.execute(sql6)
    all = cur.fetchall()
    if t == 1:
        return [amounts, cats, msgs, dates, total_amount]
    elif t == 2:
        return all




def viewlist():
    root =Tk()
    root.geometry('500x500')
    root.title('Expense tracker')
    root.configure(bg='magenta')
    data1 = view(2)
    data1.insert(0,('amount','category','message','date'))
    for i in range(len(data1)):
        for j in range(4):
            b = Entry(root, text=data1[i][j])
            b.grid(row=i, column=j)
            b.insert(END,data1[i][j])
            print(data1[i][j])
    root.mainloop()


def data_chart():
    data2 = view(1)
    print(data2)
    labels = ["Food", "Travel", "Bills", "Charity", "Clothing/Toiletries", "Others", "Savings"]
    sizes = [0, 0, 0, 0, 0, 0, 10000 - data2[4]]
    print(len(data2[1]))
    for i in range(len(data2[1])):
        if data2[1][i] == "Food":
            sizes[0] = sizes[0] + data2[0][i]
            continue
        if data2[1][i] == "Travel":
            sizes[1] = sizes[1] + data2[0][i]
            continue
        if data2[1][i] == "Bills":
            sizes[2] = sizes[2] + data2[0][i]
            continue
        if data2[1][i] == "Charity":
            sizes[3] = sizes[3] + data2[0][i]
            continue
        if data2[1][i] == "Clothing" or data2[1][i] == "Toiletries":
            sizes[4] = sizes[4] + data2[0][i]
            continue
        else:
            print("here", data2[0][i])
            sizes[5] = sizes[5] + int(data2[0][i])
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def viewdata():
    root = Tk()
    root.title('Expense tracker')
    root.geometry('200x200')
    root.configure(bg='#856ff8')
    list_btn = Button(root, text='View list', command=viewlist)
    list_btn.grid(row=0, column=0, columnspan=3, padx=70, pady=30)
    chart_btn = Button(root, text='View Chart', command=data_chart)
    chart_btn.grid(row=1, column=0, columnspan=3)
    root.mainloop()

txt = Label(root, text='EXPENSE TRACKER', fg='red', bg='pink', font='ComicSans 20 bold')
txt.grid(row=0, column=0, padx=50, pady=50)
e_button= Button(root, text='Enter data', command=popup)
e_button.grid(row=1, column=0, columnspan=3)
v_button= Button(root, text="View data", command=viewdata)
v_button.grid(row=2, column=0, columnspan=3, pady=20)



root.mainloop()