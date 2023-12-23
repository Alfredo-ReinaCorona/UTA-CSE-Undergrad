simport numpy as np
import random
import math


def openDataset(dataset):
    allData = np.loadtxt(dataset, dtype=float)

    #cannot be 0 for some reason
    dimensions = 2
    #all data files will either be 1D or 2D
    if len(allData.shape) == 1:
        dimensions = 1
        return allData, dimensions

    elif len(allData.shape) != 1:
        dimesnsions = 2
        return allData, dimensions
    
#Initial point to cluster initialization
def roundRobinClusters(allData, clusters, dimensions, K):
    assignedClusters = []
    clusterNum = 0

    #iterate over every line in the file and put it into a tuple with a cluster
    for line in allData:
        cluster = clusters[clusterNum]

        if dimensions == 2:
            assignedClusters.append((list(line), cluster))
        else:
            assignedClusters.append((line, cluster))

        clusterNum += 1
        if clusterNum == K:
            clusterNum = 0

    return assignedClusters

#Initial point to cluster initialization
def randomClusters(allData, clusters, dimensions):
    assignedClusters = []

    for line in allData:
        cluster = random.choice(clusters)

        if dimensions == 2:
            assignedClusters.append((list(line), cluster))
        elif dimensions == 1:
            assignedClusters.append((line, cluster))

    return assignedClusters

#Get the average location of each cluster
def averageClusterLocation(assignedClusters,clusters, dimensions, K):

    #define a list that will contain the average location of K clusters
    #if set to 0 it may cause division by 0
    avgLocation = [1]*K
    numEachCluster = [1]*K
    count = 0

    avgX = [0]*K
    avgY = [0]*K

    #Average X-coordinate = (Sum of X-coordinates) / (Number of Points)
    #Average Y-coordinate = (Sum of Y-coordinates) / (Number of Points)
    if dimensions == 2:
        for entry in assignedClusters:
            for i in range(len(clusters)):
                if entry[1] == clusters[i]:
                    avgX[i] += entry[0][0]
                    avgY[i] += entry[0][1]
                    numEachCluster[i] += 1

        #get the average X and Y locations of each cluster
        for i in range(len(avgX)):
            avgX[i] = avgX[i] / numEachCluster[i]
            avgY[i] = avgY[i] / numEachCluster[i]

            #return a list of tuples(coordinates for each cluster avg)
            avgLocation[i] = (avgX[i],avgY[i])

              
    
    #Average Location = (Sum of Data Points) / (Number of Data Points)
    elif dimensions == 1:
        #get the sum of and number of points in each cluster
        for entry in assignedClusters:
            for i in range(len(clusters)):
                if entry[1] == clusters[i]:
                    avgLocation[i] += entry[0]
                    numEachCluster[i] += 1

        #divide the sum of each cluster by their number of points
        for i in range(len(avgLocation)):
            avgLocation[i] = avgLocation[i] / numEachCluster[i] #division by 0 possible

    # print(numEachCluster)
    # print(avgX)
    # print(avgY)
    # print("\n", avgLocation)

    return avgLocation

#internal function. Get the distance of the closest cluster(for 2 dimensional data only)
def distance2D(point, avgClusterLoc):
    #given 1 point and the list of average cluster locations, return the  closest cluster
    index = 0
    distances = []
    
    #iterate over every cluster center
    for i in range(len(avgClusterLoc)):
        distances.append(math.sqrt((avgClusterLoc[i][0] - point[0])**2 + (avgClusterLoc[i][1] - point[1])**2))
    #point[0] = X
    #point[1] =Y

    #get the index of the closest cluster
    index = distances.index(min(distances))
    index += 1

    #returns the string denoting the closest cluster
    return "Cluster"+str(index)


def reassignPointsToCluster(assignedClusters, dimensions, clusters, avgClusterLoc, K):

    newAssignedClusters = []
    target = 0
    closestClusterLoc = 0
    closestClusterLocIndex = 0

    # access X coordinate assignedClusters[i][0][0]
    # access Y coordinate assignedClusters[i][0][1]
    # X of avgLoc avgClusterLoc[i][0]
    # Y of avgLoc avgClusterLoc[i][1]
    
    if dimensions == 2:
        for i in range(len(assignedClusters)):
            newAssignedClusters.append((assignedClusters[i][0],distance2D(assignedClusters[i][0],avgClusterLoc)))

    elif dimensions == 1:
        for i in range(len(assignedClusters)):
            #find the closest number to the 
            target = assignedClusters[i][0]
            closestClusterLoc = min(avgClusterLoc, key=lambda x: abs(x - target))
            closestClusterLocIndex = avgClusterLoc.index(closestClusterLoc)
            closestClusterLocIndex +=1
            newAssignedClusters.append((assignedClusters[i][0], "Cluster"+str(closestClusterLocIndex)))

    #return a tuple in the format 
    #1D: "(int, "Cluster[K]")"
    #2D: "((int,int), "Cluster[K]")"
    return newAssignedClusters

#Steps
# 1) Initialize the number of clusters and their average locations(K_avg) 
# 2) Assign each datapoint a cluster through "random" or "round robin"

# 3) Calculate Euclidian Distance to the average location of each cluster
# 4) assign each allData point to the nearest K_avg
# 5) update K_avg

# 6) if K_avg is the same as the previous iteration of K_avg, stop, you are done
# 7) if K_avg changes goto step 2 and repeat until complete


def k_means(data_file, K, initialization):
    
    allData, dimensions = openDataset(data_file)
    clusters = []
    newAssignedClusters = []
    tempAssignedClusters = []
    count =0

    num = 1
    #Make the list of clusters to put into the tuple
    for i in range(K):
        clusters.append("Cluster"+str(num))
        num+=1
    
    #Assign each row of the file to a cluster depending on the initalization value
    if initialization == "round_robin":
        assignedClusters = roundRobinClusters(allData, clusters, dimensions, K)
        
    elif initialization == "random":
        assignedClusters = randomClusters(allData, clusters, dimensions)

    #Calculate the average location of each cluster
    avgClusterLoc = averageClusterLocation(assignedClusters, clusters, dimensions, K)

    newAssignedClusters = reassignPointsToCluster(assignedClusters, dimensions, clusters, avgClusterLoc, K)

    #------------
    # Loop until Both lists of tuples are equal

    while newAssignedClusters != tempAssignedClusters:
        newAssignedClusters = reassignPointsToCluster(assignedClusters, dimensions, clusters, avgClusterLoc, K)

        #calc new avg
        avgClusterLoc = averageClusterLocation(newAssignedClusters, clusters, dimensions, K)

        #temp assignedclusters to compare
        tempAssignedClusters = reassignPointsToCluster(assignedClusters, dimensions, clusters, avgClusterLoc, K)

    #------------

    # for i in range(len(assignedClusters)):
    #     print("Original: ",assignedClusters[i],"  New: ",newAssignedClusters[i])
    for i in range(len(assignedClusters)):
        print(newAssignedClusters[i][0], " ----> ", newAssignedClusters[i][1])








 
    

