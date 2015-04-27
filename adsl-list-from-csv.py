#!/usr/bin/python

"""
Ispisuje ADSL promet, duljinu razgovora i iznos racuna
iz t-ht csv datoteke racuna s admin portala t-ht-a
Autor: hrvooje
Datum: 20.04.2015.
Licenca: GPLv2
"""
import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def ui_str(prompt):
	"""
	Uzima unos od korisnika kao string.
	"""
	while True:
		try:
			value = raw_input(prompt)
		except ValueError:
			print('Unos nije dobar.')
			continue
		break
	return value

def ui_int(prompt):
	"""
	Uzima unos od korisnika kao integer.
	Javlja gresku, ako nije integer ili ako je negativan.
	"""
	while True:
		try:
			value = int(raw_input(prompt))
		except ValueError:
			print('Wrong input. Try again.')
			continue

		if value < 0:
			print('Negative values are not allowed.')
			continue
		else:
			break
	return value

def encoding_code(prompt):
    """
    Asks for an encoding,
    throws an error if not ok.
    Returns encoding.
    """
    while True:
        try:
            enc = raw_input(prompt)
            tmp = ''.decode(enc) # Just to throw an error if not correct
        except:
            print("Wrong input. Try again.")
            continue
        break
    return enc
    

def add_csv(value):
	"""
	Uzima ime datoteke kao unos i dodaje .csv nastavak ako ga nema.
	"""
	if value[-4:] != '.csv':
		value = value + '.csv'
		return value
	return value

def choice(prompt):
    """
    Uzima odabir od korisnika koje informacije zeli iz datoteke.
    Korisnik bira 1, 2 ili 3. 
    ESC gasi program.
    """
    while True:
    	print prompt
        getch = _Getch() # iz klase _Getch()
        char = getch.impl()
        if char == '\x1B': # ESC is pressed
            sys.exit("Quitting ...")
        elif char.lower() not in ('1', '2', '3'):
            print("Wrong selection. Try again: ")
            continue
        else:
            break
    return int(char)

def keywords(lst):
    """
    Takes list as an argument. 
    User is asked to change the list or not.
    Returns a modified or default list
    """
    index  = -1 # -1 jer se odmah poveca za 1 i index u listi je 0
    for word in lst: # za svaku kljucnu rijec u listi
        index += 1 # indeksira listu, pa se lakse modificira u 122. redu
        while True: # petlja iz koje se izlazi ako je unos ispravan
            print(
                "\nKeyword for selecting a line in a file: %s"
                "\n(L)eave this keyword or (C)hange: "
                ) % word
            getch = _Getch() # uzima pritisak tipke tipkovnice kao utf-8
            chars = getch.impl()
            char = chars.decode('utf-8') # dekodira pritisak tipke u unicode
            if char == u'l' or char == u'L':
                break
            elif char == u'c' or char == u'C': # ako je odgovor c, unosi se
                words = raw_input("Enter a new string (ESC for exit): ")
                lst[index] = words.decode('utf-8')
                break # nakon unosa, ide van petlje na novi word u listi
            elif char == u'\u001b': # ako je unos escape (unicode)
                sys.exit("Quitting ...") # izlazi van programa
            else:
                print('Wrong input. Try again.')
                continue
    return lst

def print_list(lst):
    """
    Prints the list. Each item in a new line.
    Adds an ordinal number.
    """
    count = 1
    print("\nFile lines will be searched for these keywords: ")
    for i in lst:
        print("%d. %s" % (count, i))
        count += 1

def modified_list(user_choice):
    """
    Takes int user_choice as input.
    Returns the same or modified list
    """
    if user_choice == 1:
        mod_list = keywords(maxadsl_default)
    elif user_choice == 2:
        mod_list = keywords(conversation_time_default)
    else:
        mod_list = keywords(amount_default)
    return mod_list

def time_convert(time_min_sec):
    times = time_min_sec.split(':')
    time_min = float(times[0])
    time_sec = float(times[1]) / 60.0
    time = time_min + time_sec
    return str(time)

def lines(csv_file,encoding_code, user_choice):
    """
    Takes a csv file as an input,
    filters lines by keywords,
    returns a dictionary with selected lines and data of interest
    """
    dictionary = dict()
    data = open(csv_file)
    for line in data:
        if line.startswith("DETAIL") == False:
            continue
        line = line.rstrip()
        line = line.decode(encoding_code)
        line = line.split(";")
        for word in line:
            if word in mod_list:
                if user_choice == 1:
                    dictionary[line[2]] = (
                        dictionary.get(line[2], 0) + int(line[5])
                        )
                elif user_choice == 2:
                    temp = line[6].split(":")
                    converted = float(temp[0]) + float(temp[1]) / 60.0
                    dictionary[line[2]] = (
                        dictionary.get(line[2], 0) + converted
                        )
                else:
                    dictionary[line[2]] = (
                        dictionary.get(line[2], 0) + 
                        float(line[9].replace(',', '.')) #eg. 15,2 to 15.2
                        )

    return dictionary

def print_from_top(dicton):
    """
    Takes dictionary dicton as input
    and number from_top, which tells us how
    many to print from top of the list.
    """
    from_top = ''
    while True:
        try:
            from_top = int(raw_input
                ("Unesi broj ispisa od vrha (0 za sav ispis): ")
                )
            if from_top >= 0:
                break
        except:
            if from_top == None:
                break
            else:
                print("Mora biti broj veci od nule")
                continue

    tmp = list()
    for key, val in dicton.items(): # creates list of tuples from key, val
        tmp.append( (val, key))
        tmp.sort(reverse=True) # sorts list by value val
        if from_top != 0:
            tmp = tmp[:from_top] # prints only 'from_top' keys, lines
    # print tmp
    for key, val in tmp:
        if user_choice == 1:
            print("Vrijednost: %.2f GB Identifikator: %s" % (key, val))
        elif user_choice == 2:
            print("Vrijednost: %.2f min. Identifikator: %s" % (key, val))
        else:
            print("Vrijednost: %.2f HRK Identifikator: %s" % (key, val))
        
maxadsl_default = [u'MAXadsl promet']
conversation_time_default = [
    u'Promet uklju\u010Den u Business Minute Fix',
    u'Promet uklju\u010Den u Business Minute Mobile',
    u'Promet uklju\u010Den u Business Minute International',
    u'POS transakcija',
    u'Me\u0111unarodni promet - VoIP',
    u'Nacionalni VPN promet-VoIP',
    ]
amount_default = [
    u'Mjese\u010Dna naknada',
    u'Mjese\u010Dna naknada za ADSL pristup',
    u'Usluge s posebnim tarifama',
    u'POS transakcija',
    ]
choice_default = [
    "1 - MAXADSL TRAFFIC",
    "2 - CONVERSATION TIME",
    "3 - AMOUNT",
    ]
tht_file = ui_str('Enter a T-Com .csv file name: ')
tht_file_csv = add_csv(tht_file) # csv s podacima i encodingom windows-1250
print("Loading file %s into memory.") % tht_file_csv
print("\nChoose a data from file:")
for s in choice_default:
    print s

user_choice = choice("\nSelect an option 1, 2 or 3 (ESC for exit): ")
print("You chose: "), choice_default[user_choice-1]
encoding_code = encoding_code(
    "Enter your file encoding (eg. windows-1250, utf-8, ISO-8859-2): "
    )
mod_list = modified_list(user_choice)
print_list(mod_list) # Prints a list, each iteam in a new row
result_dict = lines(tht_file_csv, encoding_code, user_choice)
print(result_dict)
print_from_top(result_dict)
