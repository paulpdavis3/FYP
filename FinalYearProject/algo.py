import random

def algo(op, level):

    global x
    global y
    global z
    global answer

    operation = op
    startingRange = level
    difficulty = startingRange
    rangeMin = None
    rangeMax = None
    numOfVariables = None
    x = None
    y = None
    z = None
    answer = None
    correctAnswer = 0
    incorrectAnswer = 0
    blank = None
    expectedAnswer = None
    userAnswer = None
    roundNum = 0

    def randomInRange(min, max):
        return random.randrange(min, max + 1)

    while roundNum < 10:
        print("round: ", roundNum + 1)
        # difficulty can't go below starting range - 1
        if difficulty < startingRange - 1:
            difficulty = startingRange - 1
        # difficulty can't go above starting range + 1
        if difficulty > startingRange + 1:
            difficulty = startingRange + 1
        # difficulty can't go below 1
        if difficulty < 1:
            difficulty = 1
        # difficulty can't go above 10
        if difficulty > 10:
            difficulty = 10

        if operation == "add":
            # decide how many variables will be used in the equation
            numOfVariables = randomInRange(3, 4)

            rangeMin = difficulty * 9
            rangeMax = difficulty * 99

        elif operation == "subtract":
            numOfVariables = 3

            rangeMin = difficulty * 5
            rangeMax = difficulty * 55

        elif operation == "divide":
            numOfVariables = 3

            rangeMin = 1
            rangeMax = difficulty * 2

        elif operation == "multiply":
            numOfVariables = 3

            rangeMin = 1
            rangeMax = difficulty * 2

        # verify if the numbers will work in the equation
        possibleAnswer = False

        while not possibleAnswer:
            if operation == "add":
                if numOfVariables == 4:
                    x = randomInRange(rangeMin, rangeMax)
                    y = randomInRange(rangeMin, rangeMax)
                    z = randomInRange(rangeMin, rangeMax)
                    answer = x + y + z
                else:
                    x = randomInRange(rangeMin, rangeMax)
                    y = randomInRange(rangeMin, rangeMax)
                    answer = x + y

                if answer < 1000:
                    possibleAnswer = True

            if operation == "subtract":
                x = randomInRange(rangeMin, rangeMax)
                y = randomInRange(rangeMin, rangeMax)

                if x >= y:
                    answer = x - y
                    possibleAnswer = True
                else:
                    temp = x
                    x = y
                    y = temp
                    answer = x - y
                    possibleAnswer = True

            if operation == "multiply":
                x = randomInRange(rangeMin, rangeMax)
                y = randomInRange(rangeMin, rangeMax)
                answer = x * y
                possibleAnswer = True

            if operation == "divide":
                x = randomInRange(rangeMin, rangeMax)
                y = randomInRange(rangeMin, rangeMax)

                if x >= y == 0:
                    if x % y == 0:
                        answer = x / y
                        possibleAnswer = True
                else:
                    temp = x
                    x = y
                    y = temp

                    if x % y == 0:
                        answer = x / y
                        possibleAnswer = True

        # give the users all of the numbers of the equation except one and have them enter the missing number
        if numOfVariables == 3:
            blank = randomInRange(0, 2)

            if blank == 0:
                if operation == "add":
                    print("? + ", y, " = ", answer)
                    expectedAnswer = x
                if operation == "subtract":
                    print("? - ", y, " = ", answer)
                    expectedAnswer = x
                if operation == "multiply":
                    print("? * ", y, " = ", answer)
                    expectedAnswer = x
                if operation == "divide":
                    print("? / ", y, " = ", answer)
                    expectedAnswer = x
            elif blank == 1:
                if operation == "add":
                    print(x, " + ? = ", answer)
                    expectedAnswer = y
                if operation == "subtract":
                    print(x, " - ? = ", answer)
                    expectedAnswer = y
                if operation == "multiply":
                    print(x, " * ? = ", answer)
                    expectedAnswer = y
                if operation == "divide":
                    print(x, " / ? = ", answer)
                    expectedAnswer = y
            elif blank == 2:
                if operation == "add":
                    print(x, " + ", y, " = ?")
                    expectedAnswer = answer
                if operation == "subtract":
                    print(x, " - ", y, " = ?")
                    expectedAnswer = answer
                if operation == "multiply":
                    print(x, " * ", y, " = ?")
                    expectedAnswer = answer
                if operation == "divide":
                    print(x, " / ", y, " = ?")
                    expectedAnswer = answer

        else:
            blank = randomInRange(0, 3)

            if blank == 0:
                if operation == "add":
                    print("? + ", y, " + ", z, " = ", answer)
                    expectedAnswer = x
            elif blank == 1:
                if operation == "add":
                    print(x, " + ? + ", z, " = ", answer)
                    expectedAnswer = y
            elif blank == 2:
                if operation == "add":
                    print(x, " + ", y, " + ? = ", answer)
                    expectedAnswer = z
            elif blank == 3:
                if operation == "add":
                    print(x, " + ", y, " + ", z, " = ?")
                    expectedAnswer = answer

        acceptableAnswer = False

        while not acceptableAnswer:
            try:
                userAnswer = int(input("What's the answer?\n"))
                acceptableAnswer = True
            except ValueError:
                print("Make sure you enter a valid number\n")

        if expectedAnswer == userAnswer:
            print("You got the answer right")
            correctAnswer += 1
            difficulty += 1
        else:
            print("You got the answer wrong")
            incorrectAnswer += 1
            difficulty -= 1

        roundNum += 1

    print("game over\n")
    print(correctAnswer, "answers correct ", incorrectAnswer, "answers incorrect")