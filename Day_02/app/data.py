import psycopg2

def database_connection() :
    try:
        connection = psycopg2.connect(user="postgres", password="Hk@0810@2001", host="localhost", port="5433", database="db_posts")
        print("\n---------- Connection established Successfully ----------")
        return connection

    except Exception as error: 
        print(f"Error when establishing connction {error}")


def close_database_connection(connection) :
    try :
        if (connection):
            connection.close()
            print("----------- PostgreSQL connection is closed -----------")
    
    except Exception as e :
        print(f"Error when closing connection {e}")