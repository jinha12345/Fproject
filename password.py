def passgen(idd):
    if idd is None:
        return ""
    
    #setting
    length = 10

    import random

    seed = ""
    for i in idd:
        seed += str(ord(str(i)))

    random.seed(seed)
    return(str(random.randint(10**(length-1),int("9"*length))))

#jinha12345
#5770097152