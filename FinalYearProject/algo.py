import random
import globalVariables


def algo(op, level):

    operation = op
    startingRange = level
    difficulty = startingRange
    rangeMin = None
    rangeMax = None
    correctAnswer = 0
    incorrectAnswer = 0
    expectedAnswer = None
    userAnswer = None
    roundNum = 0

    def randomInRange(min, max):
        return random.randrange(min, max + 1)

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
        numOfVariables = 3

        rangeMin = difficulty * 9
        rangeMax = difficulty * 99

    elif operation == "subtract":
        numOfVariables = 3

        rangeMin = difficulty * 5
        rangeMax = difficulty * 50

    elif operation == "divide":
        numOfVariables = 3

        rangeMin = 1
        rangeMax = difficulty * 3

    elif operation == "multiply":
        numOfVariables = 3

        rangeMin = 1
        rangeMax = difficulty * 3

    # verify if the numbers will work in the equation
    possibleAnswer = False

    while not possibleAnswer:
        if operation == "add":
            if numOfVariables == 4:
                globalVariables.x = randomInRange(rangeMin, rangeMax)
                globalVariables.y = randomInRange(rangeMin, rangeMax)
                globalVariables.z = randomInRange(rangeMin, rangeMax)
                globalVariables.answer = globalVariables.x + globalVariables.y + globalVariables.z
            else:
                globalVariables.x = randomInRange(rangeMin, rangeMax)
                globalVariables.y = randomInRange(rangeMin, rangeMax)
                globalVariables.answer = globalVariables.x + globalVariables.y

            if globalVariables.answer < 1000:
                possibleAnswer = True

        if operation == "subtract":
            globalVariables.x = randomInRange(rangeMin, rangeMax)
            globalVariables.y = randomInRange(rangeMin, rangeMax)

            if globalVariables.x >= globalVariables.y:
                globalVariables.answer = globalVariables.x - globalVariables.y
                possibleAnswer = True
            else:
                temp = globalVariables.x
                globalVariables.x = globalVariables.y
                globalVariables.y = temp
                globalVariables.answer = globalVariables.x - globalVariables.y
                possibleAnswer = True

        if operation == "multiply":
            globalVariables.x = randomInRange(rangeMin, rangeMax)
            globalVariables.y = randomInRange(rangeMin, rangeMax)
            globalVariables.answer = globalVariables.x * globalVariables.y
            possibleAnswer = True

        if operation == "divide":
            globalVariables.x = randomInRange(rangeMin, rangeMax)
            globalVariables.y = randomInRange(rangeMin, rangeMax)

            if globalVariables.x >= globalVariables.y == 0:
                if globalVariables.x % globalVariables.y == 0:
                    globalVariables.answer = globalVariables.x / globalVariables.y
                    possibleAnswer = True
            else:
                temp = globalVariables.x
                globalVariables.x = globalVariables.y
                globalVariables.y = temp

                if globalVariables.x % globalVariables.y == 0:
                    globalVariables.answer = globalVariables.x / globalVariables.y
                    possibleAnswer = True

    # give the users all of the numbers of the equation except one and have them enter the missing number
    if numOfVariables == 3:
        globalVariables.blank = randomInRange(0, 2)

        if globalVariables.blank == 0:
            if operation == "add":
                print("? + ", globalVariables.y, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.x
            if operation == "subtract":
                print("? - ", globalVariables.y, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.x
            if operation == "multiply":
                print("? * ", globalVariables.y, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.x
            if operation == "divide":
                print("? / ", globalVariables.y, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.x
        elif globalVariables.blank == 1:
            if operation == "add":
                print(globalVariables.x, " + ? = ", globalVariables.answer)
                expectedAnswer = globalVariables.y
            if operation == "subtract":
                print(globalVariables.x, " - ? = ", globalVariables.answer)
                expectedAnswer = globalVariables.y
            if operation == "multiply":
                print(globalVariables.x, " * ? = ", globalVariables.answer)
                expectedAnswer = globalVariables.y
            if operation == "divide":
                print(globalVariables.x, " / ? = ", globalVariables.answer)
                expectedAnswer = globalVariables.y
        elif globalVariables.blank == 2:
            if operation == "add":
                print(globalVariables.x, " + ", globalVariables.y, " = ?")
                expectedAnswer = globalVariables.answer
            if operation == "subtract":
                print(globalVariables.x, " - ", globalVariables.y, " = ?")
                expectedAnswer = globalVariables.answer
            if operation == "multiply":
                print(globalVariables.x, " * ", globalVariables.y, " = ?")
                expectedAnswer = globalVariables.answer
            if operation == "divide":
                print(globalVariables.x, " / ", globalVariables.y, " = ?")
                expectedAnswer = globalVariables.answer

    else:
        globalVariables.blank = randomInRange(0, 3)

        if globalVariables.blank == 0:
            if operation == "add":
                print("? + ", globalVariables.y, " + ", globalVariables.z, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.x
        elif globalVariables.blank == 1:
            if operation == "add":
                print(globalVariables.x, " + ? + ", globalVariables.z, " = ", globalVariables.answer)
                expectedAnswer = globalVariables.y
        elif globalVariables.blank == 2:
            if operation == "add":
                print(globalVariables.x, " + ", globalVariables.y, " + ? = ", globalVariables.answer)
                expectedAnswer = globalVariables.z
        elif globalVariables.blank == 3:
            if operation == "add":
                print(globalVariables.x, " + ", globalVariables.y, " + ", globalVariables.z, " = ?")
                expectedAnswer = globalVariables.answer