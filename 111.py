import nympy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


training_inputs = [[5, 1, 2],
                   [7, 5, 3]]

training_outputs = np.array([[1, 0]]).T

np.random.seed(1)

synaptic_weights = 2 * np.random.random((3, 1)) - 1

print(synaptic_weights)

for i in range(200000):
    input_layers = training_inputs
    outputs = sigmoid(np.dot(input_layers, synaptic_weights))

    err = training_outputs - outputs
    adjustments = np.dot(input_layers.T, err * (outputs * (1 - outputs)))

    synaptic_weights += adjustments

print(outputs)
