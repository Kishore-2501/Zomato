import streamlit as st
import mysql.connector
import pandas as pd


# st.title("Zomato Database Connection Test") 
# st.write("Checking database connection...")

def get_db_connection():
  try:
   conn = mysql.connector.connect(
   host=st.secrets["connections"]["gateway01.us-west-2.prod.aws.tidbcloud.com"],
   user=st.secrets["connections"]["2b7jibPEQ1KmgLs.root"],
   password=st.secrets["connections"]["RncdgdnrSS9NzYzI"],
   database=st.secrets["connections"]["zomato"],
   port=st.secrets["connections"]["4000"],
   ssl_ca=st.secrets["connections"]["C:/Users/kisho/Downloads/isrgrootx1.pem"],
   use_pure=True )
        
if conn.is_connected():
   st.success("Connected successfully")
   return conn
else:
   st.error("Connection failed")
   return None
except mysql.connector.Error as err:
   st.error(f"Connection Error: {err}")
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

    "Highest Rated Restaurant": """ 
        SELECT restaurant_name, restaurant_rating 
        FROM restaurants 
        ORDER BY restaurant_rating DESC 
        LIMIT 1;
    """,

    "Customers with No Orders": """ 
        SELECT c.customer_id, c.customer_name 
        FROM customers c 
        LEFT JOIN orders o ON c.customer_id = o.customer_id 
        WHERE o.customer_id IS NULL;
    """,

    "Restaurants with No Orders": """ 
        SELECT r.restaurant_id, r.restaurant_name 
        FROM restaurants r 
        LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id 
        WHERE o.restaurant_id IS NULL;
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
