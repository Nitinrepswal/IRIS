from neural_network import NeuralNetwork


model = NeuralNetwork()

inputs = [1.0, 2.0]

hidden_outputs, output = model.forward(inputs)

print("Inputs:", inputs)
print("Hidden outputs:", hidden_outputs)
print("Final output:", output)