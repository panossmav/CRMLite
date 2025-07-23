import sqlite3 as sql
import hashlib
import sys
import os
import csv
from datetime import datetime

conn = sql.connect('database.db')

cursor=conn.cursor()

with open('commands.sql', "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)
conn.commit()

def create_logs(u,act):
    fetch_users = cursor.execute(
        "SELECT real_name FROM users WHERE username = ?",(u,)
    )
    user = fetch_users.fetchone()
    if user:
        cursor.execute(
            "INSERT INTO user_logs (user, action, dateandtime) VALUES (?,?,?)",(user[0],act,datetime.now())
        )
        conn.commit()
    else:
        pass
def check_phone(p):
    find_cust=cursor.execute(
        "SELECT * FROM customers WHERE phone = ?",(p,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False
    
def check_email(e):
    find_cust=cursor.execute(
        "SELECT * FROM customers WHERE email = ?",(e,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False

def check_vat(v):
    find_cust=cursor.execute(
        "SELECT * FROM customers WHERE vat = ?",(v,)
    )
    fetch = find_cust.fetchone()
    if fetch:
        return True
    else:
        return False
    
def new_customer_back(n,p,e,a,v,user):
    if check_phone(p) == False and check_email(e) == False and check_vat(v) == False:
        cursor.execute(
            "INSERT INTO customers (name,phone,email,address,vat) VALUES (?,?,?,?,?)",(n,p,e,a,v)
        )
        cust_id = cursor.lastrowid
        conn.commit()
        create_logs(user,f"Created user (Phone {p}, Name {n})")
        return 'Ο πελάτης προστέθηκε',cust_id
    else:
        return 'Σφάλμα! υπάρχει πελάτης με αυτά τα στοιχεία',cust_id

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
                "INSERT INTO orders (cust_name, cust_phone, prod_sku, prod_title, price, date_time) VALUES (?, ?, ?, ?, ?, ?)",(customer[0],c_p,p_s,product[0],product[1],datetime.now())
            )
            order_id = cursor.lastrowid
            if product[2] !=0:
                cursor.execute(
                    "UPDATE products SET stock = ? WHERE sku = ?",(product[2]-1,p_s)
                )
            conn.commit()
            create_logs(u,f"Create order {order_id}")
            return f"Η παραγγελία με αριθμό {order_id} δημιουργήθηκε!"
        else:
            return f"Σφάλμα! Ο κωδικός προϊόντος δεν υπάρχει"
    else:
        return f"Σφάλμα! ο πελάτης δεν υπάρχει"


def find_order(o_n):
    fetch = cursor.execute(
        "SELECT * FROM orders WHERE order_id = ?",(o_n)
    )
    order = fetch.fetchone()
    return order

def search_order(o_n):
    order = find_order(o_n)
    if order:
        return f"Κωδικός παραγγελίας {order[6]} \n Όνομα πελάτη: {order[0]} \n Τηλέφωνο πελάτη: {order[1]} \n Κωδικός προϊόντος: {order[2]} \n Τίτλος προϊόντος:{order[3]} \n Τιμή: {order[4]}€ \n Κατάσταση: {order[5]} \n Ημερομηνία / ώρα: {order[7]}"
    else:
        return f"Δεν βρέθηκε παραγγελία με αυτόν τον αριθμό"

def modify_order_status(o_n,u,n_s):
    order = find_order(o_n)
    if order:
        cursor.execute(
            "UPDATE orders SET status = ?",(n_s,)
        )
        conn.commit()
        create_logs(u,f"Modify order {order[5]} status to {n_s}")
        return f"Η κατάσταση παραγγελίας άλλαξε σε {n_s}"
    else:
        return f"Η παραγγελία δεν βρέθηκε"

def total_net():
    fetch_orders = cursor.execute(
        "SELECT SUM(price) FROM orders"
    )
    t_net = fetch_orders.fetchone()
    return t_net

def total_customers():
    fetch_customers = cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )
    result = fetch_customers.fetchone()
    return result

def total_orders():
    fetch_orders = cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )
    res = fetch_orders.fetchone()
    return res

def add_stock(sku,stock,u):
    if find_prod(sku) == True:
        fetch_products = cursor.execute(
            "SELECT stock FROM products WHERE sku = ?",(sku,)
        )
        product = fetch_products.fetchone()
        total_stock = stock + product[0]
        cursor.execute(
            "UPDATE products SET stock = ? WHERE sku = ?",(total_stock,sku)
        )
        conn.commit()
        create_logs(u,f"Add stock to {sku}, new stock: {total_stock}")
        return f"Νέο απόθεμα προϊόντος {sku}: {total_stock}"
    else:
        return f"Δεν βρέθηκε πελάτης"

def create_user(c_u,n_u,p,r_n,isadmin):
    fetch_users = cursor.execute(
        "SELECT * FROM users WHERE username = ?",(n_u,)
    )
    user_check = fetch_users.fetchone()
    if not user_check:
        encrypted_pass = hashlib.sha256(p.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, passw, real_name, is_admin) VALUES (?, ?, ?, ?)",(n_u,encrypted_pass,r_n,isadmin)
        )
        conn.commit()
        create_logs(c_u,f"Create user {n_u}")
        return f"Ο χρήστης δημιουργήθηκε"
    else:
        return f"Το όνομα χρήστη χρησιμοποιείται ήδη! Δοκιμαστε άλλο όνομα"

def delete_user(c_u,d_u):
    fetch_users = cursor.execute(
        "SELECT * FROM users WHERE username = ?",(d_u,)
    )
    user = fetch_users.fetchone()
    if user:
        cursor.execute(
            "DELETE FROM users WHERE username = ?",(d_u,)
        )
        conn.commit()
        create_logs(c_u,f"Delete user {d_u}")
        return f"Η διαγραφή ολοκληρώθηκε."
    else:
        return f"Δεν βρέθηκε χρήστης με αυτό το username"
    
def auth(user,passw):
    fetch_users = cursor.execute(
        "SELECT passw FROM users WHERE username = ?",(user,)
    )
    user_passw = fetch_users.fetchone()
    if user_passw:
        if user_passw[0] == hashlib.sha256(passw.encode()).hexdigest():
            create_logs(user,f"Logged in.")
            return True,True # Auth sucsessful
        else:
            return False,True #Wrong password
    else:
        return False,False # No user found

def check_admin(username):
    fetch_users = cursor.execute(
        "SELECT is_admin FROM users WHERE username = ?",(username,)
    )
    user = fetch_users.fetchone()
    if user:
        if user[0] == 1:
            isadmin = True
        elif user[0] == 0:
            isadmin = False
    else:
        isadmin = False
    return isadmin