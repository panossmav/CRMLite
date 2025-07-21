import sqlite3 as sql
import hashlib
import sys
import os
import csv
import datetime

conn = sql.connect('database.db')

cursor=conn.cursor()

with open('commands.sql', "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)
conn.commit()

def create_logs(u,act):
    cursor.execute(
        "INSERT INTO user_logs (user, action, dateandtime) VALUES (?,?,?)",(u,act,datetime.now())
    )

def check_phone(p):
    find_cust=cursor.execute(
        "SELECT FROM customers WHERE phone = ?",(p,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False
    
def check_email(e):
    find_cust=cursor.execute(
        "SELECT FROM customers WHERE email = ?",(e,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False

def check_vat(v):
    find_cust=cursor.execute(
        "SELECT FROM customers WHERE vat = ?",(v,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False
    
def new_customer(n,p,e,a,v,user):
    if check_phone(p) == False and check_email(e) == False and check_vat(v) == False:
        cursor.execute(
            "INSERT INTO customers (name,phone,email,adress,vat) VALUES (?,?,?,?,?)",(n,p,e,a,v)
        )
        create_logs(user,f"Created user (Phone {p}, Name {n})")
        return 'Ο πελάτης προστέθηκε'
    else:
        return 'Σφάλμα! υπάρχει πελάτης με αυτά τα στοιχεία'

def delete_customer_phone(p,user):
    if check_phone(p) == True:
        cursor.execute(
            "DELETE FROM customers WHERE phone=?",(p,)
        )
        create_logs(user,f"Delete user (Phone: {p})")
        return 'Ο πελάτης διαγράφηκε'
    else:
        return 'Σφάλμα! Δεν βρέθηκε πελάτης'

def delete_customer_vat(v,user):
    if check_vat(v) == True:
        cursor.execute(
            "DELETE FROM customers WHERE vat=?",(v,)
        )
        create_logs(user,f"Delete user (VAT: {v})")
        return 'Ο πελάτης διαγράφηκε'
    else:
        return 'Σφάλμα! Δεν βρέθηκε πελάτης' 

def modify_customer_phone(p,n_n,n_p,n_e,n_a,n_v):
    find_cust = cursor.execute(
        "SELECT * FROM customers WHERE phone = ?",(p,)
    )
    if find_cust:
        single_cust = find_cust.fetchone()
        if not n_n:
            n_n = single_cust[0]
        if not n_p:
            n_p = p
        if not n_e:
            n_e = single_cust[2]
        if not n_a:
            n_a = single_cust[3]
        if not n_v:
            n_v = single_cust[4]
        

