from pymongo import MongoClient
import os
import pandas as pd
import snowflake.connector as sc

# Function to establish Snowflake connection using environment variables
def connect_to_snowflake():
    try:
        conn = sc.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

# Function to establish MongoDB connection using environment variables
def connect_to_mongodb():
    try:
        client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Establish connections
scconn = connect_to_snowflake()
mcconn = connect_to_mongodb()

def execute_query(query, params=None):
    """Helper function to execute a query with optional parameters."""
    try:
        cursor = scconn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def getTotalCasesByCountry():
    query = """
        SELECT COUNTRY_REGION, SUM(CASES) AS TOTAL_CASES
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.ECDC_GLOBAL
        GROUP BY COUNTRY_REGION
        ORDER BY SUM(CASES) DESC
    """
    return execute_query(query)

def getTotalCasesByDate():
    query = """
        SELECT DATE, SUM(CASES) AS TOTAL_CASES
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.ECDC_GLOBAL
        GROUP BY DATE
        ORDER BY DATE
    """
    return execute_query(query)

def getCasesByCountry(country):
    query = """
        SELECT DATE, CASES
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.ECDC_GLOBAL
        WHERE COUNTRY_REGION = %s
        ORDER BY DATE
    """
    return execute_query(query, (country,))

def getTotalDeaths():
    query = """
        SELECT COUNTRY_REGION, SUM(DEATHS) AS TOTAL_DEATHS
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.ECDC_GLOBAL
        GROUP BY COUNTRY_REGION
        ORDER BY SUM(DEATHS) DESC
    """
    return execute_query(query)

def getDeathsByCountry(country):
    query = """
        SELECT DATE, DEATHS
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.ECDC_GLOBAL
        WHERE COUNTRY_REGION = %s
        ORDER BY DATE
    """
    return execute_query(query, (country,))

def getEconomicsDataByCountry(country):
    try:
        table = pd.read_csv("data/economicDB.csv")
        # Filter data based on the country
        filtered_data = table[table['country'] == country]
        return filtered_data
    except Exception as e:
        print(f"Error loading or filtering economic data: {e}")
        return None
