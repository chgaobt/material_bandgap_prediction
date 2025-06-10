# Running through the coding examples found in
# https://medium.com/google-developer-experts/graph-neural-networks-the-message-passing-algorithm-301b0080f418 
# for educational purposes 

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy import linalg

Adj = np.array(
    [[0, 0, 1, 0, 1],
     [0, 0, 0, 0, 1], 
     [0, 0, 0, 1, 1], 
     [0, 0, 1, 0, 1], 
     [1, 1, 0, 0, 0]]
)
g = nx.from_numpy_array(Adj)
pos = nx.circular_layout(g)

fig, ax = plt.subplots(figsize=(8,8))
nx.draw(g, pos, with_labels=True, 
    labels={i: i+1 for i in range(g.number_of_nodes())}, node_color='#f78c31', 
    ax=ax, edge_color='gray', node_size=1000, font_size=20, font_family='DejaVu Sans')

# plt.show()

# '@' is for matrix multiplication 
# .reshape(-1,1) transforms the array into a column vector --- 
# the -1 means that the dimension should be infered & 1 means the second dimension should be 1

# This is the message vector 
H = Adj @ np.array([1,2,3,4,5]).reshape(-1,1)                                               # Sum of connected neighborhoods

# print(Adj)
# print(H)

D = np.zeros(Adj.shape)                                                                     # Creates a new array of same size as Adj filled with zero
                                                                                            # This is known as the Diagonal Degree Matrix 

# axis = 0 -> sum along columns; axis = 1 -> sum along rows 
np.fill_diagonal(D, Adj.sum(axis=0))

# print(D)

# Next step is to assign a weight to each edge, done so by dividing the Identity Matrix by D 
# Essentially tells us how much weight each connection has on the total connectivity of the node in question

D_inv = np.linalg.inv(D)

# print(D_inv)

Avg_Adj = D_inv @ Adj
# print(Avg_Adj)

# Message Passing 
g = nx.from_numpy_array(Adj)

#np.eye used to create an identity matrix 
A_tilde = Adj + np.eye(g.number_of_nodes())

D_tilde = np.zeros_like(A_tilde)
# [matrix].flatten converts a multidimentional matrix into a 1D matrix
np.fill_diagonal(D_tilde, A_tilde.sum(axis=1).flatten())     # why over row this time? 

D_tilde_invroot = np.linalg.inv(linalg.sqrtm(D_tilde))
A_hat = D_tilde_invroot @ A_tilde @ D_tilde_invroot

print(A_hat)

# Message Passing Algorithm 
epochs = 9
information = [H.flatten()]
for i in range(epochs):
    H = A_hat @ H
    information.append(H.flatten())

