import pyodbc, os

username = os.environ['LOCAL_SQLEXPRESS_USER']
password = os.environ['LOCAL_SQLEXPRESS_PW']
sql_server = os.environ['LOCAL_SQLEXPRESS_SERVER']

# Define connection string
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    rf"SERVER={sql_server};"
    r"DATABASE=FamilyTree;"
    r"Trusted_Connection=no;"
    rf"UID={username};"
    rf"PWD={password};"
)

members = [
    # first name, last name, maiden name, birth day (YYYY-MM-DD)
    # ("Dio's Mother", "", "", "1920-06-06"),
    # ("Dario", "Brando", "", "1920-06-06"),
    # ("Dio", "Brando", "", "1920-06-06"),
    # ("Giorno's Mother", "", "", "1920-06-06"),
    # ("Giorno", "Giovanna", "", "1920-06-06"),
    ("John", "Doe", "", "1920-06-06"),
    ("Jane", "Doe", "", "1920-06-06"),
    ("John Mom", "Doe", "", "1920-06-06"),
    ("John Dad", "Doe", "", "1920-06-06"),
    ("Jane Dad", "Something", "", "1920-06-06"),
    ("Jane Mom", "Something", "", "1920-06-06")
]

def add_member(cursor, first_name, last_name, maiden_name, birth_date):
    cursor.execute("INSERT INTO Members (FIRST_NAME, LAST_NAME, MAIDEN_NAME, BIRTH_DATE) VALUES (?, ?, ?, ?)", (first_name, last_name, maiden_name, birth_date))

def set_mother(cursor, first_name, last_name, mother_first_name, mother_last_name):
    cursor.execute("UPDATE Members SET MOTHER = (SELECT TOP(1) OBJECTID FROM Members WHERE FIRST_NAME=? AND LAST_NAME=?) WHERE FIRST_NAME = ? AND LAST_NAME = ?", (mother_first_name, mother_last_name, first_name, last_name))

def set_father(cursor, first_name, last_name, father_first_name, father_last_name):
    cursor.execute("UPDATE Members SET FATHER = (SELECT TOP(1) OBJECTID FROM Members WHERE FIRST_NAME=? AND LAST_NAME=?) WHERE FIRST_NAME = ? AND LAST_NAME = ?", (father_first_name, father_last_name, first_name, last_name))

try:
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # insert members
    for member in members:
        first_name, last_name, maiden_name, birth_date = member
        add_member(cursor, first_name, last_name, maiden_name, birth_date)
    cursor.commit()

    set_father(cursor, 'Jane', 'Doe', 'Jane Dad', 'Something')
    set_mother(cursor, 'Jane', 'Doe', "Jane Mom", 'Something')
    set_father(cursor, 'John', 'Doe', 'John Dad', 'Doe')
    set_mother(cursor, 'John', 'Doe', "John Mom", 'Doe')
    cursor.commit()

    cursor.execute("SELECT * FROM Members")

    # Fetch and print results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Clean up
    cursor.close()
    conn.close()

except Exception as e:
    print("Error connecting to the database:", e)
