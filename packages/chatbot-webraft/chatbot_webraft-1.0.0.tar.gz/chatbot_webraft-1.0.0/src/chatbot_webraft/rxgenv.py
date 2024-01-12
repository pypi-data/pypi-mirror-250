import random
import csv
import string
def preprocess(text):
    # Convert text to lowercase and split into words
    words = text.lower().split()

    # Create dictionary mapping each unique word to a unique integer index
    word_to_index = {word: i for i, word in enumerate(set(words))}

    # Convert each word in the text to its corresponding integer index
    indices = [word_to_index[word] for word in words]

    # Convert integer indices to one-hot vectors
    num_words = len(word_to_index)
    input_vectors = np.zeros((len(indices), num_words))
    input_vectors[np.arange(len(indices)), indices] = 1

    return input_vectors, word_to_index

def preprocessorx(list):
    import random

    my_list = list

    used_numbers = []

    for i in range(len(my_list)):
        if my_list[i] in used_numbers:
            continue
        else:
            random_number = random.randint(1, 10000)
            while random_number in used_numbers:
                random_number = random.randint(1, 10000)
            my_list[i] = str(random_number)
            used_numbers.append(random_number)

    print(my_list)


import json

def extractor(text):
    text = text.split("\n")
    text = [s.split(" ") for s in text]
    words = []
    for sentence in text:
        for word in sentence:
            words.append(word)
    return words

def preprocessor(words):
    used_values = {}
    output = {}
    for word in words:
        if word in used_values:
            output[word] = used_values[word]
        else:
            value = round(random.uniform(0, 1), 8)
            used_values[word] = value
            output[word] = value

    with open('preprocessed_fr_eng.json', 'w') as f:
        json.dump(output, f)

#with open('input.txt', 'r') as f:
    #text = f.read()

#words = extractor(text)
#preprocessor(words)
import numpy as np

# Sigmoid activation function
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# Derivative of sigmoid function
def sigmoid_derivative(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights
        self.weights1 = np.random.rand(self.input_size, self.hidden_size)
        self.weights2 = np.random.rand(self.hidden_size, self.output_size)

    def feedforward(self, X):
        # Propagate input through the network
        self.hidden_layer = sigmoid(np.dot(X, self.weights1))
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights2))
        return self.output_layer

    def backpropagation(self, X, y, learning_rate):
        # Calculate errors and deltas for each layer
        output_error = y - self.output_layer
        output_delta = output_error * sigmoid_derivative(self.output_layer)

        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_layer)

        # Update weights with deltas and learning rate
        self.weights2 += learning_rate * np.dot(self.hidden_layer.T, output_delta)
        self.weights1 += learning_rate * np.dot(X.T, hidden_delta)

    def train(self, X, y, learning_rate, epochs):
        for i in range(epochs):
            # Feedforward through the network

            output = self.feedforward(X)

            # Backpropagation to update weights
            self.backpropagation(X, y, learning_rate)
            print("Iterating Epoch :", i,"/",epochs)

    def predict(self, X):
        # Predict output for new input
        return self.feedforward(X)





# Define neural network class
class NeuralNetwork2:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights
        self.weights1 = np.random.rand(self.input_size, self.hidden_size)
        self.weights2 = np.random.rand(self.hidden_size, self.output_size)

    def feedforward(self, X):
        # Propagate input through the network
        self.hidden_layer = sigmoid(np.dot(X, self.weights1))
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights2))
        return self.output_layer

    def backpropagation(self, X, y, learning_rate):
        # Calculate errors and deltas for each layer
        output_error = y - self.output_layer
        output_delta = output_error * sigmoid_derivative(self.output_layer)

        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_layer)

        # Update weights with deltas and learning rate
        self.weights2 += learning_rate * np.dot(self.hidden_layer.T, output_delta)
        self.weights1 += learning_rate * np.dot(X.T, hidden_delta)

    def train(self, X, y, learning_rate, epochs):
        for i in range(epochs):
            # Feedforward through the network
            output = self.feedforward(X)

            # Backpropagation to update weights
            self.backpropagation(X, y, learning_rate)
            print("Iterating Epoch: ", i, " / ", epochs)

    def predict(self, X):
        # Predict output for new input
        return self.feedforward(X)




