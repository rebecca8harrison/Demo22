import numpy as np
import numpy.matlib 
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

# Load the iris dataset
irisdata = datasets.load_iris()

# Get the iris data
x = irisdata.data
x_labs = irisdata.target
labels = np.unique(x_labs) #get unique labels

# Network output format
y_labs = np.zeros((x.shape[0],len(labels)))
for i,j in enumerate(x_labs):
    y_labs[i,j] = 1

# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y_labs, 
                                                    test_size=0.3, random_state=42)


# Sigmoid function and derivation, 
def sigmoid(x): # can chose a different function here
    return 1.0/(1.0+np.exp(-x))
def dsigmoid(x):
    return sigmoid(x)*(1.0-sigmoid(x))


# Network specifications (this one does not have a hidden layer)
layer_input = x.shape[1]
layer_output = len(labels)

# Other parameters
learning_rate = 0.3 # can play around with this and the epoch
epochs_number = 50
batch_size = x_train.shape[0] # this is set to the shape of the dataset, but can be otherwise

# Track the error in each epoch
training_error = np.zeros((epochs_number))

# Weights and bias in output
weights = np.zeros((layer_output, layer_input)) # this and bias are set as 0s as this is a simplee ANN
bias = np.zeros((layer_output))


# Train the network
for i in range(epochs_number):
    
    epoch_error = 0
    change_weights = np.zeros(weights.shape)
    change_bias = np.zeros(bias.shape)
    
    # Iterate over the batch 
    for j in range(batch_size):
        # Feedforward
        weighted_sum = np.dot(weights, x_train[j]) + bias
        network_output = sigmoid(weighted_sum)
        
        # Error calculation
        #epoch_error = network_output - y_train[j]
        #epoch_error = np.square(epoch_error)
        #epoch_error = 0.5 * np.sum(epoch_error)
        epoch_error += 0.5 * np.sum( np.square( network_output - y_train[j] ) ) 
        
        # Backpropagation
        # Delta function
        delta = (y_train[j]-network_output) * dsigmoid(weighted_sum)
        
        # Compute the change in the weights
        change_weights += learning_rate * np.outer(delta, x_train[j])
        
        # Compute the change in the bias
        change_bias += learning_rate * delta
    
    # Update the weights and the bias
    weights += change_weights / batch_size
    bias += change_bias / batch_size
       
    # Store the error of this epoch
    training_error[i] = epoch_error / batch_size
    print("Training error is:",training_error[i],"epoch error is:",epoch_error,"learning rate is:",learning_rate)
    
    
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
    
    weighted_sum = np.dot(weights, x_test[i]) + bias
    network_output = sigmoid(weighted_sum)
    
    # If the most active neuron matches the label increase the accuracy
    if np.argmax(network_output) == np.argmax(y_test[i]):
        accuracy += 1

percentage_accuracy = 100 * accuracy / test_size  
print('Network accuracy over ' +str(test_size)+ ' samples is ' +str(round(percentage_accuracy,3)))