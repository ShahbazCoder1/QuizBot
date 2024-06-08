#main method
print("LIST OF TOPICS AVAILABLE\n 1.JAVA\n2.PYTHON\n3.MY SQL\n")
topic=input(print("Enter the topic you wish to take a quiz on: "))
incor=0 #to store number of incorrect answers
cor=0 #to store number of correct answers
if (topic=="JAVA"):
    x=input(print("What is the default value of a boolean variable in java?\n a.true\nb.0\nc.false\nd.void"))
    if (x=="c"):
        print("Correct")
        cor++
    else:
        print("Incorrect")
        incor++
    
    x=input(print("Which of the following is not a primitive data type in Java?\na.int\nb.char\nc.String\nd.None of the above"))
    if(x==c):
        print("Correct")
        cor++
    else:
        print("Incorrect")
        incor++
    x=input(print("Which method is called when an object is created in Java?\na.constructor\nb.finalize()\nc.main()\nd.int()"))
    if(x==a):
        print("Correct")
        cor++
    else:
        print("Incorrect")
        incor++
    x=input(print("What is the size of an int variable in Java?\na.int\nb.char\nc.String\nd.None of the above"))
    if(x==c):
        print("Correct")
        cor++
    else:
        print("Incorrect")
        incor++

#elif (topic=="PYTHON"):
    



