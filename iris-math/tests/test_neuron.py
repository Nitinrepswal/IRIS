from neuron import Neuron


inputs = [2.0, 3.0]

weights = [0.5, 0.8]

bias = 1.0


neuron = Neuron(weights, bias)

output = neuron.forward(inputs)

print("Inputs:", inputs)
print("Weights:", weights)
print("Bias:", bias)
print("Neuron output:", output)