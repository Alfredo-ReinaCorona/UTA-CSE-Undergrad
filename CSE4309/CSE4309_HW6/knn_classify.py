import numpy as np


#copied from HW5
def openDataset(dataset):
    allData = np.loadtxt(dataset)
    # we don't want to use the labels
    # remove the last class (labels)
    attributes = allData[:, :-1]
    uniqueAttributes = np.unique(attributes)
    numUniqueAttributes = attributes.shape[1]

    # get the labels and convert them to integers
    # do not touch the last column
    labels = [int(label) for label in allData[:, -1]]
    uniqueLabels = np.unique(labels)
    numUniqueLabels = len(np.unique(labels))

    return attributes, labels, allData, uniqueLabels

 
def knn_classify(training_file, test_file, k):
    
    #Split up information from the dataset
    trainingAttributes, trainingLabels,_,_ = openDataset(training_file)
    testAttributes, testLabels,_,_ = openDataset(test_file)

    #Get the means and standard deviations to normalize the data(extend to full range)
    means = np.mean(trainingAttributes, axis=0)
    std = np.std(trainingAttributes, axis=0, ddof=1)
    
    #at the index where the std is 0, replace it with 1 so that the calculation is not undefined
    for i in range(len(std)):
        if std[i] == 0:
            std[i] = 1

    #Normalize each dimension using F(v) = (v - mean) / std 
    #Each normalization must use each dimension's respective mean and standard deviation
    normalizedTrainingAttributes = (trainingAttributes-means)/std
    normalizedTestAttributes = (testAttributes-means)/std
    
    #Classification stage
    correct = 0

    for i, test_instance in enumerate(normalizedTestAttributes):
        
        #Calculate the euclidian distances
        #low dimensionality makes this viable
        distances = np.linalg.norm(normalizedTrainingAttributes - test_instance, axis=1)
        
        #sort distances from least to greatest
        sorted_indices = np.argsort(distances)

        #list the 'k' nearest neigbors
        k_nearest_neighbors = [trainingLabels[idx] for idx in sorted_indices[:k]]
        
        #return the unique classes(and their frequency) found within the 'k' neigbors
        classesFromNeighbors, counts = np.unique(k_nearest_neighbors, return_counts=True)

        #Predict the class. If there is a tie, choose between the choices randomly
        predictedClass = np.random.choice(classesFromNeighbors[counts == counts.max()])
        
        #Use the true class to see if the guess is correct
        realClass = testLabels[i]

        #Convert to a list. numpy array gives errors
        predictedClassList = [predictedClass]
        
        #Get the boolean accuracy or each individual case( 1 or 0)
        if len(predictedClassList) == 1 and predictedClassList[0] == realClass:
            accuracy = 1
        else:
            accuracy = 1 / len(predictedClassList) if realClass in predictedClassList else 0

        # Print individual test results
        print(f"ID={i+1:5d}, predicted={predictedClass}, true={realClass}, accuracy={accuracy:4.2f}")

        correct += accuracy

    #Total Accuracy                                 vvv predictions should sum up to the length of the list of labels
    classification_accuracy = correct / len(testLabels)
    print(f'classification accuracy= {classification_accuracy:6.4f}')

