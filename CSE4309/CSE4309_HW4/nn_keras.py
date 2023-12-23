import numpy as np
import tensorflow as tf

def openDataset(dataset, type):

    #find out what type of files was passed in and open it
    if type == "training":
        datasetFile = dataset + "_training.txt"

    if type == "test":
        datasetFile = dataset + "_test.txt"

    dataFromDataset = np.loadtxt(datasetFile)
    
    #get the labels and convert them to integers
    #do not touch the last column
    labels = [int(label) for label in dataFromDataset[:, -1]]

    #we dont want to use the labels
    #remove the last class(labels)
    dataFromDataset = dataFromDataset[:, :-1]

    #I keep getting an error about labels being out of bound i.e (0,7] will not allow a label of value 7
    #Shift all the labels down by the smallest label. This is only a visual change in order to run the code
    labels = labels - np.min(labels)

    numClasses = len(np.unique(labels)) + 1

    return dataFromDataset, labels, numClasses

#part of the assignment, "...single highest absolute value..."
#divide EVERY value within the dataset(minus the last column) by maximum absolute value
def normalizeAttributes(dataFromDataset):
    maxValueAbsolute = np.max(np.abs(dataFromDataset))
    return dataFromDataset / maxValueAbsolute


#most of this function was coped from the class website with minor modifications
def nn_keras(dir, dataset, layers, units_per_layer, epochs):
    
    #open the datasets
    #specify the types so that the function can handle them appropriately
    trainingData, trainingLabels, numClasses = openDataset(dataset, "training")
    testData, testLabels, _ = openDataset(dataset, "test")

    #normalize the data as instructed
    trainingData = normalizeAttributes(trainingData)
    testData = normalizeAttributes(testData)

    #make the model. Copies from code provided in class website
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(trainingData.shape[1],)))

    #if more than 2 layers are used, hidden layers will need to be initialized as well
    #loop untill the number of layers specified is built
    for i in range(layers - 2):
        model.add(tf.keras.layers.Dense(units_per_layer, activation='sigmoid'))

    # Output layer
    model.add(tf.keras.layers.Dense(numClasses, activation='sigmoid'))

    #build the model
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

    # Train the model
    model.fit(trainingData, trainingLabels, epochs=epochs)

    # Evaluate on test dataFromDataset
    loss, accuracy = model.evaluate(testData, testLabels, verbose=0)

    print("classification accuracy = %6.4f\n" % accuracy)
