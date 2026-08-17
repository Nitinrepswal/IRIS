from neuron_details import Neuron


inputs = [2.0, 3.0]

weights = [0.5, 0.8]

bias = 0.2

neuron = Neuron(weights, bias)

weighted_sum = neuron.weighted_sum(inputs)

print("Inputs:", inputs)
print("Weights:", weights)
print("Bias:", bias)
print("Weighted sum:", weighted_sum)