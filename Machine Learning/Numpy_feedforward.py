import numpy as np 
from random import seed

def init_network(num_inputs, num_hidden_layers, num_nodes_hidden, num_nodes_output):

	num_nodes_previous = num_inputs # number of nodes in the previous layer

	network = {}

	#  randomly initialize the weights and biases associated with each layer
	for layer in range(num_hidden_layers + 1):
		if layer == num_hidden_layers:
			layer_name = 'output' # name last layer in the network output
			num_nodes = num_nodes_output
		else:
			layer_name = 'layer_{}'.format(layer + 1) # otherwise give the layer a number
			num_nodes = num_nodes_hidden[layer] 
		 
		# initialize weights and bias for each node
		network[layer_name] = {}
		for node in range(num_nodes):
			node_name = 'node_{}'.format(node+1)
			network[layer_name][node_name] = {
				'weights': np.around(np.random.uniform(size=num_nodes_previous), decimals=2),
				'bias': np.around(np.random.uniform(size=1), decimals=2),
			}
	
		num_nodes_previous = num_nodes

	return network 



def compute_weighted_sum(inputs, weights, bias):
	return np.sum(inputs * weights) + bias



def node_activation(weighted_sum):
	return 1.0 / (1.0 + np.exp(-1 * weighted_sum))



def forward_propagate(network, inputs):
	
	layer_inputs = list(inputs) # start with the input layer as the input to the first hidden layer
	
	for layer in network:
		
		layer_data = network[layer]
		
		layer_outputs = [] 
		for layer_node in layer_data:
			node_data = layer_data[layer_node]
		
			# compute the weighted sum and the output of each node at the same time 
			node_output = node_activation(compute_weighted_sum(layer_inputs, node_data['weights'], node_data['bias']))
			layer_outputs.append(np.around(node_output[0], decimals=4))
		
		if layer != 'output':
			print('The outputs of the nodes in hidden layer number {} is {}'.format(layer.split('_')[1], layer_outputs))
	
		layer_inputs = layer_outputs # set the output of this layer to be the input to next layer

	network_predictions = layer_outputs
	return network_predictions

np.random.seed(12)
inputs_number = 5
inputs = np.around(np.random.uniform(size=inputs_number), decimals=2)

print('The inputs to the network are: {}'.format(inputs))

layer_count = int(input('Enter hidden layers number: '))

nodes_count = []

for i in range(1,layer_count+1):
	nodes_in_layer = int(input('Enter nodes number in layer {}: '.format(i)))
	nodes_count.append(nodes_in_layer)



outputs_count = int(input('Enter outputs number: '))

my_network = init_network(inputs_number,layer_count,nodes_count,outputs_count)

node_weights = my_network['layer_1']['node_1']['weights']
node_bias = my_network['layer_1']['node_1']['bias']

weighted_sum = compute_weighted_sum(inputs, node_weights, node_bias)
print('Sum at the 1 node in the hidden layer: {}'.format(np.around(weighted_sum[0], decimals=4)))

node_output  = node_activation(compute_weighted_sum(inputs, node_weights, node_bias))
print('Output of the 1 node in the hidden layer: {}'.format(np.around(node_output[0], decimals=4)))

predictions = forward_propagate(my_network, inputs)
print('The predicted values by the network for the given input are {}'.format(predictions))