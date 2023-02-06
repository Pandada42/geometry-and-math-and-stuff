// Got Bored
// Code graphing circles representing the Fourier Series Expansion of a periodic heaviside function. 
// By Matthieu Boyer


let theta = 0;
let wave = []

let n = 5;

function setup() {
  createCanvas(500, 500)
  slider = createSlider(0, 500, 1, 1)
}

function draw() {
  
  background(0);
  translate(175, 225);
  
  textSize(32)
  fill(127, 0, 0, 255)
  text("Fourier Series Expansion :", -150, -180)
  fill(127, 0, 0, 255)
  line(-150, -175, 205, -175)
  fill(127, 100, 100, 255)
  text("The Square Function", -135, -145)
  fill(127, 100, 100, 255)
  line(-135, -140, 156, -140)
  
  
  textSize(32)
  value = str(slider.value())
  fill(255, 200, 200)
  text("Number of waves : " + value, -130, 175)
  
  let x = 0;
  let y = 0;

  for (let i = 0; i < slider.value(); i++) {
    let prevx = x;
    let prevy = y;

    let n = i * 2 + 1;
    let radius = 75 * (4 / (n * PI));
    x += radius * cos(n * theta);
    y += radius * sin(n * theta);

    stroke(255, 100);
    noFill();
    ellipse(prevx, prevy, radius * 2, radius * 2);

    fill(255);
    stroke(255);
    line(prevx, prevy, x, y);
    ellipse(x, y, 8);
  }

  wave.unshift(y)

  translate(200, 0);
  line(x - 200, y, 0, wave[0]);
  beginShape();
  noFill();
  for (let i = 0; i < wave.length; i++) {
    vertex(i, wave[i]);
  }
  endShape();

  theta += 0.05;

  if (wave.length > 250) {
    for (let n = 250; n < wave.length; n++) {
      wave.pop(n);
    }
  }
}
