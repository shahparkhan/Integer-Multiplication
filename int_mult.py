import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from random import randrange
import math
from time import time, localtime, asctime
import sys



            

def brute_force(x, y, n, m):
    #making result array of size n+m. Result cant have size greater than n+m
    result = [0]*(n + m) 

    #loop on first number    
    for i in range(n-1, -1, -1):
        dig1 = int(x[i])
        
        #loop on second number
        for j in range(m-1, -1, -1):
            #retrieving carry
            carry = int(result[i+j+1])

            dig2 = int(y[j])

            #multiplying
            dig12 = (dig1*dig2) + carry

            carry_l = dig12//10

            carry_r = dig12%10

            #saving result
            result[i+j+1] = carry_r

            #saving carry
            result[i+j] = result[i+j] + carry_l
            
    #removing leading zeros
    while(result[0] == 0):
        result.pop(0)

    #making result string from result array
    return_this = "".join([str(dig) for dig in result])
    
    return return_this






def add_string(x, y, n, m):

    #base case
    if x == "" and y == "":
        return "0"
    
    elif x == "":
        return y
    
    elif y == "":
        return x

    big = ""
    small = ""
    
    #finding longer number in LENGTH
    if (n == m):
        big = x
        big_l = n
        small = y
        small_l = m
    elif (n > m):
        big = x
        big_l = n
        small = y
        small_l = m
    else:
        big = y
        big_l = m
        small = x
        small_l = n

    #creating a result array with length one greater than greatest length 
    temp = "0" + big
    result = [int(x) for x in temp]
    
    #initializing counter for result array 
    counter = big_l

    #making bigger and smaller number of equal length string
    if (big_l != small_l):
        zero_n = big_l - small_l
        small = "0"*(zero_n) + small
        small_l = big_l 
    
    for i in range(small_l-1, -1, -1):
        #retrieving carry
        carry = result[counter]

        dig = int(small[i])

        #adding
        dig12 = dig + carry

        carry_l = dig12//10

        carry_r = dig12%10

        #saving addition result
        result[counter] = carry_r

        counter = counter - 1

        #saving carry
        result[counter] = result[counter] + carry_l

    #making result string from result array    
    return_this = "".join([str(x) for x in result])
    
    #stripping leading zeros
    return_this = return_this.lstrip("0")
    
    return return_this

# function to subtract two numbers as strings
def sub_string(x, y, n, m):
    
    #base case
    if x == "" and y == "":
        return "0"
    
    elif x == "":
        return y
    
    elif y == "":
        return x

    big = ""
    small = ""

    if x == y:
        return "0"

    # finding larger number
    if (n < m):
        big = y
        big_l = m
        small = x
        small_l = n
        small = ("0"*(big_l-small_l)) + small

    else:
        big = x
        big_l = n
        small = y
        small_l = m
        small = ("0"*(big_l-small_l)) + small

    return_this = ""

    #intializing carry
    carry = False


    for i in range(big_l - 1, -1, -1):
        
        # borrowing if answer is in -ve
        if (carry):
            dummy = int(big[i]) - int(small[i]) - 1

        else:
            dummy = int(big[i]) - int(small[i]) 
        
        carry = False

        if dummy < 0:
            dummy = 10 + dummy
            carry = True

        #building answer
        return_this = return_this + str(dummy)


    #reversing answer
    return_this = return_this[::-1]
    
    return return_this





def divide_conquer(x, y):
    #base case

    if (len(x) <= 1) or (len(y) <= 1):
        if x == "" or y == "":
            return "0"
        else:
            return str(int(x)*int(y))
            
    else:
        
        #finding max length
        n = max(len(str(x)), len(str(y)))
        m = n//2
        
        neg_m = m * -1

        #splitting
        a = x[:neg_m]
        b = x[neg_m:]
        c = y[:neg_m]
        d = y[neg_m:]

        #recurssion
        e = divide_conquer(a, c)
        f = divide_conquer(b, d)
        g = divide_conquer(add_string(a, b, len(a), len(b)), add_string(c, d, len(c), len(d)))

        #arithemetic
        m_2 = m*2
        p = e + ("0"*m_2)
        
        q = sub_string(g, f, len(g), len(f))
        q = sub_string(q, e, len(q), len(e))
        q = q + ("0"*m)

        r = add_string(p, q, len(p), len(q))
        r = add_string(r, f, len(r), len(f))
        
        return r
        

def plot():
    
    digits = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    
    times1 = []
    times2 = []

    for digit in digits:

        x = str(randrange((10**(digit-1)), (10**(digit))))
        y = str(randrange((10**(digit-1)), (10**(digit))))
        n = len(x)
        m = len(y)
        
        avg_list = []

        for _ in range(5):
            run_time = time()
            b = brute_force(x, y, n, m)
            run_time = time() - run_time
            run_time = run_time*1000

            print("Brute Force Signal")
            print(asctime(localtime(time())))
            print(digit, ":", run_time)

            avg_list.append(run_time)

        times1.append(np.mean(avg_list))

        avg_list = []

        for _ in range(5):
            run_time = time()
            d = divide_conquer(x, y)
            run_time = time() - run_time
            run_time = run_time*1000

            print("Divide and Conquer Signal")
            print(asctime(localtime(time())))
            print(digit, ":", run_time)

            avg_list.append(run_time)
        
        if b != d:
            print("b d dont match!")
        times2.append(np.mean(avg_list))
        print("Run for", digit, "digit number done!")
        print("\n")
    print(asctime(localtime(time())))
    df = pd.DataFrame({"Digits": digits,
                       "Brute Force": times1,
                       "Divide and Conquer": times2})
        
    print(df)

    _, ax = plt.subplots()
    df.plot(kind="line", x = 'Digits', y=["Brute Force", "Divide and Conquer"], ax=ax, grid = True, linewidth = 5, figsize = (15, 8))
    ax.set_xlabel("Digits of Integer")
    ax.set_ylabel("Time (ms)")
    ax.set_title("Runtime Comaprison Between Brute-Force and Divide and Conquer")
    plt.show()




def main():
    
    # plot()

    algo_name = ""

    while(1):
        algo_name = input("Which algorithm do you want to run\nEnter (B) for Brute Force Algorithm and (D) for Divide and Conque Algorithm. Enter (E) to exit: ")

        if algo_name == "E":
            print("Shutting Down...")
            sys.exit()

        elif algo_name == "B":
            print("We will Run Brute Force Algorithm\n")
            

        elif algo_name == "D":
            print("We will Run Divide and Conquer Algorithm\n")
            
        else:
            print("Invalid Input. Please Enter either B, D, or E\n")
            continue


        number1 = ""
        number2 = ""

        while(1):
            number1 = input("Enter first number: ")
            
            if (not number1.isdecimal()):
            
                print("Input is not a number. Please enter a number\n")

            else:
                print("Number1:", number1, "\n")
                break

        while(1):
            number2 = input("Enter second number: ")
            
            if (not number1.isdecimal()):
            
                print("Input is not a number. Please enter a number\n")

            else:
                print("Number2:", number2, "\n")
                break
        
        result = ""
        if (algo_name == "B"):
            result = brute_force(number1, number2, len(number1), len(number2))

        else:
            result = divide_conquer(number1, number2)
        
        print("Number1 * Number2 =", result)
        print("\n***************************************************************\n")

    

main()