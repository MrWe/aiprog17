let points = [];
let neurons = [];
let num_neurons;
let dimension = 2;
let init_decay = 0.3;
let decay = init_decay;
let sigma = num_neurons;
let sigma_now;
let tau = 500;
let eta = 0.3;
let eta_now;
let neurons_near_point = []
let mid_points = [];

let learning_rate = 1;
let file;

function preload(){
	file = loadStrings('data/8.txt');
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	background(0);


	p = sanitize_data(file);

	x_points = p.x;
	num_neurons = x_points.length;
	y_points = p.y;

	for (let i = 0; i < num_neurons; i++) {
		points.push(createVector(x_points[i],y_points[i]));
	}
	for (let i = 0; i < points.length-1; i++) {
		let halfwayX;
		let halfwayY;
		if(i === points.length-1){
			halfwayX = (points[i].x + points[0].x)/2;
			halfWayY = (points[i].y + points[0].y)/2;
			mid_points.push(createVector(halfwayX,halfWayY));
		}
		else{
			halfwayX = (points[i].x + points[i+1].x)/2;
			halfWayY = (points[i].y + points[i+1].y)/2;
			mid_points.push(createVector(halfwayX,halfWayY));
		}

	}

	for (var i = 0; i < num_neurons*3; i++) {
		circX = width/2 + 150 * cos(map(i, 0, num_neurons*3,0, TWO_PI));
		circY = height/2 + 150 * sin(map(i, 0, num_neurons*3,0, TWO_PI));
		neurons.push(new Neuron(createVector(circX,circY)));
	}

}

function draw() {
	frameRate(120)
	background(0);
	decay *= 0.999;
	//0.005;

	sigma_now = sigma*exp(-(frameRate()/tau));
	eta_now = eta*exp(-(frameRate()/tau));

	for (let i = 0; i < points.length; i++) {
		fill(255,0,0);
		noStroke();
		ellipse(points[i].x, points[i].y,15,15);

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

	// if(decay < 0.005){
	// 	add_midway_points()
	// }
}

function add_midway_points(){
	let rand_num = floor(random(mid_points.length));

	let p = mid_points[rand_num]

	let nearest_neuron = null;
	let that_distance = Infinity;
	let index = 0;

	for (let i = 0; i < neurons.length; i++) {
		let d = neurons[i].distance_to(p);
		if(d < that_distance){
			nearest_neuron=neurons[i];
			that_distance = d;
			index = i;
		}
	}

	cooperative_Process(nearest_neuron, that_distance, index, p);

}



function discriminant_function(){

	let rand_num = floor(random(points.length));

	let p = points[rand_num]

	let nearest_neuron = null;
	let that_distance = Infinity;
	let index = 0;

	for (let i = 0; i < neurons.length; i++) {
		let d = neurons[i].distance_to(p);
		if(d < that_distance){
			nearest_neuron=neurons[i];
			that_distance = d;
			index = i;

		}
	}

	cooperative_Process(nearest_neuron, that_distance, index, p);


	// if(decay < 0.0005){
	// 	remove_neurons();
	// 	add_neuron_on_stuck_city();
	// }
}

function remove_neurons(){

		for (var i = 0; i < points.length; i++) {
			p = points[i];


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
			if(neurons_near_point.indexOf(nearest_neuron) === -1){
				neurons_near_point.push(nearest_neuron);

			}
		}

		let temp = [];

		for (var i = neurons.length-1; i >= 0; i--) {
			if(neurons_near_point.indexOf(neurons[i]) === -1){
				temp.push(neurons[i]);
				neurons.splice(i,1);
				break;
			}
		}

		// for (var i = 0; i < temp.length; i++) {
		// 	let r = floor(random(neurons.length-1));
		// 	neurons.splice(r,0,temp[i]);
		// }
		//



}

function add_neuron_on_stuck_city(){
	let temp_nearest = [];
	for (var i = 0; i < points.length; i++) {
		p = points[i];

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

function add_neuron(){
	neurons.splice(floor(random(neurons.length)),0,new Neuron(mouseX,mouseY, null, null))
}

function cooperative_Process(neuron, that_distance, index, point){

	let dir_x = learning_rate * (neuron.weights.x - point.x);
	let dir_y = learning_rate * (neuron.weights.y - point.y);
	neuron.weights.x -= dir_x*0.6;
	neuron.weights.y -= dir_y*0.6;

	// if(that_distance > 15){
	// 	for (var i = 0; i < neurons.length; i++) {
	//
	// 		//if(i !== index){
	// 			//Distance to neuron that won
	// 			let S = dist(neurons[i].weights.x, neurons[i].weights.y, neuron.weights.x, neuron.weights.y);
	// 			//Sigma now ==
	// 			let T = exp(-S^2/2*sigma_now^2)
	//
	// 			dir_x = ((neurons[i].weights.x - point.x));
	// 			dir_y = ((neurons[i].weights.y - point.y));
	// 			neurons[i].weights.x -= dir_x*eta_now*T;
	// 			print(dir_x*eta_now*T);
	// 			neurons[i].weights.y -= dir_y*eta_now*T;
	// 		};
	// 	}
	// }


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
	for (var i = 6; i > 0; i--) {
		marker--;
		if(marker < 0){
			marker = neurons.length-1;
		}
		let dir_x = learning_rate * (neurons[marker].weights.x - point.x);
		let dir_y = learning_rate * (neurons[marker].weights.y - point.y);
		neurons[marker].weights.x -= dir_x*decay*extra_decay;
		neurons[marker].weights.y -= dir_y*decay*extra_decay;
		extra_decay*0.3;
	}


}


function update_neighbours(){
	new_neuron_list = [];
	for (let i = 0; i < neurons.length; i++) {
		for (let j = 0; j < neurons.length; j++) {
			if(i === j){continue;}
			if(neurons[i].distance_to(neurons[j].weights) < neurons[i].distance_to(neurons[i].neighbours[neurons[i].neighbours.length-1].weights)){
				neurons[i].add_neighbour(neurons[j]);
				neurons[j].add_neighbour(neurons[i]);
			}

			// else if(neurons[i].distance_to(neurons[j].weights) < neurons[i].distance_to(neurons[i].neighbours[1].weights)){
			// 	neurons[i].add_neighbour(neurons[j]);
			// }
		}
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
	for (var i = 0; i < num_neurons; i++) {
		remove_neurons();
		add_neuron_on_stuck_city();
	}
}

function keyPressed(){
	add_neuron();
}