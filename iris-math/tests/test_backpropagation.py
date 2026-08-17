from backpropagation import SimpleNeuron


neuron = SimpleNeuron(
    weight=0.5,
    bias=0.0,
    learning_rate=0.1
)

x = 2.0
target = 1.0

print("Initial weight:", neuron.weight)
print("Initial bias:", neuron.bias)

for epoch in range(5):
    prediction, loss = neuron.train_step(
        x,
        target
    )

    print(
        "Epoch:", epoch + 1,
        "Prediction:", prediction,
        "Loss:", loss,
        "Weight:", neuron.weight,
        "Bias:", neuron.bias
    )