def algo(op, level):
    operation = op
    startingRange = level
    difficulty = startingRange
    rangeMin = None
    rangeMax = None
    numOfVariables = None
    temp = None
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

    while roundNum < 10:
        print("round: ", roundNum+1, "\n")
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
            