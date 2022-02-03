# Written by Patrick Keener on 10/05/2020; Video recorded on 10/08/2020
# Video Link: https://youtu.be/76mp1YUv4rQ
# Honor Statement:  "I have not given or received any unauthorized assistence 
#                    on this assignment"
# 



def dispResults(testNum, prime, happy):
    """ Displays results for Happy Primes
    
    Keyword Arguments:
    prime - Boolean, indicates whether the number is prime
    happy - Boolean, indicates whether the number is happy
    
    Output:
    Prints whether the number is prime and happy
    """

    if prime == True:
        prime = 'prime'
    else:
        prime = 'not prime'
    
    if happy == True:
        happy = 'happy :)'
    else:
        happy = 'not happy :('

    print('The number {} is {} and is {}'.format(testNum, prime, happy))

    return None


def primeTest(testNum):
    """ This function will determine whether the number is prime.
    A number is considered prime if it is only divisible by 1 and itself

    Keyword Arguments:
    testNum - Integer that is being evaluated as a happy prime

    Returns:
    Boolean - Indicates whether the number is prime or not
    """

    if testNum % 2 == 0: return False  # check if even
        
    for num in range(3, testNum, 2): # iterate on odds to evaluate if # is prime
        if testNum % num == 0: return False

    return True


def getDigits(newNum):
    """ This function will find the digit in each place of the number

    Keyword Arguments:
    newNum - Integer that will be broken into its constituent pieces

    Returns:
    digitList - a list of each digit
    """

    # How to get the number in each place: 
    # My initial thought was to find the number of digits n = (log10(x)) then 
    # iterate # n times, dividing the number by num % 10^(n-1) each time, however I 
    # did additional research and found a solution that doesn't involve exponents
    # and therefore should be computationally faster that I have chosen to use.  
    # This solution simply divides by 10
    # https://stackoverflow.com/questions/32752750/how-to-find-the-numbers-in-the-thousands-hundreds-tens-and-ones-place-in-pyth

    digitList = list()

    while newNum >= 1:
        digitList.append(newNum % 10) # append the last digit
        newNum //= 10 # remove last digit from number
    
    return digitList


def nextNum(newNum):
    """ This function finds the next number in the sequence

    Keyword Arguements:
    newNum - the test number in the previous case

    Returns:
    nextNum - the next number in the sequence
    """

    digitList = getDigits(newNum) # Get the list of digits
    nextNum = sum([x**2 for x in digitList]) # square each number & sum list

    return nextNum


def happyTest(testNum):
    """ This function will determine whether the number is happy.
    A number is happy if it meets the following criteria:
    * starting iwth any positive integer
    * sum the square of the digits
    * --
    * if it ends in 1 it is happy
    * if it ends in an infinite loop it is not happy

    Keyword Arguments:
    testNum - Integer that is being evaluated as a happy prime

    Returns:
    Boolean - Indicates whether the number is happy or not
    """

    newNum = testNum
    previousNumbers = set()
    
    while True:
        previousNumbers.add(newNum) # record numbers for exit condition
        newNum = nextNum(newNum) 

        if newNum == 1: return True # Happy :)
        if newNum in previousNumbers: return False # Sad :(

    return False


def happyPrimes(testNum):
    """ This program will find happy primes as defined in the assignment
    
    Keyword Arguments:
    testNum - an integer that will be tested to see if it is happy

    Output:
    Prints whether the number is prime and happy 
    """
    # Initialize variables
    prime = False
    happy = False

    prime = primeTest(testNum) # Determine if the # is prime
    happy = happyTest(testNum) # Determine if the number is happy
    dispResults(testNum, prime, happy) # Display the results

    return None


#happyPrimesTest = [1, 3, 7, 9, 13, 15, 17, 27, 29, 31, 97, 100]

#for n in happyPrimesTest:
happyPrimes(n)





# Video Transcript

# My name is Patrick Keener and this is DSC 430- Python Programming, 
# Assignment 6 - Happy Primes.  A transcript of this video can be found at the 
# bottom of the code.

# I have implemented a loop to call the program several times to show how it 
# works.  This functionality will be commented out in the submitted version.

# Top-down design resulted in more readable code by helping organize the 
# functions and abstract the problems.  I have found that I can write the code 
# faster when using top-down design, even though more time is spent on the 
# planning phase. Additionally, the problems are simplified through abstraction- 
# one large problem becomes many small problems, and the small problems can be 
# solved fairly easily.

# I started with the main module, HappyPrimes, which controls program execution.  
# This was subdivided into determining whether the number was prime, then happy, 
# then displaying the results.

# The Prime test is rather simple- it tests for divisibility by 2, then checks 
# whether it is divisible by all odd numbers.  If we knew we would run this 
# program several times I'd likely include memoisation of the primes, similar to 
# how I did it in assignment 5.

# Happy test is more detailed.  I begin by initiating the variables.  I track 
# the previous numbers encountered in a set, which in python is implemented as a 
# hash table.  This allows for the speed of a hash table without the cumberance 
# of a dictionary; I only need to check for a 1:1 relationship so a key/value 
# set-up adds unnecessary functionality that will need to be coded around, 
# therefore I opted to use a set.

# Determining the next number in the series required some problem solving.  
# Originally I had planned to use a scheme wehrein I'd find the number of digits 
# by taking the base 10 logarithm then iterating n times, dividing the number by 
# 10 to the n-1 each time until I ended up with no more numbers, however I found 
# a much more elegant solution on stackOverFlow that I chose to implement.  I 
# start by getting the list of digits, which is accomplished by repeatedly 
# dividing the number by 10 and appending the whole number to a list, then 
# subsequently removing that number until there are no remaining digits.

# Once I get he list of digits, I square them using a list comprehension and sum 
# the results, which yields the next number. if the next number == 1 then the 
# number is happy, and if it is not but it is in the set of previous numbers 
# then it is false.  If neither, the loop executes again.

# Finally, once the number's happy/prime state is determined, the happyPrimes 
# function calls the dispResults function, which prints the results.