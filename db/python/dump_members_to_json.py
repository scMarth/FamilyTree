import data, json

rows = data.get_all_member_data()

members = []
for row in rows:
    objectid, first_name, last_name, maiden_name, birth_date, mother_id, father_id = row

    birth_date_str = birth_date.strftime('%Y-%m-%d')

    members.append([objectid, first_name, last_name, maiden_name, birth_date_str, mother_id, father_id])

# dump to json file
with open('member_data.json', 'w') as outfile:
    json.dump(members, outfile, indent=4)