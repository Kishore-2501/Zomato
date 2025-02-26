import streamlit as st
import mysql.connector
import pandas as pd


def get_db_connection():

    conn = mysql.connector.connect(
       host=st.secrets["connections"]["host"],
       user=st.secrets["connections"]["user"],
       password=st.secrets["connections"]["password"],
       database=st.secrets["connections"]["database"],
       port=int(st.secrets["connections"]["port"]),
       ssl_ca=st.secrets["connections"]["ssl_ca"],  
       use_pure=True )
    if conn.is_connected():
            st.success("Connected successfully")
            return conn
    else:
            st.error("Connection failed")
            return None

queries = {
    "Total Customers": "SELECT COUNT(*) FROM customers;",

    "Total Orders": "SELECT COUNT(*) FROM orders;",

    "Total Restaurants": "SELECT COUNT(*) FROM restaurants;",

    "Top 5 Customers by Order Value": """ 
    SELECT c.customer_id, c.customer_name, SUM(o.total_amount) AS total_spent 
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id 
    GROUP BY c.customer_id, c.customer_name 
    ORDER BY total_spent DESC 
    LIMIT 5;
    """,

    "Top 5 Restaurants by Orders": """ 
    SELECT r.restaurant_id, r.restaurant_name, COUNT(o.order_id) AS total_orders 
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
    GROUP BY r.restaurant_id, r.restaurant_name 
    ORDER BY total_orders DESC 
    LIMIT 5;
    """,

    "Peak Order Hours": """ 
    SELECT HOUR(delivery_time) AS order_hour, COUNT(*) AS total_orders 
    FROM orders 
    GROUP BY order_hour 
    ORDER BY total_orders DESC 
    LIMIT 5;
    """,

    "Average Delivery Time per Restaurant": """ 
        SELECT r.restaurant_name, AVG(d.delivery_time) AS avg_delivery_time 
        FROM deliveries d 
        JOIN orders o ON d.order_id = o.order_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
        GROUP BY r.restaurant_name 
        ORDER BY avg_delivery_time ASC;
    """,

    "Most Common Payment Mode": """ 
        SELECT payment_mode, COUNT(*) AS count 
        FROM orders 
        GROUP BY payment_mode 
        ORDER BY count DESC 
        LIMIT 1;
    """,

    "Most Popular Cuisine Type": """ 
        SELECT cuisine_type, COUNT(*) AS order_count 
        FROM restaurants r 
        JOIN orders o ON r.restaurant_id = o.restaurant_id 
        GROUP BY cuisine_type 
        ORDER BY order_count DESC 
        LIMIT 1;
    """,

    "Average Order Value": """ 
        SELECT AVG(total_amount) AS avg_order_value 
        FROM orders;
    """,

    "Cancelled Orders Count": """ 
        SELECT COUNT(*) AS cancelled_orders 
        FROM orders 
        WHERE status = 'Cancelled';
    """,
    
     "Most Used Vehicle Type for Deliveries": """ 
    SELECT vehicle_type, COUNT(*) AS total_deliveries 
    FROM deliveries 
    GROUP BY vehicle_type 
    ORDER BY total_deliveries DESC 
    LIMIT 1; 
    """,

    "Premium vs Non-Premium Customers": """ 
        SELECT is_premium, COUNT(*) AS total_customers 
        FROM customers 
        GROUP BY is_premium;
    """,

   "Total Revenue by Restaurant": """ 
    SELECT r.restaurant_id, r.restaurant_name, SUM(o.total_amount) AS total_revenue 
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
    GROUP BY r.restaurant_id, r.restaurant_name 
    ORDER BY total_revenue DESC;
    """,
    
   "Count of Different Payment Methods": """ 
    SELECT payment_mode, COUNT(*) AS total_count 
    FROM orders 
    GROUP BY payment_mode; 
    """,

    "Highest Rated Restaurant": """ 
        SELECT restaurant_name, restaurant_rating 
        FROM restaurants 
        ORDER BY restaurant_rating DESC 
        LIMIT 1;
    """,

    "Top 5 Fastest Deliveries": """ 
        SELECT o.order_id, r.restaurant_name, d.delivery_time 
        FROM deliveries d 
        JOIN orders o ON d.order_id = o.order_id 
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
        ORDER BY d.delivery_time ASC 
        LIMIT 5;
    """,

    "Total Discount Given": """ 
        SELECT SUM(discount_applied) AS total_discount 
        FROM orders;
    """,

    "Most Expensive Order": """ 
    SELECT o.order_id, o.total_amount, c.customer_name, r.restaurant_name 
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id 
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
    ORDER BY o.total_amount DESC 
    LIMIT 1;
    """,

    "Least rated 5 Restaurants by Average Feedback Rating": """ 
    SELECT r.restaurant_id, r.restaurant_name, AVG(o.feedback_rating) AS avg_rating 
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
    GROUP BY r.restaurant_id, r.restaurant_name 
    HAVING avg_rating < 2.5 
    ORDER BY avg_rating ASC 
    LIMIT 5;
    """

}

