var operation = "add"; // depends on whatever the user chooses
var startingRange = 7;  // level name will be the starting range
var difficulty = startingRange;
var rangeMin;
var rangeMax;
var numOfVariables;
var temp;
var x;
var y;
var z;
var answer;
var correctAnswer = 0;
var incorrectAnswer = 0;
var blank;
var expectedAnswer;
var userAnswer;
var roundNum = 0;

while(roundNum < 10) {
	console.log("Round: ", roundNum+1, "\n");
	// difficulty cant go below starting range - 1
	if(difficulty < startingRange - 1) {
		difficulty = startingRange - 1;
	}
	// difficulty cant go above starting range + 1
	if(difficulty > startingRange + 1) {
		difficulty = startingRange + 1;
	}
	// difficulty cant go below 1
	if(difficulty < 1) {
		difficulty = 1;
	}
	// difficulty cant go above 10
	if(difficulty > 10) {
		difficulty = 10;
	}

	// 0 - 990
	if(operation == "add") {
		// decide how many variables will be used in the equations
		numOfVariables = randomInRange(3, 4);
		
		rangeMin = difficulty * 9;
		rangeMax = difficulty * 99;
	}
	// 0 - 990
	else if(operation == "subtract") {
		numOfVariables = 3;
		
		rangeMin = difficulty * 5;
		rangeMax = difficulty * 55;
	} 
	// 0 - 20
	else if(operation == "divide") {
		numOfVariables = 3;
	  
		rangeMin = 0;
		rangeMax = difficulty * 2;
		// console.log("in divide", difficulty, rangeMin, rangeMax);
	}
	// 0 - 12
	else if(operation == "multiply") {
		numOfVariables = 3;
	  
	  rangeMin = Math.round(difficulty + (difficulty * 0.6));
	  rangeMax = Math.round(difficulty * 1.2);
	}

	// console.log(randomInRange(rangeMin, rangeMax));

	// verify the numbers work in the equation
	getEquationNumbers(numOfVariables, operation);

	// give the user all of the numbers of the equation except one and have them type the correct answer to the missing box.
	if(numOfVariables == 3) {
		blank = randomInRange(0,2);
		
		switch(blank) {
			case 0:
				if(operation == "add") {
					console.log("? + ", y, " = ", answer);
					expectedAnswer = x;
				}
				if(operation == "subtract") {
					console.log("? - ", y, " = ", answer);
					expectedAnswer = x;
				}
				if(operation == "multiply") {
					console.log("? * ", y, " = ", answer);
					expectedAnswer = x;
				}
				if(operation == "divide") {
					console.log("? / ", y, " = ", answer);
					expectedAnswer = x;
				}
				break;
			case 1:
				if(operation == "add") {
					console.log(x, " + ? = ", answer);
					expectedAnswer = y;
				}
				if(operation == "subtract") {
					console.log(x, " - ? = ", answer);
					expectedAnswer = y;
				}
				if(operation == "multiply") {
					console.log(x, " * ? = ", answer);
					expectedAnswer = y;
				}
				if(operation == "divide") {
					console.log(x, " / ? = ", answer);
					expectedAnswer = y;
				}
				break;
			case 2:
				if(operation == "add") {
					console.log(x, " + ", y, " = ?");
					expectedAnswer = answer;
				}
				if(operation == "subtract") {
					console.log(x, " - ", y, " = ?");
					expectedAnswer = answer;
				}
				if(operation == "multiply") {
					console.log(x, " * ", y, " = ?");
					expectedAnswer = answer;
				}
				if(operation == "divide") {
					console.log(x, " / ", y, " = ?");
					expectedAnswer = answer;
				}
				break;
		}
	}
	else {
		blank = randomInRange(0,3);
		
		switch(blank) {
			case 0:
				if(operation == "add") {
					console.log("? + ", y, " + ", z, " = ", answer);
					expectedAnswer = x;
				}
				break;
			case 1:
				if(operation == "add") {
					console.log(x, " + ? + ", z, " = ", answer);
					expectedAnswer = y;
				}
				break;
			case 2:
				if(operation == "add") {
					console.log(x, " + ", y, " + ? = ", answer);
					expectedAnswer = z;
				}
				break;
			case 3:
				if(operation == "add") {
					console.log(x, " + ", y, " + ", z, " = ?");
					expectedAnswer = answer;
				}
				break;
		}
	}

	userAnswer = prompt("what is the answer?");
	// if they get the answer correct then add 1 to the correct answers var and increase the range
	if(userAnswer == expectedAnswer) {
		console.log("you got the answer right");
		correctAnswer++;
		difficulty += 1;
	}
	// if they get the answer wrong thena dd 1 to the incorrect answers var and decrease the range
	else {
		console.log("you got the answer wrong");
		incorrectAnswer++;
		difficulty -= 1;
	}
	
	roundNum += 1;
}
console.log("game over");
console.log("correct: ", correctAnswer);
console.log("incorrect: ", incorrectAnswer);

function randomInRange(min, max) {
  return Math.round(Math.random() * (max - min) + min);
}

function getEquationNumbers(numOfVariables, operator) {
	var possibleAnswer = false;

	while (possibleAnswer === false) {
  	if(operator == "add") {
    	if(numOfVariables == 4) {
      	x = randomInRange(rangeMin, rangeMax);
        y = randomInRange(rangeMin, rangeMax);
        z = randomInRange(rangeMin, rangeMax);
        answer = x + y + z;
		// console.log("got an answer: ", answer, " = ", x, " + ", y, " + ", z);
      }
      else {
		x = randomInRange(rangeMin, rangeMax);
      	y = randomInRange(rangeMin, rangeMax);
      	answer = x + y;
		// console.log("got an answer: ", answer, " = ", x, " + ", y);
      }
	  
	  if(answer < 1000) {
		  possibleAnswer = true;
	  }
    }
    if(operator == "subtract") {
		x = randomInRange(rangeMin, rangeMax);
		y = randomInRange(rangeMin, rangeMax);
      
      if(x >= y) {
      	answer = x - y;
        possibleAnswer = true;
		// console.log("got an answer: ", answer, " = ", x, " - ", y);
      }
      else {
      	answer = y - x;
        possibleAnswer = true;
		// console.log("got an answer: ", answer, " = ", y, " - ", x);
      }
    }
    if(operator == "multiply") {
		x = randomInRange(rangeMin, rangeMax);
		y = randomInRange(rangeMin, rangeMax);
		answer = x * y
		possibleAnswer = true;
		// console.log("got an answer: ", answer, " = ", x, " * ", y);
    }
    if(operator == "divide") {
		x = randomInRange(rangeMin, rangeMax);
		y = randomInRange(rangeMin, rangeMax);
     	if(x >= y) {
			if(x % y == 0) {
			answer = x / y;
			possibleAnswer = true;
			// console.log("got an answer: ", answer, " = ", x, " / ", y);
		}
        else {
        	// need new variables that are evenly divisible by each other
			console.log("not possible");
        }
      }
      else {
		  temp = x;
		  x = y;
		  y = temp;
      	if(x % y == 0) {
			answer = x / y;
			possibleAnswer = true;
			// console.log("got an answer: ", answer, " = ", x, " / ", y);
        }
        else {
			// need new variables that are evenly divisible by each other
			console.log("not possible");
        }
      }
   	}
  }
}