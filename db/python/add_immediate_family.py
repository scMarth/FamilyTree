import data
import immediate_family

mother = immediate_family.mother
father = immediate_family.father
children = immediate_family.children

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
    
