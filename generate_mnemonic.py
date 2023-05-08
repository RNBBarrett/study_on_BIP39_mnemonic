#all modules should be included in python
import random #for generating an initial binary number if we want it
import hashlib #used in sha-256 hash
import binascii #used in sha-256 hash

def generate_random_binary(length): #generates an initial binary number to use as an exmaple
    binary = ""
    for _ in range(length):
        bit = random.choice(["0", "1"])
        binary += bit
    return binary

def split_binary_numbers_into_list(binary_number): #split the initial binary number into a list of 12 numbers 0-11
    
    list_binary_numbers = [binary_number[i:i+11] for i in range(0, len(binary_number), 11)]
    return list_binary_numbers

def convert_list_binary_numbers_to_decimal(list_binary_numbers): #takes in a list of the 12 binary numbers, converts these to decimal with the exception of item 11 which it replaces with a question mark
    
    list_decimal_numbers = []
    #for each binary number we generated in our list
    for each_binary_number in list_binary_numbers:
        
        #convert the binary number to decimal
        each_decimal_number = int(each_binary_number, 2)
        #add it to a new list of decimal numbers
        list_decimal_numbers.append(each_decimal_number)

    #lets take the 12th item in our list, which is numbered 11 (lists start at 0) we are going to update that to a ? mark right now
    list_decimal_numbers[11] = '?'

    print('Your list of decimal numbers is: ', list_decimal_numbers)
    return list_decimal_numbers

def generate_sha256_hash(binary_number):
    hexstr = "{0:0>4X}".format(int(random_binary,2)) 
    data = binascii.a2b_hex(hexstr) 
    sha_result = hashlib.sha256(data).hexdigest()
    print("The sha-256 hash algorithm resulted in the hexadecimal: ", sha_result)
    return sha_result

def convert_sha256hash_to_binary_return_first_4bits(sha_result): #takes a sha-256 hash, converts it to binary, peels off the first item and converts it back to a four bit number
    # convert the whole sha_result back to binary
    binary_number = bin(int(sha_result, 16))[2:].zfill(256)
    print("The binary of your sha-256 hash is:", binary_number)
    # Extract the first 4 bits
    four_bit_number = binary_number[:4]
    print("Exracting the first four bits we get:", four_bit_number)
    return four_bit_number

def read_file_into_dictionary(filename): #takes in the bip39 words list, returns a dictionary of the words
    data_dict = {}
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            data_dict[line_number] = line.strip()
    return data_dict

def retrieve_seed_words(dictionary, decimal_numbers): #takes in a dictionary of bip39 words and a list of decimal numbers, matches list of decimal numbers against dictionary, returns the result as a list
    seed_phrase = []
    for a_decimal_number in decimal_numbers:
        if a_decimal_number in dictionary: #if the decimal number is in the dictionary
            seed_phrase.append(dictionary[a_decimal_number]) #take the word out of the dictionary and add it to our list
    return seed_phrase

def list_to_string(word_list): #takes in a list and returns a clean string
    return ' '.join(word_list)

def generate_seed_from_binary(binary_number): #the core function that takes in a binary number and gives back a complete seed phrase

    #split our initial 128-bit binary number into a list 11 bits per list item excluding item 12 which falls short at only 7 bits
    list_binary_numbers = split_binary_numbers_into_list(binary_number)

    #convery our list of binary numbers into a list of decimal numbers
    list_decimal_numbers = convert_list_binary_numbers_to_decimal(list_binary_numbers)

    # generate a sha-256 hash of the initial binary number passed into this function
    sha_result = generate_sha256_hash(binary_number)
    
    #convert the hash to binary, return back the first four bits
    four_bit_number = convert_sha256hash_to_binary_return_first_4bits(sha_result)

    #append this onto our list of binary numbers
    list_binary_numbers[11] = list_binary_numbers[11] + four_bit_number
    print('Your completed list of binary numbers is: ', list_binary_numbers)

    #finally convert this to decimal and put it in the 11 place in our list of decimals replacing the questions mark "?"
    #convert the binary number to decimal
    final_decimal_number = int(list_binary_numbers[11], 2)

    #add it to a new list of decimal numbers
    list_decimal_numbers[11] = final_decimal_number

    #iterate over array and add 1 to each number to get proper positions
    for number in range(len(list_decimal_numbers)): 
        list_decimal_numbers[number] = list_decimal_numbers[number] + 1

    print("Your final list of decimal numbers is:", list_decimal_numbers)

    #generate a dictionary from a file of bip39 words
    bip39_dictionary = read_file_into_dictionary("bip39.txt")

    #pass our bip39 dictionary and our list of decimal numbers in and get back a list of our final 12 words
    final_result = retrieve_seed_words(bip39_dictionary, list_decimal_numbers)

    my_seed_phrase = list_to_string(final_result)

    #print the result
    print("Your final list of seed words is: ", my_seed_phrase)

#main

#generate a binary numbner 128-bits long
random_binary = generate_random_binary(128)
print("Your initial binary number is: ", random_binary)

#generate seed phrase
generate_seed_from_binary(random_binary)