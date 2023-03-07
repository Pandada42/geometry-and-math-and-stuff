let x, y;
let px, py;
let step = 1;
let stepSize = 50;
let numSteps = 1;
let state = 0;
let turnCounter = 1;
let totalSteps;

function setup() {
  createCanvas(550, 550);

  const cols = width / stepSize;
  const rows = height / stepSize;
  totalSteps = cols * rows;

  x = width / 2;
  y = height / 2;
  px = x;
  py = y;
  background(0);
}

function isPrime(value) {
  // Fast Primality Check
  if (value < 2) {return false}
  else if (value < 4) {return true}
  else if (value % 2 == 0 || value % 3 == 0) {return false}
  else {
    for (let i = 5; i <= sqrt(value); i += 6) {
      if (value % i == 0 || value % (i + 2) == 0) {
        return false;
      }
    }
  }

  return true;
}


function draw() {
  textSize(stepSize * 0.5);
  textAlign(CENTER, CENTER);
  
  //Prints out the number of the step the program is showing
  //fill(255);
  //noStroke();
  //noFill();
  //stroke(255, 0, 0);
  //text(step, x, y); 
  
  //Creates a grid separating each number
  //stroke(255);
  //strokeWeight(0.5);
  //noFill();
  //rectMode(CENTER);
  //rect(x, y, stepSize);
  
  if (isPrime(step)) {
    noFill()
    stroke(255)
    circle(x, y, stepSize * 0.90);
    fill(255, 0, 0);
    noStroke();
    text(step, x, y); 
  }
  
  //Creates a line showing the order of the steps taken.
  //stroke(255)
  //line(x, y, px, py);
  //px = x;
  //py = y;

  //Indicator of the position of the next orientation
  switch (state) {
    case 0:
      x += stepSize;
      break;
    case 1:
      y -= stepSize;
      break;
    case 2:
      x -= stepSize;
      break;
    case 3:
      y += stepSize;
      break;
  }
  
  //Indicator of the number of steps to take before next update to step and change of orientation. 
  if (step % numSteps == 0) {
    state = (state + 1) % 4;
    turnCounter++;
    if (turnCounter % 2 == 0) {
      numSteps++;
    }
  }
  
  step++;
  if (step > totalSteps) {
    noLoop();
  }
}
