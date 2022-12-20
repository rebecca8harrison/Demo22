"""

"""

import numpy as np
import numpy.matlib 
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

# Load the digits dataset
digitsdata = datasets.load_digits()

# Get the digits data
x = digitsdata.data
x_labs = digitsdata.target
labels = np.unique(x_labs) #get unique labels

# Visualise a digit
i = 0
plt.matshow(np.reshape(x[i],(8,8)))

# Network output format
y_labs = np.zeros((x.shape[0],len(labels)))
for i,j in enumerate(x_labs):
    y_labs[i,j] = 1

# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y_labs, 
                                                    test_size=0.2, random_state=42)


# Sigmoid function and derivation
def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))
def dsigmoid(x):
    return sigmoid(x)*(1.0-sigmoid(x))


# Network specifications
layer_input = x.shape[1]
layer_hidden = 25
layer_output = len(labels)

# Other parameters
learning_rate = 0.75
epochs_number = 500
batch_size = x_train.shape[0]

# Weights initialisation and normalisation so that the sum of each row is equal to 1
wih = np.random.uniform(0,1,(layer_hidden, layer_input))
wih = np.divide(wih,np.matlib.repmat(np.sum(wih,1)[:,None],1,layer_input))
who = np.random.uniform(0,1,(layer_output, layer_hidden))
who = np.divide(who,np.matlib.repmat(np.sum(who,1)[:,None],1,layer_hidden))
    
# Initialize the biases, set for both hidden layer and output this time
bias_wih = np.zeros((layer_hidden,))
bias_who = np.zeros((layer_output,))

# Track the error in each epoch
training_error = np.zeros((epochs_number,))


# Train the network
for i in range(epochs_number):
    
    # Weights change
    dwih = np.zeros(wih.shape)
    dwho = np.zeros(who.shape)

    # Bias change 
    dbias_wih = np.zeros(bias_wih.shape)
    dbias_who = np.zeros(bias_who.shape)
    
    # Epoch error
    epoch_error = 0
    
    # Iterate over the batch 
    for j in range(batch_size):
        
        # Feedforward #
        
        # Input layer --> hidden layer
        h1 = np.dot(wih, x_train[j]) + bias_wih
        x1 = sigmoid(h1) #activation function

        # Hidden layer -> output layer
        h2 = np.dot(who,x1)+bias_who
        x2 = sigmoid(h2) #activation function
        
        # Error calculation
        epoch_error += 0.5 * np.sum( np.square( x2 - y_train[j] ) ) 
        
        # Backpropagation #
        
        # Output layer --> hidden layer, delta function and compute the change in the weights and bias
        delta2 = (y_train[j]-x2) * dsigmoid(h2)
        dwho += np.outer(delta2, x1)
        dbias_who += delta2

        # Hidden layer --> input layer, delta function and compute the change in the weights and bias
        delta1 = x1*(1-x1) * np.dot(who.T, delta2)
        dwih += np.outer(delta1,x_train[j])
        dbias_wih += delta1

    # Update the weights and the biases
    wih += learning_rate * dwih/batch_size
    who += learning_rate * dwho/batch_size
    bias_wih += dbias_wih/batch_size
    bias_who += dbias_who/batch_size
    
    # Store the error of this epoch
    training_error[i] = epoch_error / batch_size

    # Progress (every 10 iterations)
    if i % 10 == 0 or i==epochs_number-1:
        print( "Epoch ", i+1, ": training error = ", round(training_error[i],9))
    
    
    
# See if the network is training
fig, ax = plt.subplots()
ax.plot(training_error, lw=2.5)
ax.grid()
ax.set_xlabel('epochs')
ax.set_ylabel('mean square error (training)')
ax.set_title('$\eta$ = ' +str(learning_rate)+ ' , batch = ' +str(batch_size))
plt.show()


# Test the network using unseen data
test_size = len(y_test)
accuracy = 0

for i in range(test_size):
    
    # Input layer --> hidden layer
    h1 = np.dot(wih, x_test[i]) + bias_wih
    x1 = sigmoid(h1) #activation function

    # Hidden layer -> output layer
    h2 = np.dot(who,x1)+bias_who
    x2 = sigmoid(h2) #activation function
    
    # If the most active neuron matches the label increase the accuracy
    if np.argmax(x2) == np.argmax(y_test[i]):
        accuracy += 1

percentage_accuracy = 100 * accuracy / test_size  
print('Network accuracy over ' +str(test_size)+ ' samples is ' +str(round(percentage_accuracy,3)))