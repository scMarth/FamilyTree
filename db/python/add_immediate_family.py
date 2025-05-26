import data

mother = ('Rick Owen Mom', 'Owen', 'Before', '1920-08-08')

father = ('Rick Owen Dad', 'Owen', '', '1920-08-08')

children = [
    ('Rick', 'Owen', '', '1920-08-08'),
    ('Timmy', 'Owen', '', '1920-08-08')
]

# add the members
members = [mother] + [father] + children
for member in members:
    first_name, last_name, maiden_name, birth_date = member
    data.add_member(first_name, last_name, maiden_name, birth_date)

# set the parents
for child in children:
    first_name, last_name, maiden_name, birth_date = child

    data.set_father(first_name, last_name, birth_date, father[0], father[1], father[3])
    data.set_mother(first_name, last_name, birth_date, mother[0], mother[1], mother[3])
    
