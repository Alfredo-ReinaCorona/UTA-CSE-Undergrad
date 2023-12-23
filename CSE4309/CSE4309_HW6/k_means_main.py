from k_means import *

#data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW6/Toy_Datasets/set1a.txt"
#data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW6/Toy_Datasets/set2a.txt"
data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW6/Toy_Datasets/set2c.txt"
#data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW6/Toy_Datasets/set2_1.txt"

K = 2
#initialization = "random"
initialization = "round_robin"


k_means(data_file, K, initialization)
