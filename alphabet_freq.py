# alphabet_freq.py

#2. Design an application which is able to calculate the relative frequencies of each symbol from the
#   alphabet of the sequence. Use the same sequence as before.

seq = input("Enter sequence: ").upper()   
length = len(seq)

alphabet = sorted(set(seq))               
print("Alphabet:", alphabet)

print("Relative frequencies:")
for symbol in alphabet:
    freq = seq.count(symbol) / length
    print(f"{symbol}: {freq:.3f}")       

