### Study_BIP39_SeedPhrases ###
-------------------------------

This readme consists of notes from a personal study on constructing valid BIP39 seed phrases for use in Bitcoin wallet recovery.
I have learned much of this material from: https://www.blockplate.com/blogs/blockplate/how-a-seed-phrase-is-created
and give them full credit for their detailed explaination which exists in few places online.

### Intro ###

A seed phrase is an ordered set of 12-24 words used to generate a memorable phrase used for Bitcoin wallet recovery.

In general seed phrases follow the Bitcoin Improvement Proposal (BIP 39) standard found here:
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

The words in the seed phrase are constructed from a range of 12 to 24 of the 2048 words found here:
https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt

NOTE!!! - The order of these words matters. This is an ordered list. When seed phrases are made, words are selected from the number of their position in the list! 

You cannot randomly select a list of 12-24 words. An initial 128-256 bit binary number is used to generate the first 11 words in a 12 word seed phrase, or the first 23 words in a 24 word seed phrase.

The LAST word in the seed phrase is ALWAYS constructed from generating a partial checksum of the final words.

Lets review the method by which valid seed phrases are generated...

### Step 1. Generate a random binary entropy number between 128-256 bits long: ###

To generate our seed phrase we need a binary number, a number consisting of only 0s and 1s. Each 1 or 0 is known as a bit.

We will generate a large random number that will then be used to select our seed words. 

The BIP39 standard states that the random number we generate should be 128 bits long for a 12 word seed phrase, up to 256 bits long for a 24 word seed phrase. Lets focus on a 12 word seed phrase as an example.

Using Python lets write a function to do this (note in the real world we should avoid the use of the random library, because generally they are not always truly random):

```
import random

def generate_random_binary(length):
    binary = ""
    for _ in range(length):
        bit = random.choice(["0", "1"])
        binary += bit
    return binary

random_binary = generate_random_binary(128)
print(random_binary)
```
When running our example this resulted in a random binary number 128 bits long. That's 128 individual 0s 1s making up our number. 

<img width="918" alt="Screenshot 2023-05-06 at 12 08 39 PM" src="https://user-images.githubusercontent.com/46794084/236634982-237cedd7-99a0-48bc-a9d0-391783b93d67.png">


*You will hear the term entropy used when referring to this, it just means we generated a random number. 
Ideally this number is large enough that it is difficult to guess and collision are unlikely to occur when reselecting that number.  

*A 128-bit number has 2^128, two to the power of one hundred twenty-eight possible combinations that is 340,282,366,920,938,463,463,374,607,431,768,211,456.

### Step 2. Chop up our Entropy number into sections 11 bits long: ###

Now we need to chop up our binary number into sections 11 bits long.
*In binary a number 11 bits long will convert to any decimal number between 1 and 2048. Keep that in mind for use in selecting our words here in a minute.

```
list_binary_numbers = [random_binary[i:i+11] for i in range(0, len(random_binary), 11)]
print(list_binary_numbers)
```

This results in the following list of binary numbers 11 bits long, with the exception of the last number which we are going to use here in a minute to generate our entropy:

<img width="201" alt="Screenshot 2023-05-06 at 11 14 05 AM" src="https://user-images.githubusercontent.com/46794084/236632821-d3fff079-947f-43bd-ab3c-48eb26a85330.png">

Notice that the last set of bits in our list is not a full 11 bits long. That last entry is special, we are going to save that for our last step.

### Step 3. Convert each set of bits into its decimal equivalent: ###

We must now convert each set of 11 bits to a binary number between 1 and 2047. 

To do this we iterate over our list, grab an entry, calculate the decimal equivalent and insert it into a new list called list_decimal_numbers:

```
#define a list to store our decimal numbers
list_decimal_numbers = []

#for each binary number we generated in our list
for each_binary_number in list_binary_numbers:
    
    #convert the binary number to decimal
    each_decimal_number = int(each_binary_number, 2)
    #add it to a new list of decimal numbers
    list_decimal_numbers.append(each_decimal_number)

#lets take the 12th item in our list, which is numbered 11 (lists start at 0) we are going to update that to a ? mark right now
list_decimal_numbers[11] = '?'

print(list_decimal_numbers)
```

The results look like this:

<img width="90" alt="Screenshot 2023-05-06 at 1 28 13 PM" src="https://user-images.githubusercontent.com/46794084/236638555-90929f7f-39be-4381-9d41-effe7e115d5c.png">

Ok we almost have the index of the words we need from the BIP39 word list but two more steps. We need to deal with that last set of binary numbers thats only 7 bits long, thats in the next step...

### Step 4. Calculate the 12th binary number: ###

How do we get the last 4 bits to make it into 11 bits for the binary number at position 11 in the list?

This step is broken down into a numer of sub-steps as follows...

#### Sub-step 4.a Generate Sha-256 hash from original 128-bit binary ####

First we take our original entropy number those 128-bits and we run it through the sha-256 hash algorithm.

random_binary = "01100000011111100011001001111101100111101001110001110001001001011010000110010110100110001100111111011011010100111011010001011110"

