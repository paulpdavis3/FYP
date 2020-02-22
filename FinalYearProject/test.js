var operation = "subtract"; // depends on whatever the user chooses
var startingRange = 7;  // level name will be the starting range
var difficulty = startingRange;
var rangeMin;
var rangeMax;
var numOfVariables;
var x;
var y;
var z;
var answer;
var correctAnswer = 0;
var incorrectAnswer = 0;

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
// if they get the answer correct then add 1 to the correct answers var
// if they get the answer wrong thena dd 1 to the incorrect answers var
// games should last 10 rounds
// increase the range if the answer is correct
// decrease the range if the answer is incorrect

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
		console.log("got an answer: ", answer, " = ", x, " + ", y, " + ", z);
      }
      else {
		x = randomInRange(rangeMin, rangeMax);
      	y = randomInRange(rangeMin, rangeMax);
      	answer = x + y;
		console.log("got an answer: ", answer, " = ", x, " + ", y);
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
		console.log("got an answer: ", answer, " = ", x, " - ", y);
      }
      else {
      	answer = y - x;
        possibleAnswer = true;
		console.log("got an answer: ", answer, " = ", y, " - ", x);
      }
    }
    if(operator == "multiply") {
		x = randomInRange(rangeMin, rangeMax);
		y = randomInRange(rangeMin, rangeMax);
		answer = x * y
		possibleAnswer = true;
		console.log("got an answer: ", answer, " = ", x, " * ", y);
    }
    if(operator == "divide") {
		x = randomInRange(rangeMin, rangeMax);
		y = randomInRange(rangeMin, rangeMax);
     	if(x >= y) {
			if(x % y == 0) {
			answer = x / y;
			possibleAnswer = true;
			console.log("got an answer: ", answer, " = ", x, " / ", y);
		}
        else {
        	// need new variables that are evenly divisible by each other
			console.log("not possible");
        }
      }
      else {
      	if(y % x == 0) {
			answer = y / x;
			possibleAnswer = true;
			console.log("got an answer: ", answer, " = ", y, " / ", x);
        }
        else {
			// need new variables that are evenly divisible by each other
			console.log("not possible");
        }
      }
   	}
  }
}