#main method
print("LIST OF TOPICS AVAILABLE\n 1.JAVA\n2.PYTHON\n3.MY SQL\n")
topic=input(print("Enter the topic you wish to take a quiz on: "))
incor int(3) #to store number of incorrect answers
cor int(3) #to store number of correct answers
if (topic=="JAVA"):
    x=input(print("What is the default value of a boolean variable in java?\n a.true\nb.0\nc.false\nd.void"))
    if (x=="c"):
        print("Correct")
    else:
        print("Incorrect")

