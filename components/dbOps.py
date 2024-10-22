import psycopg2
from psycopg2.extras import RealDictCursor

def connect_db():
    return psycopg2.connect(
        dbname="watchdb",
        user="rukonpsql",
        password="String@4099",
        host="localhost"
    )


def insert_data(querry, vals):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(querry + " RETURNING id;", vals)
        inserted_id = cur.fetchone()[0]
        conn.commit()
        print(f"Inserted successfully. ID: {inserted_id}")
        
        return inserted_id
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def get_data(tableName, limit=10, offset=0):
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute(f"SELECT * FROM {tableName}")
        watches = cur.fetchall()
        return watches
    except Exception as e:
        print(f"An error occurred while retrieving data: {e}")
        return []
    finally:
        cur.close()
        conn.close()