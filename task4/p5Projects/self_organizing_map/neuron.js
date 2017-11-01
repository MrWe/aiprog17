class Neuron {
  constructor(weights) {
    this.weights = weights;

  }

  show(){
    fill(51);
    stroke(255);
    strokeWeight(2);
    ellipse(this.weights.x,this.weights.y,10,10)
    for (var n in this.neighbours) {
      line(this.weights.x,this.weights.y,this.neighbours[n].weights.x,this.neighbours[n].weights.y)
    }
  }

  distance_to(point){
    return dist(this.weights.x,this.weights.y,point.x,point.y);
  }



}