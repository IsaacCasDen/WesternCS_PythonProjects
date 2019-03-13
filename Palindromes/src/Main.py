
import random

def is_palindrome(items:list):
    value = (items == list(reversed(items)))
    return value

def find_palindrome(list:list,center:int):
    value = None
    if list == None or len(list)==1 or center<0 or center>(len(list)-2):
        return value

    if center == 0 or center == (len(list)-2):
        if list[center]==list[center+1]:
            value = list[center:center+2]
    else:
        if list[center] == list[center+1]:
            bounds = [0,1]
        elif is_palindrome(list[center-1:center+2]):
            bounds = [1,1]
        else:
            bounds = None

        if bounds == None:
            return value

        while bounds[0]>=0 and bounds[1]<len(list) and is_palindrome(list[center-bounds[0]:center+bounds[1]+1]):
            value = list[center-bounds[0]:center+bounds[1]+1]
            bounds[0]+=1
            bounds[1]+=1

    if value == None:
        return None
    else:
        return (len(value),value)

def palindromes(list:list):
    value = [(0,None)]
    if list == None:
        return value
    for c in range(0,len(list)-1):
        val = find_palindrome(list,c)
        if val!=None:
            value.append(val)

    if len(value)>1:
        value = value[1:]
    return value

def palindrome(list:list):
    if list!=None:
        data = palindromes(list)
        data.sort(key=lambda x: x[0], reverse=True)
        size = 0
        result = []

        for i in range(len(data)):
            if size == 0 or data[i][0] == size:
                size=data[i][0]
                result.append(data[i][1])
            else:
                break

        return (size,result)


if __name__ == "__main__":
    palind_r = [ random.randint(-10,10) for i in range(20) ]
    palind_l = list(reversed(palind_r))
    palind = palind_l + palind_r
    sample = [ random.randint(-10,10) for i in range(500) ] + palind + [ random.randint(-10,10) for i in range(500) ]

    #result = palindrome([3, 42, 1, 1, 42, 3])
    result = palindrome(sample)
    #result = palindrome(palindromes([3, 42, 1, 7, 1, 42, 6, 3, 42, 1, 7, 1, 42, 3, 3, 41, 1, 7, 1, 42, 3]))
    if result != None:
        print(result)