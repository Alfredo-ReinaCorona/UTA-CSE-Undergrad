

#Avg times for each option at a pruning threshold of 50
#option = 1 = 5 seconds
#option = 3 = 1 minute
#option = 'optimized' = 1 minute

#given decision tree and pattern can you classify the pattern
#--------------------------------
import numpy as np
import random

# # When you test your code, you can change this line to reflect where the 
# # dataset directory is located on your machine.
dataset_directory = "/home/alfredo/Documents/CSE4309/CSE4309_HW5"

# # When you test your code, you can select the dataset you want to use 
# # by modifying the next lines
dataset = "pendigits"
# #dataset = "satellite"
# #dataset = "yeast"

training_file = dataset_directory + "/" + dataset + "_training.txt"
test_file = dataset_directory + "/" + dataset + "_test.txt"

# # When you test your code, you can select the function arguments you want to use 
# # by modifying the next lines
# #option = "optimized"
#option = 1
#option = 3
#option = 15
option = 'optimized'
pruning_thr = 50


# Copied from my other HW's
def openDataset(dataset):
    allData = np.loadtxt(dataset)
    attributes = allData[:, :-1]
    uniqueAttributes = np.unique(attributes)
    numUniqueAttributes = attributes.shape[1]
    labels = [int(label) for label in allData[:, -1]]
    uniqueLabels = np.unique(labels)
    numUniqueLabels = len(np.unique(labels))
    return allData


training_file_data = openDataset(training_file)
test_file_data = openDataset(test_file)


class Tree:
    def __init__(self, attribute=-1, threshold=-1, left=None, right=None, data=-1, gain=0):
        self.attribute = attribute
        self.threshold = threshold
        self.left = left
        self.right = right
        self.data = data
        self.gain = gain


# Makes the first call to DTL with the right arguments
#ok
def DTL_TopLevel(examples):
    default = PDF(examples)[1]
    attributes = range(len(examples[0][:-1]))
    return DTL(examples, attributes, default)


#ok
def DTL(examples, attributes, default):

    # Base case: examples is below the pruning threshold or there is a uniform class
    if len(examples) < pruning_thr or 1 in PDF(examples):
        return Tree(data=PDF(examples) if 1 in PDF(examples) else default)

    # get best attribute, threshold, and gain using the CHOOSE_ATTRIBUTE function
    best_attribute, best_threshold, gain = CHOOSE_ATTRIBUTE(attributes, examples)
    # Make tree node
    tree = Tree(best_attribute, best_threshold, gain=gain)

    # Split to left and right branches
    examples_left = [x for x in examples if x[best_attribute] < best_threshold]
    examples_right = [x for x in examples if x[best_attribute] >= best_threshold]

    # Recursively make subtrees
    tree.left = DTL(examples_left, attributes, PDF(examples))
    tree.right = DTL(examples_right, attributes, PDF(examples))

    return tree


# Search for best combination of attribute and threshold happens in this fucntion
#ok
def CHOOSE_ATTRIBUTE(attributes, examples):
    if option == "optimized":
        max_gain = best_attribute = best_threshold = -1
        for A in attributes:
            attribute_values = [x[A] for x in examples]
            L, M = min(attribute_values), max(attribute_values)
            for K in range(1, 51):#(1,50)?
                threshold = L + K * (M - L) / 51
                gain = information_gain(examples, A, threshold)
                if gain > max_gain:
                    max_gain, best_attribute, best_threshold = gain, A, threshold
        return (best_attribute, best_threshold, max_gain)
    
    elif option == "randomized":
        max_gain = best_threshold = -1
        A = random.choice(attributes)
        attribute_values = [x[A] for x in examples]
        L, M = min(attribute_values), max(attribute_values)
        for K in range(1, 51):
            threshold = L + K * (M - L) / 51
            gain = information_gain(examples, A, threshold)
            if gain > max_gain:
                max_gain, best_threshold = gain, threshold
        return (A, best_threshold, max_gain)


#Entropy portion of the information gain function
def entropy(data):
    class_distribution = PDF(data)
    return -sum(probability * np.log2(probability) if probability > 0 else 0 for probability in class_distribution)


# probability distribution function for all classes
#ok
def PDF(examples):
    # list to store the count of each class in the given distribution
    densityList = np.zeros(len(distribution))
    
    # Count number of each class
    for example in examples:
        densityList[distribution[example[-1]]] += 1
    
    # Normalize, then convert to probability distribution
    densityList /= len(examples) if len(examples) > 0 else 1
    
    return densityList



#ok
def information_gain(examples, A, threshold):
    H_E = entropy(examples)
    
    examples_left = [i for i in examples if i[A] < threshold]
    examples_right = [i for i in examples if i[A] >= threshold]
    
    H_E1 = entropy(examples_left)
    H_E2 = entropy(examples_right)
    
    K, K1, K2 = len(examples), len(examples_left), len(examples_right)
    
    final_entropy = H_E - (K1 / K) * H_E1 - (K2 / K) * H_E2
    
    return final_entropy


# probability of a class label on a specified tree
#ok
def predict(tree, test_data):
    if tree.left is None and tree.right is None:
        return tree.data
    return predict(tree.left, test_data) if test_data[tree.attribute] < tree.threshold else predict(tree.right, test_data)

#Couldnt figure out how to call DTL_Top Level from within "decision_tree()"
#Kept getting "attribute referenced before assignment" error
def decision_tree(training_file, test_file, option, pruning_thr):
    return 0


#--------------------
#TODO add code to denote when training starts and end
#"For the other three options (randomized, forest3, forest 15) the results will vary, since the code needs to make randomized choices"
if option == 1:
    option = 'randomized'
elif option == 3:
    option = 'forest3'
elif option == 15:
    option == 'forest15'

attributes = range(len(training_file_data[0][:-1]))

#--------------------
#Train
# Extract unique classes from the last column of examples
unique_classes = sorted(set(row[-1] for row in training_file_data))
# Create a dictionary with classes as keys and unique integers as values
distribution = {cls: i for i, cls in enumerate(unique_classes)}
trees = []

#Changed DTL_TopLevel(train_data, attributes) to what it is now. Optimized accuracy increased from .8382 to .8393
if option == "optimized" or option == "randomized":
    trees.append(DTL_TopLevel(training_file_data))

elif option in ["forest3", "forest15"]:
    option = "randomized"
    num_trees = 3 if option == "forest3" else 15
    for _ in range(num_trees):
        trees.append(DTL_TopLevel(training_file_data))


# prints the tree that was generated during the training phase
node_number = 1
for i, tree in enumerate(trees):
    if not tree:
        break
    queue = [tree]
    while queue:
        current_node = queue.pop(0)
        print("tree=%2d, node=%3d, feature=%2d, thr=%6.2f, gain=%f" % (i+1, node_number, current_node.attribute, current_node.threshold, current_node.gain))
        node_number += 1
        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

#--------------------
#Test            
total_correct = 0
for n in range(len(test_file_data)):
    accuracy = 0
    distance = [predict(tree, test_file_data[n]) for tree in trees]
    predicted_class_index = np.argmax(distance)
    predicted_class = predicted_class_index % len(distance[0])
    accuracy = 1 if predicted_class == test_file_data[n][-1] else 0
    total_correct += accuracy
    print("ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2f" % (n+1, predicted_class, int(test_file_data[n][-1]), accuracy))
print("classification accuracy= %6.4f" % (total_correct/len(test_file_data)))
