# alphabet.py

# 1. Design an application which is able to find the alphabet of a given sequence. The alphabet means 
# the unique symbols from which the sequence is made.
# Eg. sequence S='ATTGCCCCGAAT'
# find the alphabet of the sequence.

seq = input("Enter sequence: ")
alphabet = sorted(set(seq.upper()))
print("Alphabet:", alphabet)
