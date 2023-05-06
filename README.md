# Study_BIP39_SeedPhrases
A study on constructing valid BIP39 seed phrases for use in Bitcoin wallet recovery

Intro
------

A seed phrase is an ordered set of 12-24 words used to generate a memorable phrase used for Bitcoin wallet recovery.

In general seed phrases follow the Bitcoin Improvement Proposal (BIP 39) standard found here:
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

The words in the seed phrase is constructed from the the 2048 words in the BIP39 word list found here:
https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt

NOTE!!! - The order of these words matters. This is an ordered list. When seed phrases are made, words are selected from the number of their position in the list!

Many hackers try and bruteforce the bitcoin wallet recovery phrase by randomly selecting combinations of 12-24 words from the list and spraying these against a wallet app. This often results in a high rate of error given the method in which valid seed phrases must be constructed.

The LAST word in the seed phrase is ALWAYS constructed from the previous words. 
Lets review the method by which valid seed phrases are generated...

Step 1. Generate a random binary entropy number between 128-256 bits long:
--------------------------------------------------------------------------

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

Step 2. Chop up our Entropy number into sections 11 bits long:
--------------------------------------------------------------

Now we need to chop up our binary number into sections 11 bits long.
*In binary a number 11 bits long will convert to any decimal number between 1 and 2048. Keep that in mind for use in selecting our words here in a minute.

```
sections = [random_binary[i:i+11] for i in range(0, len(random_binary), 11)]
print(sections)
```

This results in the following list of binary numbers 11 bits long, with the exception of the last number which we are going to use here in a minute to generate our entropy:

<img width="201" alt="Screenshot 2023-05-06 at 11 14 05 AM" src="https://user-images.githubusercontent.com/46794084/236632821-d3fff079-947f-43bd-ab3c-48eb26a85330.png">

Notice that the last set of bits in our list is not a full 11 bits long. That last entry is special, we are going to save that for our last step.

Step 3. Convert each set of bits into its for the first 11 set of bits:
---------------------------------------------------------------------------

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

Calculate the 12th word - the partial checksum
----------------------------------------------

How do we get the last 4 bits to make it into 11 bits for the binary number at position 11 in the list?

<img width="106" alt="Screenshot 2023-05-06 at 1 37 44 PM" src="https://user-images.githubusercontent.com/46794084/236638913-d0d1ed0d-0363-404d-9e71-91e453892053.png">

First we take our original entropy number those 128-bits and we run it through the sha-256 hash algorithm.

random_binary = "01100000011111100011001001111101100111101001110001110001001001011010000110010110100110001100111111011011010100111011010001011110"

here==============

The checksum is generated by hashing our entropy number. The hash employed in BIP39 seed phrases is known as SHA-256, this was originally developed by the NSA and is used widely by bitcoin.

The sha-256 hash algorithm results in a hexadecimal number:

ced25fa131e86640ffc9517b590f84877e40ad20f7f1ae88707ec79945d0d45

To complete our seed phrase we now:
1. Take the first hexadecimal character 'c' and convert that back to binary 1100
2. We take those 4 bits and 1100 and tage them on the end of the last 7 bits to find the position of our last word: 2044

*A 24 word seed would have 8 bits from two 4 digit binary numbers that would be added to the leftover 3 bits for a total of 11 bits.

Now using the BIP39 wordlist, we can look up the word corresponding to its position in the list. 
*Note we are using 11 bits representing a number between 0 and 2047, so we must add 1 to the position found.

11011010010 = 1747 = surge
00010110010 = 179 = bind
11110010011 = 1940 = venue
10010000111 = 1160 = movie
11100001001 = 1802 = thrive
01000000011 = 516 = document
00001101001 = 106 = artwork
10010100101 = 1190 = net
11100111110 = 1855 = treat
01000010001 = 530 = drama
01011000010 = 707 = flame
1111111 = 2045 = zebra

Now we have our 12 word seed phrase:

surge bind venue movie thrive document artwork net treat drama flame zebra

Combintions