def rxgenv_model(corpus,seed,len1=10,len2=20,learning_rate=0.1,hidden_size=100,epochs=10,save="save.npz",traintype="cpu",pretrain="False",pretrain_file="save.npz"):
    corpus = open(corpus).read().lower().translate(str.maketrans('', '', string.punctuation)).split()
    if traintype=="cpu":
        xp = np
    elif traintype=="gpu":
        import cupy as cp
        xp = cp
    elif traintype=="CPU":
        xp = np
    elif traintype=="GPU":
        import cupy as cp
        xp = cp
    else:
        xp=np

    vocab = sorted(set(corpus))
    word2idx = {w: i for i, w in enumerate(vocab)}
    idx2word = {i: w for i, w in enumerate(vocab)}


    WINDOW_SIZE = 2
    train_data = []
    for i in range(len(corpus) - WINDOW_SIZE):
        train_data.append(([corpus[j] for j in range(i, i + WINDOW_SIZE)], corpus[i + WINDOW_SIZE]))


    INPUT_SIZE = len(vocab)
    HIDDEN_SIZE = hidden_size
    OUTPUT_SIZE = len(vocab)
    LEARNING_RATE = learning_rate

    if pretrain == "True":
        data = xp.load(pretrain_file)
        U = data['U']
        V = data['V']
        W = data['W']
        bh = data['bh']
        by = data['by']

    elif pretrain == "False":
        U = xp.random.randn(INPUT_SIZE, HIDDEN_SIZE) * 0.01
        V = xp.random.randn(HIDDEN_SIZE, OUTPUT_SIZE) * 0.01
        W = xp.random.randn(HIDDEN_SIZE, HIDDEN_SIZE) * 0.01
        bh = xp.zeros((1, HIDDEN_SIZE))
        by = xp.zeros((1, OUTPUT_SIZE))
    else:
        U = xp.random.randn(INPUT_SIZE, HIDDEN_SIZE) * 0.01
        V = xp.random.randn(HIDDEN_SIZE, OUTPUT_SIZE) * 0.01
        W = xp.random.randn(HIDDEN_SIZE, HIDDEN_SIZE) * 0.01
        bh = xp.zeros((1, HIDDEN_SIZE))
        by = xp.zeros((1, OUTPUT_SIZE))


    for epoch in range(epochs):
        loss = 0
        for X, y in train_data:

            x_idx = [word2idx[w] for w in X]
            y_idx = word2idx[y]


            h = xp.zeros((1, HIDDEN_SIZE))
            inputs = xp.zeros((1, INPUT_SIZE))
            for i in x_idx:
                inputs[0, i] = 1


            h = xp.tanh(xp.dot(inputs, U) + xp.dot(h, W) + bh)
            y_hat = xp.exp(xp.dot(h, V) + by) / xp.sum(xp.exp(xp.dot(h, V) + by))


            loss += -xp.log(y_hat[0, y_idx])


            dy = xp.copy(y_hat)
            dy[0, y_idx] -= 1
            dV = xp.dot(h.T, dy)
            dby = dy
            dh = xp.dot(dy, V.T)
            dg = (1 - h ** 2) * dh
            dU = xp.dot(inputs.T, dg)
            dbh = dg


            U -= LEARNING_RATE * dU
            V -= LEARNING_RATE * dV
            W -= LEARNING_RATE * dh
            bh -= LEARNING_RATE * dbh
            by -= LEARNING_RATE * dby
        correct_count = 0
        total_count = 0
        for X, y in train_data:
            x_idx = [word2idx[w] for w in X]
            y_idx = word2idx[y]
            h = xp.zeros((1, HIDDEN_SIZE))
            inputs = xp.zeros((1, INPUT_SIZE))
            for i in x_idx:
                inputs[0, i] = 1
            h = xp.tanh(xp.dot(inputs, U) + xp.dot(h, W) + bh)
            y_hat = xp.exp(xp.dot(h, V) + by) / xp.sum(xp.exp(xp.dot(h, V) + by))
            predicted_idx = xp.argmax(y_hat)
            if predicted_idx == y_idx:
                correct_count += 1
            total_count += 1
        accuracy = correct_count / total_count
        print('Epoch:', epoch+ 1, '/ ', epochs, ' \n Loss:', loss, 'Accuracy:', accuracy )
    xp.savez(save, U=U, V=V, W=W, bh=bh, by=by, word2idx=word2idx, idx2word=idx2word)
    for i in range(len1):
        x = xp.zeros((1, INPUT_SIZE))
        x[0, word2idx[seed]] = 1
        h = xp.zeros((1, HIDDEN_SIZE))
        sentence = [seed]
        for j in range(len2):
            h = xp.tanh(xp.dot(x, U) + xp.dot(h, W) + bh)
            y = xp.dot(h, V) + by
            p = xp.exp(y) / xp.sum(xp.exp(y))
            idx = xp.random.choice(range(len(vocab)), p=p.ravel())
            if idx2word[idx] == '.':
                sentence.append('.')
                break
            sentence.append(idx2word[idx])
            x = xp.zeros((1, INPUT_SIZE))
            x[0, idx] = 1

        return  ' '.join(sentence)
#print(model("internet_archive_scifi_v3.txt","the",epochs=100,hidden_size=50,learning_rate=0.1))


