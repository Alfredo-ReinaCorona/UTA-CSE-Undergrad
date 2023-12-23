import math

# open the file and extract the data into lists
def openFile(filepath, type, allTrainingFile, allTestFile):
    file = open(filepath, "r")
    for (i,line) in enumerate(file.readlines()):
        if type == 1:
            allTrainingFile.append([])
        else:
            allTestFile.append([])
        for string in line.split():
            value = float(string)
            if type == 1:
                allTrainingFile[i].append(value)
            else:
                allTestFile[i].append(value)


def trainingPhase(allTrainingFile):
    
    #Holds all class info
    infoByClass = {}

    for row in allTrainingFile:

        #Get class value and attribute of each row
        classValue = row[-1]
        attributes = row[:-1]

        #Add attributes for each class
        infoByClass[classValue] = infoByClass.get(classValue, []) + [attributes]

    #Get class information
    classInformation = {label: [(sum(attr) / len(attr), stdv(attr), len(attr)) for attr in zip(*class_values)] for label, class_values in infoByClass.items()}

    #Print the training information
    for label in sorted(classInformation.keys()):
        for i, row in enumerate(classInformation[label]):
            print("Class ", label,", Attribute ", i + 1,", Mean = %0.2f" % row[0],", Standard Deviation = %0.2f" % row[1])

    return classInformation


def testingPhase(summaries, allTestFile, allTrainingFile):

    predictions = []
    correct = 0 

    for i, row in enumerate(allTestFile):

        #Array of probabilities for each class
        probabilities = {}
        numRows = len(allTrainingFile)

        for label, classInformation in summaries.items():

            #Get the prior probability of the class P(Cj)
            priorProbability = classInformation[0][2] / numRows
            pgivenCj = 1

            #Iterate over each attribute of the input data row
            for j, (mean, stdv, _) in enumerate(classInformation):
                #Gaussian distribution
                probabilityDensityFunction = (1 / (stdv * math.sqrt(2 * math.pi))) * math.exp(-(((row[j] - mean) ** 2) / (2 * (stdv ** 2))))
                pgivenCj *= probabilityDensityFunction

            #P(Cj|x)
            probabilities[label] = pgivenCj * priorProbability

        totalProbability = sum(probabilities.values())

        #Normalize the probabilities
        normalizedProbabilities = {label: prob / totalProbability for label, prob in probabilities.items()}

        #Find most probable label
        bestLabel, highestProbability = max(normalizedProbabilities.items(), key=lambda x: x[1])
        
        #Getthe number of ties
        numTies = sum(1 for prob in normalizedProbabilities.values() if prob == highestProbability) - 1

        predictions.append([bestLabel, highestProbability, numTies if numTies > 0 else 0])

        #Get boolean accuracy and print the results
        accuracy = 1 if allTestFile[i][-1] == predictions[i][0] else 0
        accuracy /= predictions[i][2] if predictions[i][2] > 0 else 1
        print(f"ID= {i+1}, predicted= {predictions[i][0]}, probability= {predictions[i][1]:.4f}, true= {allTestFile[i][-1]}, accuracy= {accuracy:.2f}")
        correct += accuracy

    accuracy = correct / len(allTestFile)
    print(f"classification accuracy is {accuracy:.4f}")


# numpy and math libraries don't give the correct std output, so it is defined here
def stdv(numbers):
    avg = sum(numbers) / len(numbers)
    dx = sum((x - avg) ** 2 for x in numbers)
    covariance = dx / (len(numbers) - 1)

    #makes sure the stdv never falls below the threshold
    stdv = max(covariance ** 0.5, 0.01)

    return stdv


def naive_bayes(training_file, test_file):

    allTrainingFile = []
    allTestFile = []
    openFile(training_file, 1, allTrainingFile, allTestFile)
    openFile(test_file, 0,  allTrainingFile, allTestFile)

    # predict for the test file
    # Given the training output, get the testing acurracy
    testingPhase(trainingPhase(allTrainingFile), allTestFile, allTrainingFile)



