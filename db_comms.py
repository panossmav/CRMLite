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
    conn.commit()

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
        conn.commit()
        create_logs(user,f"Created user (Phone {p}, Name {n})")
        return 'Ο πελάτης προστέθηκε'
    else:
        return 'Σφάλμα! υπάρχει πελάτης με αυτά τα στοιχεία'

def delete_customer_phone(p,user):
    if check_phone(p) == True:
        cursor.execute(
            "DELETE FROM customers WHERE phone=?",(p,)
        )
        conn.commit()
        create_logs(user,f"Delete user (Phone: {p})")
        return 'Ο πελάτης διαγράφηκε'
    else:
        return 'Σφάλμα! Δεν βρέθηκε πελάτης'

def delete_customer_vat(v,user):
    if check_vat(v) == True:
        cursor.execute(
            "DELETE FROM customers WHERE vat=?",(v,)
        )
        conn.commit()
        create_logs(user,f"Delete user (VAT: {v})")
        return 'Ο πελάτης διαγράφηκε'
    else:
        return 'Σφάλμα! Δεν βρέθηκε πελάτης' 

def modify_customer_phone(p,n_n,n_p,n_e,n_a,n_v,user):
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
        cursor.execute(
            "UPDATE customers SET name = ?, phone = ?, email = ?, address = ?, vat = ?",(n_n,n_p,n_e,n_a,n_v)
            )
        conn.commit()
        create_logs(user,f"Update customer: {single_cust[5]}")

def create_prod(t,p,s,u):
    cursor.execute(
        "INSERT INTO products (title, price, stock) VALUES (?, ?, ?)",(t,p,s)
    )
    conn.commit()
    create_logs(u,f"Create product {t}")

def find_prod(sku):
    fetch = cursor.execute(
        "SELECT * FROM products WHERE sku = ?",(sku,)
    )
    if fetch:
        return True
    else:
        return False

def modify_prod(n_t,n_p,n_s,sku,u):
    if find_prod(sku) == True:
        fetch_prod = cursor.execute(
            "SELECT * FROM products WHERE sku = ?",(sku,)
        )
        prod = fetch_prod.fetchone()
        if not n_t:
            n_t = prod[0]
        if not n_p:
            n_p = prod[1]
        if not n_s:
            n_s = prod[2]
        cursor.execute(
            "UPDATE products SET title = ?, price = ?, stock = ?",(n_t,n_p,n_s)
        )
        conn.commit()
        fetch_upd_prod = cursor.execute(
            "SELECT * FROM products WHERE sku = ?",(sku)
        )
        upd_prod = fetch_upd_prod.fetchone()
        create_logs(u,f"Update product {sku}")
        return f"Νέα στοιχεία προϊόντος:\n Τίτλος: {upd_prod[0]} \n Τιμή: {upd_prod[1]}€ \n Απόθεμα {upd_prod[2]} \n SKU: {upd_prod[3]}"
    else:
        return f"Δεν βρέθηκε αυτό το προϊόν!"

def create_order(c_p,p_s,u):
    fetch_customers = cursor.execute(
        "SELECT * FROM customers WHERE phone = ?",(c_p,)
    )
    customer = fetch_customers.fetchone()
    fetch_products = cursor.execute(
        "SELECT * FROM products WHERE sku = ?",(p_s,)
    )
    product = fetch_products.fetchone()
    if customer:
        if product:
            cursor.execute(
                "INSERT INTO orders (cust_name, cust_phone, prod_sku, prod_title, price) VALUES (?, ?, ?, ?, ?)",(customer[0],c_p,p_s,product[0],product[1])
            )
            order_id = cursor.lastrowid
            conn.commit()
            create_logs(u,f"Create order {order_id}")
            return f"Η παραγγελία με αριθμό {order_id} δημιουργήθηκε!"
        else:
            return f"Σφάλμα! Ο κωδικός προϊόντος δεν υπάρχει"
    else:
        return f"Σφάλμα! ο πελάτης δεν υπάρχει"



