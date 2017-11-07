class City {
  constructor(coords) {
    this.coords = coords;
    this.assigned_neuron;
    this.id;
  }

  hash_city(){
  	this.id = this.coords.x.toString() + this.coords.y.toString();
  }
}