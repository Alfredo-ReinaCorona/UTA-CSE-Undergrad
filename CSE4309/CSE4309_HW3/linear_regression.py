import numpy as np


# Returns a polynomial basis function 
def polynomialBasisFunction(dataset, degree):
    
    # Feature Matrix
    phi = []
    for row in dataset:
        temp = [1]

        for attr in row[:-1]:
            # get phi values based on the degree and polynomial basis function 
            temp.extend([attr**(k+1) for k in range(degree)])

        phi.append(temp)

    # Convert to numpy array for ease of use
    return np.array(phi, dtype=float)


def linear_regression(training_file, test_file, degree, lamda):
    # Training
    #Goal is to estimate the weights
    trainingData = np.loadtxt(training_file)
    testData = np.loadtxt(test_file)

    phiValues = polynomialBasisFunction(trainingData, degree)
    I = np.identity(len(phiValues[0]))
    t = trainingData.T[-1]

    # Calculate weights using regularized least squares formula
    phi_transpose_phi = np.dot(phiValues.T, phiValues)
    w = np.dot(np.dot(np.linalg.pinv(lamda*I + phi_transpose_phi), phiValues.T), t)

    # Print weights calculated
    for i, weight in enumerate(w):
        print(f"w{i}={weight:.4f}")

    #-----------------------------
    # Testing 
    phi_test = polynomialBasisFunction(testData, degree)

    for i, row in enumerate(testData):
        output = float(np.dot(w.T, phi_test[i]))
        target = row[-1]
        error = float((target - output)**2)
        #print(f"ID={i+1:5d}, output={output:14.4f}, target value={target:10.4f},   squared error={error:.4f}")

        





