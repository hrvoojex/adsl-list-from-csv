# Daje nam izlistanje svih korisnika koji trose vise od nekog broja (gb_number) GB MAXadsl prometa 
prekrsitelji = dict()
tmp = list()
file = raw_input('Unesi ime csv datoteke: ')
try:
    handler = open(file)
except:
    print 'Ne postoji takva datoteka ', file + ', izlazim ...'
    exit()
try:
    gb_number = int(raw_input('Unesi broj GB prema kojim zelis filtrirati: '))
except ValueError:
    print 'Nije broj. Mora biti broj. Izlazim ...'
    exit()    
for line in handler:
    line = line.rstrip()
    line = line.split(';')
    if 'MAXadsl promet' in line and line[0] == 'DETAIL' :
	if int(line[5]) > gb_number :
	    prekrsitelji[line[2]] = line[5]

for key, val in prekrsitelji.items() :
    tmp.append( (int(val), key) )

tmp.sort(reverse=True)
for val, key in tmp :
    print val, 'GB', key
