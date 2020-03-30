import random
import math

difficulty = 5

# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
difficultyMapped = int((((difficulty - 1) * (1 -9)) / (10 - 1)) + 9)


expectedAnswer = random.randrange(100, 1000)

expectedAnswerLength = len(str(expectedAnswer))

pAns1 = expectedAnswer
pAns1Res = 0

if expectedAnswerLength == 1:
    expectedAnswerSingles = expectedAnswer%10
    print(expectedAnswerLength,expectedAnswer, expectedAnswerSingles)
    
    while pAns1Res == 0:
        pAns1 = expectedAnswer + random.randrange(-difficultyMapped, difficultyMapped)
        if pAns1 != expectedAnswer and pAns1 > 0:
            pAns1Res = 1
    
    print(pAns1, expectedAnswer)
    
elif expectedAnswerLength == 2:
    expectedAnswerSingles = expectedAnswer%10
    expectedAnswerTens = int(str(expectedAnswer%100)[0])
    print(expectedAnswerLength, expectedAnswer, expectedAnswerTens, expectedAnswerSingles)
    while pAns1Res == 0:
        pAns1 = int(str(expectedAnswerTens + random.randrange(-difficultyMapped, difficultyMapped)) + str(expectedAnswerSingles))
        if pAns1 != expectedAnswer and pAns1 >= 0:
            pAns1Res = 1
    
    print(pAns1, expectedAnswer)
elif expectedAnswerLength == 3:
    expectedAnswerSingles = expectedAnswer%10
    expectedAnswerTens = int(str(expectedAnswer%100)[0])
    expectedAnswerHundreds = str(expectedAnswer)[0]
    print(expectedAnswerLength, expectedAnswer, expectedAnswerHundreds, expectedAnswerTens, expectedAnswerSingles)
    while pAns1Res == 0:
        pAns1 = int(str(int(expectedAnswerHundreds) + random.randrange(-difficultyMapped, difficultyMapped)) + str(expectedAnswerTens) + str(expectedAnswerSingles))
        if pAns1 != expectedAnswer and pAns1 >= 0 and pAns1 < 1000:
            pAns1Res = 1
    
    print(pAns1, expectedAnswer)
