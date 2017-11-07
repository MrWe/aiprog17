let points = [];
let neurons = [];
let num_neurons;
let dimension = 2;
let init_decay = 0.3;
let decay = init_decay;
let neurons_near_point = []
let assignments;
let learning_rate = 0.9;
let file;

function preload(){
	file = loadStrings('data/1.txt');
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	background(0);
	assignments = {};

	p = sanitize_data(file);

	x_points = p.x;
	num_neurons = x_points.length;
	y_points = p.y;

	for (let i = 0; i < num_neurons; i++) {
		let new_city = new City(createVector(x_points[i],y_points[i]));
		new_city.hash_city();

		points.push(new_city);
	}

	for (var i = 0; i < num_neurons*3; i++) {
		circX = width/2 + 300 * cos(map(i, 0, num_neurons*3,0, TWO_PI));
		circY = height/2 + 300 * sin(map(i, 0, num_neurons*3,0, TWO_PI));
		neurons.push(new Neuron(createVector(circX,circY)));
	}

}

function draw() {
	frameRate(60)
	background(0);
	decay *= 0.999;

	for (let i = 0; i < points.length; i++) {
		fill(255,0,0);
		noStroke();
		ellipse(points[i].coords.x, points[i].coords.y,15,15);
		update_assignment(points[i]);
	}

	let path_length = 0;
	for (let i = 0; i < neurons.length; i++) {
		fill(255);
		noStroke();
		ellipse(neurons[i].weights.x, neurons[i].weights.y,10,10);
		stroke(255);
		strokeWeight(2);
		if (i === neurons.length-1) {
			line(neurons[i].weights.x, neurons[i].weights.y, neurons[0].weights.x, neurons[0].weights.y)
		}
		else{
			line(neurons[i].weights.x, neurons[i].weights.y, neurons[i+1].weights.x, neurons[i+1].weights.y)
		};
		if(i < neurons.length-1){
			path_length += neurons[i].distance_to(neurons[i+1].weights);
		}
		else{
			path_length += neurons[i].distance_to(neurons[0].weights);
		}
	}

	textSize(20);
	text(floor(path_length), 20, 20);

	discriminant_function()
}




function update_assignment(p){
	let nearest_neuron = null;
	let that_distance = Infinity;
	let index = 0;

	for (let i = 0; i < neurons.length; i++) {
		let d = neurons[i].distance_to(p.coords);
		if(d < that_distance){
			nearest_neuron=neurons[i];
			that_distance = d;
			index = i;
		}
	}

	if (!assignments[p.id]) {
    assignments[p.id] = [];
		assignments[p.id].push(nearest_neuron);
  }
	else{
		assignments[p.id][0] = nearest_neuron;
	}
}



function discriminant_function(){

	let rand_num = floor(random(points.length));

	let p = points[rand_num];

	let nearest_neuron = assignments[p.id][0]

	let index = neurons.indexOf(nearest_neuron);

	cooperative_Process(nearest_neuron, index, p.coords);



}

function remove_neurons(values){

	for (var i = neurons.length-1; i >= 0; i--) {

		if(values.indexOf(neurons[i]) === -1){
			neurons.splice(i,1);
		}
	}

	// for (var i = 0; i < points.length; i++) {
	// 	p = points[i].coords;
	// 	nearest_neuron = null;
	// 	that_distance = Infinity;
	// 	index = 0;
	//
	// 	for (let i = 0; i < neurons.length; i++) {
	// 		d = neurons[i].distance_to(p);
	// 		if(d < that_distance){
	// 			nearest_neuron=neurons[i];
	// 			that_distance = d;
	// 			index = i;
	//
	// 		}
	// 	}
	// 	if(neurons_near_point.indexOf(nearest_neuron) === -1){
	// 		neurons_near_point.push(nearest_neuron);
	//
	// 	}
	// }
	//
	// let temp = [];
	//
	// for (var i = neurons.length-1; i >= 0; i--) {
	// 	if(neurons_near_point.indexOf(neurons[i]) === -1){
	// 		temp.push(neurons[i]);
	// 		neurons.splice(i,1);
	// 		break;
	// 	}
	// }
}

function add_neuron_on_stuck_city(){
	let temp_nearest = [];
	for (var i = 0; i < points.length; i++) {
		p = points[i].coords;

		nearest_neuron = null;
		that_distance = Infinity;
		index = 0;

		for (let i = 0; i < neurons.length; i++) {
			d = neurons[i].distance_to(p);
			if(d < that_distance){
				nearest_neuron=neurons[i];
				that_distance = d;
				index = i;

			}
		}
		if(temp_nearest.indexOf(nearest_neuron) === -1){
			temp_nearest.push(nearest_neuron);
		}
		else{
			neurons.splice(index+1, 0, new Neuron(createVector(p.x+random(-5,5),p.y+random(-5,5))));
		}
	}
}

function cooperative_Process(neuron, index, point){

	let dir_x = learning_rate * (neuron.weights.x - point.x);
	let dir_y = learning_rate * (neuron.weights.y - point.y);
	neuron.weights.x -= dir_x*0.6;
	neuron.weights.y -= dir_y*0.6;

	let marker = index;
	let extra_decay = 1

	for (var i = 1; i < 6; i++) {
		let dir_x = learning_rate * (neurons[(marker+i)%(neurons.length-1)].weights.x - point.x);
		let dir_y = learning_rate * (neurons[(marker+i)%(neurons.length-1)].weights.y - point.y);
		neurons[(marker+i)%(neurons.length-1)].weights.x -= dir_x*decay*extra_decay;
		neurons[(marker+i)%(neurons.length-1)].weights.y -= dir_y*decay*extra_decay;
		extra_decay*0.3;
	}
	marker = index;

	extra_decay = 1
	for (var i = 1; i > 6; i--) {
		marker--;
		if(marker < 0){
			marker = neurons.length-1;
		}
		let dir_x = learning_rate * (neurons[marker].weights.x - point.x);
		let dir_y = learning_rate * (neurons[marker].weights.y - point.y);
		neurons[marker].weights.x -= dir_x*decay*extra_decay;
		neurons[marker].weights.y -= dir_y*decay*extra_decay;
		extra_decay*0.03;
	}
}


function sanitize_data(data){
	x_points = [];
	y_points = [];
	data.shift();
	data.forEach(x=>{
		x = x.split(" ");
		if(x.length == 3){
			x_points.push(float(x[1]));
			y_points.push(float(x[2]));
		}
	});
	let max_x = Math.max.apply(Math, x_points);
	let min_x = Math.min.apply(Math, x_points);
	let max_y = Math.max.apply(Math, y_points);
	let min_y = Math.min.apply(Math, y_points);

	x_points.forEach((elem, i)=>{
		x_points[i] = map(elem, min_x, max_x, 5, width-5);
	});
	y_points.forEach((elem, i)=>{
		y_points[i] = map(elem, min_y, max_y, 5, height-5);
	});

	return {x: x_points, y: y_points};

}

function mousePressed(){

	let values = Object.keys(assignments).map(function(key){
    return assignments[key][0];
	});

	remove_neurons(values);
	//add_neuron_on_stuck_city();

}