```
import hashlib
import binascii

hexstr = "{0:0>4X}".format(int(random_binary,2)) 
data = binascii.a2b_hex(hexstr) 
sha_result = hashlib.sha256(data).hexdigest()
print(sha_result)

The sha-256 hash algorithm resulted in the hexadecimal:
f2cead8ce695e058ca4d2e3d04d53aaf5c9365606c651368041a4cea87fae31b

#### Sub-step 4.b Convert first character of our sha-256 hash to 4-bit binary ####

Taking the first character "f" we convert this back to 4 bit binary.

```
# convert the whole sha_result back to binary
binary_number = bin(int(sha_result, 16))[2:].zfill(256)

# Extract the first 4 bits
four_bit_number = binary_number[:4]

print(four_bit_number)
```

The result for character "f" is:
1111

#### Sub-step 4.c Construct our 12th decimal number ####

Remember split our binary numbers up into 11-bit blocks and placed them in a list, but we were left with those 7 binary numbers in the 11th place on our list:

<img width="201" alt="Screenshot 2023-05-06 at 11 14 05 AM" src="https://user-images.githubusercontent.com/46794084/236646862-384955d6-7b63-4706-903c-440ccfcdcbc4.png">

Well we now need to take those 4 bits from the previous step and tag them on the end of the 7 bits back in the 11th position of our original list of binary numbers "list_binary_numbers".

```
#append this onto our list entry
list_binary_numbers[11] = list_binary_numbers[11] + four_bit_number

print(list_binary_numbers[11])
```

We may as well grab the value out of the 11th place in "list_binary_numbers" and add on our last four bits:
1011110 and 1111 resulting in 10111101111 our final 11 bit number.

```
#finally convert this to decimal and put it in the 11 place in our list of decimals replacing the questions mark "?"

#convert the binary number to decimal
final_decimal_number = int(list_binary_numbers[11], 2)

#add it to a new list of decimal numbers
list_decimal_numbers[11] = final_decimal_number
print(list_decimal_numbers)
```
This final result comes up with our complete list of decimal numbers, the first 11 and our last caculated number.

[771, 1932, 1275, 489, 1592, 1174, 1074, 1688, 1662, 1748, 1896, 1519]

#### Sub-step 4.d Getting positional numbers ####


But wait one more piece, since we since representing each 11 bits as a number between 0 and 2047 and the BIP39 wordlist starts at 1 instead of 0) we must add one to each number to get its positional number.

Lets quickly iterate over our list and do this:

#iterate over array and add 1 to each number to get proper positions
for number in range(len(list_decimal_numbers)):
    list_decimal_numbers[number] = list_decimal_numbers[number] + 1

print(list_decimal_numbers)

Our original:
[771, 1932, 1275, 489, 1592, 1174, 1074, 1688, 1662, 1748, 1896, 1519]

Becomes:
[772, 1933, 1276, 490, 1593, 1175, 1075, 1689, 1663, 1749, 1897, 1520]

Make a cup of coffee its time for our final step!

### Step 5. Final step - go grab words from the BIP39 wordlist! ###

This step is very straightforward.

Grab the BIP39 wordlist from here, save it in raw format to a file named bip39.txt:
https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt

We are going to read the contents of the BIP39 wordlist into a dictionary one line at a time, we are going to insert the line numher of each word as the first entry in the dictionary, this is so we maintain the line numbering from the BIP39 wordlist:

```
def read_file_into_dictionary(filename):
    data_dict = {}
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            data_dict[line_number] = line.strip()
    return data_dict

# read the wordlist into our dictionary
filename = 'bip39.txt'  

bip39_dictionary = read_file_into_dictionary(filename)
print(bip39_dictionary)
```

Ok lets iterate over out list of numbers and extract the correct values from the corresponding entry in our dictionary:

```
def retrieve_entries(dictionary, numbers):
    seed_phrase = []
    for number in numbers:
        if number in dictionary:
            seed_phrase.append(dictionary[number])
    return seed_phrase

#returns a list with our final seed phrase in it
final_result = retrieve_entries(bip39_dictionary, list_decimal_numbers)
print(final_result)
```
In our case we generated:

'gather', 'various', 'panda', 'diamond', 'shove', 'name', 'main', 'spread', 'sound', 'surround', 'unfair', 'sadness'

Finally we can proove we got a valid seed phrase by generating a bitcoin address using the Ian Coleman's excellent Menomic Code Coverter at:
https://iancoleman.io/bip39/

### Conclusions ###
-------------------

Since in order to generate a seed phrase we need a 128-256 bit long number to start with, in order to bruteforce wallet addresses attackers would need to go through all possible combinations of bits between 128-256 bits.

If we focus on 12 word seed phrases alone we have said that our 128-bit number can have 2^128 or 340,282,366,920,938,463,463,374,607,431,768,211,456 possible combinations.

That means we would want to iterate through all those binary numbers, generate a seed phrase and then turn it into a bitcoin address. 

Bitcoin address generation will form the next part of my learning, since every wallet seems to generate bitcoin addresses from seed phrases slightly differently.

In our python file I will focus on generating a 12 word seed phrase and will consolidate much of our code into a method generate_bip39_seed() which will recieve a our binary number 128 bits long, it will then return a list containing our 12 word seed phrase.

This function will later be reused in further learnings to generate private keys, public keys and bitcoin addresses using studies on these various means.











