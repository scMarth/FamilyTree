import pyodbc, os, json, sys
import data

# target different database
data.conn_str = data.conn_str.replace("DATABASE=FamilyTree;", "DATABASE=FamilyTree2;")

members = None
with open('member_data.json', 'r') as read_file:
    members = json.load(read_file)

# build a mapping from id to name and birth date data
id_to_member_info_map = {}

for member in members:
    objectid, first_name, last_name, maiden_name, birth_date, _, _ = member

    id_to_member_info_map[objectid] = [first_name, last_name, maiden_name, birth_date]


# first add all members
for member in members:
    objectid, first_name, last_name, maiden_name, birth_date, mother_id, father_id = member

    data.add_member(first_name, last_name, maiden_name, birth_date)

# set parent data, needs to be done after prior loop to ensure parent is already in the database
for member in members:
    objectid, first_name, last_name, maiden_name, birth_date, mother_id, father_id = member

    new_member_objectid = data.get_member_objectid(first_name, last_name, maiden_name, birth_date)

    if mother_id:
        mother_first_name, mother_last_name, mother_maiden_name, mother_birth_date = id_to_member_info_map[mother_id]
        
        new_mother_objectid = data.get_member_objectid(mother_first_name, mother_last_name, mother_maiden_name, mother_birth_date)

        data.set_mother_via_objectid(new_member_objectid, new_mother_objectid)

    if father_id:
        father_first_name, father_last_name, father_maiden_name, father_birth_date = id_to_member_info_map[father_id]
        
        new_father_objectid = data.get_member_objectid(father_first_name, father_last_name, father_maiden_name, father_birth_date)

        data.set_father_via_objectid(new_member_objectid, new_father_objectid)