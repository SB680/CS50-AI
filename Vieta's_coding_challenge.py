#findpolynomialgivenitsroots uses Vieta's equations to find the coefficients of a polynomial given its roots 
#Given guesses for a polynomial's roots and its actual roots, this program can find the euclidean norm of the difference between the actual and estimated values of
#the right hand side of Vieta's equations and the estimated and actual coefficients 
import time

def findsumcombalist(alist,x): #recursively finds the sum of all possible combinations of x of the elements of an arbitrary list of real and/or complex numbers
    #for example, if alist = [1,3,4,2] and x = 2, then summation = 1*3+1*4+1*2+3*4+3*2+4*2 = 35 
    if type(alist) == list: 
        n = len(alist)  
    else:
        n = 1
    summation = 0
    if x == 1: 
        if type(alist) == list: 
            return sum(alist) 
        else:
            return alist #the sum is alist if alist is a single number 
    else: 
        for i in range(n-2,-1,-1):  
            summation+=alist[i+1]*findsumcombalist(alist[0:i+1],x-1)  
    return summation

def findpolynomialgivenitsroots(roots,coefffirstterm): #determines a polynomial's coefficients given its roots and the coefficient of its highest degree term
    #this function considers only the polynomial of least degree that has the roots specified. Each root must be included in roots as many times as its muliplicity is.  
    polynomial = [] #the coefficients are in descending order of the degree
    poldeg= len(roots)-1
    coefficients = [coefffirstterm] #first term is the highest degree term 
    for i in range(1,poldeg+2):
        ithcoefficient = coefffirstterm*findsumcombalist(roots,i)*pow(-1,i)
        coefficients.append(ithcoefficient)
    return coefficients 

coeffoffirstterm = 1 
#roots = [2,2,5,6.5,6.5,6.5,15,32.3,67.2]
roots = [2,5,6.5,15,32.3,67.2]
start_time = time.time()
print("The coefficients of the polynomial with these roots are ",findpolynomialgivenitsroots(roots,coeffoffirstterm)) 
print("--- %s seconds ---" % (time.time() - start_time))

##def findeuclideannormofdifference(a,b):
##    return (sum(pow(b[i]-a[i],2) for i in range(len(a))))**0.5 #the two vectors must be of the same length
## 
##polcoeff = [1,-13.5,55.5,-65] #corresponds to x^3-13.5x^2+55.5x-65, which has roots 2,5 and 6.5 
##guesses = [2,5.5,6.2] #if the guesses are the actual roots of the polynomial, the euclidean norm of the difference will be 0 and everything else will match   
##poldeg = len(polcoeff) - 1 #polynomial's degree 
##estimatedcoeff =[polcoeff[0]] #the coefficient of the highest degree term or a point the polynomial passes through must be known to estimate its coefficients based on guesses of its roots
##actualvalues = []; estimates=[]
###actualvalues and estimates are the actual and estimated values of the right hand side of Vieta's equations 
###Values of (-1)^k*a_k/a_n based on the guesses for the roots and actual values of the coefficients should match as the guesses become more accurate 
##
##for i in range(1,poldeg+1): 
##    estimate = findsumcombalist(guesses,i); #ith value of the left hand side of Vieta's equations, estimated based on the guesses for the roots  
##    actualvalue = pow(-1,i)*polcoeff[i]/polcoeff[0] #ith true value of the left hand side of Vieta's equations
##    actualvalues.append(actualvalue); estimates.append(estimate) 
##    estimatedcoeff.append(actualvalue*pow(-1,i)*polcoeff[0]) 
##    
##eucnorm = findeuclideannormofdifference(actualvalues,estimates)
##
##print("The actual values of the right hand side of Vieta's equations are ", actualvalues) 
##print("The estimated values of the right hand side of Vieta's equations are ", estimates) 
##print("The euclidean norm of the difference between the actual and estimated values of the right hand side of the Vieta's formulas is ",eucnorm) 
##print("The estimated values of the polynomial's coefficients based on the guesses for the roots are: ", estimatedcoeff) #this assumes the coefficient of the highest degree term is known 
##print("The actual values of the polynomial's coefficients are: ", polcoeff)


    

