# CNOunlimited/sql_conn.py

from sqlalchemy import create_engine

def db_connect(host, database, username, password, dbms, driver, port):
    try:
        conn = f"{dbms}+pyodbc://{username}:{password}@{host}:{port}/{database}?driver={driver}"
        engine = create_engine(conn)
        return engine
    except Exception as e:
        print(f"Error during database connection: {e}")
        return None


# function to close the connection to the database
def db_close(engine):
    try:
        engine.close()
    except Exception as e:
        print(f"Error during closing database connection: {e}")


# Example usage:
# engine = db_connect(host, database, username, password, dbms, driver, port)
# if engine is not None:
#     # Do something with the engine...
#     db_close(engine)
# else:
#     print("Database connection failed.")
