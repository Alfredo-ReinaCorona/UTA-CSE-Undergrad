from value_iteration import value_iteration

# When you test your code, you can select the function arguments you 
# want to use by modifying the next lines

#data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW7/Environment_Files/environment1.txt"
data_file = "/home/alfredo/Documents/CSE4309/CSE4309_HW7/Environment_Files/environment2.txt"
ntr = -.04 # non_terminal_reward
gamma = .9
K = 20


value_iteration(data_file, ntr, gamma, K)
