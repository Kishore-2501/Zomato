# Zomato

## Overview
This project focuses on analyzing food delivery data from Zomato using **Python, SQL, and Streamlit**. The objective is to enhance operational efficiency and improve customer satisfaction by providing data insights through an interactive Streamlit application.

## Features
- **Database Management**: Connects to a TiDB Cloud MySQL database.
- **Data Generation**: Uses Faker to create synthetic datasets for customers, orders, restaurants, and deliveries.
- **Data Analysis**: SQL queries extract insights such as peak order hours, top customers, and popular cuisines.
- **Interactive Dashboard**: A Streamlit app enables users to explore key metrics and execute queries dynamically.
- **Real-Time Analytics**: Incorporates live data updates for monitoring orders and deliveries.
- **User-Friendly Interface**: Simple and intuitive UI to explore insights efficiently.

## Tools Used
- **Python**
- **MySQL (TiDB Cloud)**
- **Streamlit**
- **Pandas**

## How to Run
1. **Install Dependencies:**
   
   pip install -r requirements.txt
   
2. **Set Up Database:**
   Create a MySQL database named zomato.
   Run zomato.py to generate data and insert it into the database.
3. **Run the Streamlit App:**

   streamlit run project.py

## SQL Queries Included
- Total customers, orders, and restaurants.
- Top 5 customers by order value.
- Peak ordering hours.
- Most common payment mode.
- Highest-rated restaurant.
- Orders with the highest value.
- Revenue breakdown per restaurant.
- Customer retention trends.

## Expected Results
By completing this project, you will achieve:
- A functional SQL database for food delivery management.
- An interactive Streamlit dashboard for data insights.
- A structured approach to analyzing food delivery trends.

## Note**
ssl_certificate added for CONNECTING secure transport

