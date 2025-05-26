import data

members = [
    # first name, last name, maiden name, birth day (YYYY-MM-DD)
    # ("Dio's Mother", "", "", "1920-06-06"),
    # ("Dario", "Brando", "", "1920-06-06"),
    # ("Dio", "Brando", "", "1920-06-06"),
    # ("Giorno's Mother", "", "", "1920-06-06"),
    # ("Giorno", "Giovanna", "", "1920-06-06"),
    # ("John", "Doe", "", "1920-06-06"),
    # ("Jane", "Doe", "", "1920-06-06"),
    # ("John Mom", "Doe", "", "1920-06-06"),
    # ("John Dad", "Doe", "", "1920-06-06"),
    # ("Jane Dad", "Something", "", "1920-06-06"),
    # ("Jane Mom", "Something", "", "1920-06-06"),
]

try:

    # insert members
    # for member in members:
    #     first_name, last_name, maiden_name, birth_date = member
    #     data.add_member(first_name, last_name, maiden_name, birth_date)

    

    print('first test:')
    print(data.member_exists('Jane', 'Doe', '1920-06-06'))

    print('second test:')
    print(data.member_exists('Jane', 'Doe', '1920-06-07'))



except Exception as e:
    print('Error:', e)