st.title("Zomato-SQL Queries")

selected_query = st.selectbox("Select a query to execute:", list(queries.keys()))

if st.button("Run Query"):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        st.write(f"Executing query: {queries[selected_query]}")
        cursor.execute(queries[selected_query])
        data = cursor.fetchall()
        conn.close()
        
        st.write("### Query Result:")
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        st.dataframe(df)
def add_delivery_person(name, contact_number, vehicle_type, location):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO delivery_person (name, contact_number, vehicle_type, location) VALUES (%s, %s, %s, %s)",
                (name, contact_number, vehicle_type, location)
            )
            conn.commit()
            st.success("New Delivery Person Added Successfully")
        except Exception as e:
            st.error(f"Error Adding Delivery Person: {e}")
        finally:
            conn.close()

def get_all_delivery_person():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM delivery_person")
            data = cursor.fetchall()
            return data
        except Exception as e:
            st.error(f"Error Fetching Data: {e}")
            return []
        finally:
            conn.close()

def update_delivery_person(delivery_person_id, name, contact_number, vehicle_type, location):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE delivery_person SET name=%s, contact_number=%s, vehicle_type=%s, location=%s WHERE delivery_person_id=%s",
                (name, contact_number, vehicle_type, location, delivery_person_id)
            )
            conn.commit()
            st.success("Delivery Person Updated Successfully")
        except Exception as e:
            st.error(f"Error Updating Delivery Person: {e}")
        finally:
            conn.close()

def delete_delivery_person(delivery_person_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM delivery_person WHERE delivery_person_id=%s", (delivery_person_id,))
            conn.commit()
            st.success("Delivery Person Deleted Successfully")
        except Exception as e:
            st.error(f"Error Deleting Delivery Person: {e}")
        finally:
            conn.close()
option_list = ["Create", "Read", "Update", "Delete", "None"]
option = st.sidebar.selectbox("Select Operation", option_list, index=option_list.index("None"))

if option == "Create":
    st.title("CRUD OPERATION WITH MYSQL")
    st.subheader("Create a Delivery Person Record")
    
    delivery_person_id = st.number_input("Enter ID", min_value=1, step=1)
    name = st.text_input("Enter Name")
    contact_number = st.text_input("Enter Contact Number")
    vehicle_type = st.selectbox("Select Vehicle Type", ["Bike", "Car", "Scooter"])
    location = st.text_input("Enter Location")

    if st.button("Create"):
        if delivery_person_id and name and contact_number and vehicle_type and location:
            con = get_db_connection()
            cur = con.cursor()
            sql = "INSERT INTO delivery_person (delivery_person_id, name, contact_number, vehicle_type, location) VALUES (%s, %s, %s, %s, %s)"
            val = (delivery_person_id, name, contact_number, vehicle_type, location)
            cur.execute(sql, val)
            con.commit()
            con.close()
            st.success("New Delivery Person Added Successfully")
        else:
            st.error("All fields are required.")

elif option == "Read":
    st.title("CRUD OPERATION WITH MYSQL")
    st.subheader("Show All Delivery Persons")

    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM delivery_person")
    res = cur.fetchall()

    columns = [i[0] for i in cur.description]  
    show_df = pd.DataFrame(res, columns=columns)
    
    con.close()
    st.dataframe(show_df)

elif option == "Update":
    st.title("CRUD OPERATION WITH MYSQL")
    st.subheader("Update Delivery Person Record")

    delivery_person_id = st.number_input("Enter ID", min_value=1)
    name = st.text_input("Enter New Name")
    contact_number = st.text_input("Enter New Contact Number")
    vehicle_type = st.selectbox("Select New Vehicle Type", ["Bike", "Car", "Scooter"])
    location = st.text_input("Enter New Location")

    if st.button("Update"):
        if name and contact_number and vehicle_type and location:
            con = get_db_connection()
            cur = con.cursor()
            sql = "UPDATE delivery_person SET name=%s, contact_number=%s, vehicle_type=%s, location=%s WHERE delivery_person_id=%s"
            val = (name, contact_number, vehicle_type, location, delivery_person_id)
            cur.execute(sql, val)
            con.commit()
            con.close()
            st.success("Delivery Person Updated Successfully")
        else:
            st.error("All fields are required.")

elif option == "Delete":
    st.title("CRUD OPERATION WITH MYSQL")
    st.subheader("Delete Delivery Person Record")

    delivery_person_id = st.number_input("Enter ID to Delete", min_value=1, step=1)

    if st.button("Delete"):
        con = get_db_connection()
        cur = con.cursor()
        sql = "DELETE FROM delivery_person WHERE delivery_person_id = %s"
        val = (delivery_person_id,)
        cur.execute(sql, val)
        con.commit()
        con.close()
        st.success("Delivery Person Deleted Successfully")
