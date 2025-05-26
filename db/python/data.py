import pyodbc, os

username = os.environ['LOCAL_SQLEXPRESS_USER']
password = os.environ['LOCAL_SQLEXPRESS_PW']
sql_server = os.environ['LOCAL_SQLEXPRESS_SERVER'] # note, can be on another computer e.g. "192.xxx.x.xx\SQLEXPRESS"

# Define connection string
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    rf"SERVER={sql_server};"
    r"DATABASE=FamilyTree;"
    r"Trusted_Connection=no;"
    rf"UID={username};"
    rf"PWD={password};"
)

# return a database connection and cursor
def get_connection():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return [cursor, conn]

def commit_and_clean(cursor, conn):
    cursor.commit()

    # Clean up
    cursor.close()
    conn.close()

def add_member(first_name, last_name, maiden_name, birth_date):

    # don't add the member if they already are in the table
    if member_exists(first_name, last_name, birth_date):
        print('Note member already exists, skipping: first name = "{}" ; last name = "{}" ; maiden_name = "{}" ; birth_date = "{}"'.format(first_name, last_name, maiden_name, birth_date))
        return

    cursor, conn = get_connection()
    cursor.execute("INSERT INTO Members (FIRST_NAME, LAST_NAME, MAIDEN_NAME, BIRTH_DATE) VALUES (?, ?, ?, ?)", (first_name, last_name, maiden_name, birth_date))
    commit_and_clean(cursor, conn)

def set_mother(first_name, last_name, birth_date, mother_first_name, mother_last_name, mother_birth_date):
    cursor, conn = get_connection()
    cursor.execute("UPDATE Members SET MOTHER = (SELECT TOP(1) OBJECTID FROM Members WHERE FIRST_NAME=? AND LAST_NAME=? AND BIRTH_DATE=?) WHERE FIRST_NAME=? AND LAST_NAME=? AND BIRTH_DATE=?", (mother_first_name, mother_last_name, mother_birth_date, first_name, last_name, birth_date))
    commit_and_clean(cursor, conn)

def set_father(first_name, last_name, birth_date, father_first_name, father_last_name, father_birth_date):
    cursor, conn = get_connection()
    cursor.execute("UPDATE Members SET FATHER = (SELECT TOP(1) OBJECTID FROM Members WHERE FIRST_NAME=? AND LAST_NAME=? AND BIRTH_DATE=?) WHERE FIRST_NAME=? AND LAST_NAME=? AND BIRTH_DATE=?", (father_first_name, father_last_name, father_birth_date, first_name, last_name, birth_date))
    commit_and_clean(cursor, conn)

# return true or false on whether a member exists in the table given their name and a birth day in format YYYY-MM-DD
def member_exists(first_name, last_name, birth_date):
    cursor, conn = get_connection()
    cursor.execute("SELECT * FROM Members WHERE (FIRST_NAME=?) AND (LAST_NAME=?) AND (BIRTH_DATE=?)", (first_name, last_name, birth_date))
    rows = cursor.fetchall()

    # Clean up
    cursor.close()
    conn.close()

    if len(rows) >= 1:
        return True
    else:
        return False

