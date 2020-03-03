import hashlib

while(True):
    mystring = input("enter string\n")
    temp = hashlib.sha256(mystring.encode())
    temp = temp.hexdigest()
    print(temp)
