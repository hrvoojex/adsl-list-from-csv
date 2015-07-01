#!/usr/bin/python

"""
Prints ADSL internet traffic, talk length and invoice amount from
T-Com csv file in top list form. You can download the file from
T-Com Business admin portal.
Autor: hrvooje
Datum: 20.04.2015.
Licenca: GPLv2
"""
import sys

def user_input_str(prompt):
    """
    Takes an input as a string value from a user.
    """
    while True:
        try:
            value = raw_input(prompt)
        except ValueError:
            print('Wrong input. Try again.')
            continue
        break
    return value

def uis_non_empyt(prompt):
    """
    Takes an input as a string value from a user.
    Does not allow empty string.
    """
    while True:
        try:
            value = raw_input(prompt)
            if value == '':
                continue

        except ValueError:
            print('Wrong input. Try again.')
            continue
        break
    return value

def user_input_int(prompt):
    """
    Takes an input as a integer value from a user.
    If it's not integer or it's negative value it throws an error.
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
    throws an error if not valid encoding.
    Empty string is by default windows-1250.
    Returns encoding.
    """
    while True:
        enc = raw_input(prompt)
        if enc == '':
            enc = 'windows-1250'

        try:
            tmp = ''.decode(enc) # Just to throw an error if not correct
        except:
            print('Wrong input. Try again.')
            continue
        break
    return enc

def add_csv(file_name):
    """
    Takes file name and adds '.csv' if it is not there
    """
    if file_name[-4:] != '.csv':
        file_name = file_name + '.csv'
        return file_name
    return file_name

def choice(prompt):
    """
    Takes an input from a user which information does he want from a file.
    The user has a choice 1, 2, or 3.
    ESC is for exit the program.
    """
    while True:
        #print prompt
        char = user_input_str(prompt)
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
    index  = -1 # index after increasing becomes 0 and first element in a list
    for word in lst: # for every keyword in a list
        index += 1 # indexing a list, so it is easier to modify in 122th row
        while True: # loop exits if the entry is correct
            print("\nKeyword for selecting a line in a file: %s") % word
            char = user_input_str("\nLeave this keyword or enter new? [Y/n]")
            if char == 'y' or char == 'Y' or char == '':
                break
            elif char == 'n' or char == 'N': # change a keyword if char = n
                words = raw_input("Enter a new string (ESC for exit): ")
                lst[index] = words.decode('utf-8')
                break # after new keyword, take new Keyword from a list
            elif char == u'\u001b': # unicode ESC key for exit
                sys.exit("Quitting ...") # exits out of the program
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
    try:
        data = open(csv_file)
    except:
        print("No such file %s" % tht_file_csv)
        sys.exit("Quitting...")

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
                    new_key = line[1] + ' ' + line[2]
                    dictionary[new_key] = (
                        dictionary.get(new_key, 0) + converted
                        )
                else:
                    new_key = line[1] + ' ' + line[2]
                    dictionary[new_key] = (
                        dictionary.get(new_key, 0) +
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
        from_top = raw_input("Enter list length: ")
        if from_top == '':
            from_top = 0
    
        try:
            from_top = int(from_top)
            if from_top >= 0:
                break
        except:
            if from_top == None:
                break
            else:
                print("Must be positive.")
                continue

    tmp = list()
    count = 0
    for key, val in dicton.items(): # creates list of tuples from key, val
        tmp.append( (val, key))
        tmp.sort(reverse=True) # sorts list by value val
        if from_top != 0:
            tmp = tmp[:from_top] # prints only 'from_top' keys, lines

    for key, val in tmp:
        count += 1
        if user_choice == 1:
            print("%d. %.d GB %s" % (count, key, val))
        elif user_choice == 2:
            print("%d. %.2f min. %s" % (count, key, val))
        else:
            print("%d. %.2f HRK %s" % (count, key, val))

def nice_print(num):
    """
    Prints number without decimal places
    if they are zeros
    """
    if num - int(num) != 0:
        print("%.2f" % num)
    else:
        print("%d" % num)

# default list of keywords if user choice is maxadsl
maxadsl_default = [u'MAXadsl promet']
# default list of keywords if user choice is converation time
conversation_time_default = [
    u'Promet uklju\u010Den u Business Minute Fix',
    u'Promet uklju\u010Den u Business Minute Mobile',
    u'Promet uklju\u010Den u Business Minute International',
    u'POS transakcija',
    u'Me\u0111unarodni promet - VoIP',
    u'Nacionalni VPN promet-VoIP',
    ]
# default list of keywords if user choice is amount
amount_default = [
    u'Mjese\u010Dna naknada',
    u'Mjese\u010Dna naknada za ADSL pristup',
    u'Usluge s posebnim tarifama',
    u'POS transakcija',
    ]
# default list for choice
choice_default = [
    "1 - MAXADSL TRAFFIC",
    "2 - CONVERSATION TIME",
    "3 - AMOUNT",
    ]
    
# Here starts script execution
tht_file = uis_non_empyt('Enter a T-Com csv file name: ')
tht_file_csv = add_csv(tht_file) # adds .csv if not given from a user
print("Loading file %s into memory.") % tht_file_csv
print("\nChoose a data from file:")
for s in choice_default:
    print s

user_choice = choice("\nSelect an option 1, 2 or 3 (ESC for exit): ")
print("You chose: "), choice_default[user_choice-1]
encoding_code = encoding_code(
    "\nEnter your file encoding (ENTER for windows-1250): "
    )
mod_list = modified_list(user_choice)
print_list(mod_list) # Prints a keyword list, each iteam in a new row
print '' # prints empty line
result_dict = lines(tht_file_csv, encoding_code, user_choice)
print_from_top(result_dict)
