import configparser
import psycopg2
from sql_queries import drop_table_queries, create_table_queries


def drop_tables(cur, conn):
    """
    Loops over queries in drop_table_queries to drop the tables in our
    redshift cluster
    Args:
        cur: Cursor for the connection, conn.cur() in a psycop2 connect object
        conn: Psycop2.connect(connection string)
    Returns: Nothing
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function creates the tables needed for our ETL process in the
    redshift cluster
    Args:
        cur: Cursor for the connection, conn.cur() in a psycop2 connect object
        conn: Psycop2.connect(connection string)
    Returns: Nothing
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Loads config files, creates connect and cursor objects,
    executes the drop tables function, and creates our staging tables and our
    star schema tables
    """
    config = configparser.ConfigParser()
    config.read('credentials/dwh.cfg')
    connstring = "host={} dbname={} user={} password={} port={}"
    connstring = connstring.format(*config['CLUSTER'].values())
    conn = psycopg2.connect(connstring)
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
