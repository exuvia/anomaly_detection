# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 01:21:49 2017

@author: Aboozar Mapar
@email: A.Mapar@gmail.com

This module includes the functions that I have used to analyze the social network
"""

# Defines the the n-the degree neighbor of the the node
def neighborhood(Graph, user_id, D = 1):
    """
    This functions finds D-th degree friends of a user.
    
    Inputs:
        Graph: is the input graph
        user_id: is the node that we are interested in finding its neigbours
        D: is the degree of the neigborhood
        D has a default value of 1
    
    Output:
        Returns list of nodes (not including the user itself)
    """
    import networkx as nx
    path_lengths = nx.single_source_shortest_path_length(Graph, user_id, cutoff = D)
    return [node for node, length in path_lengths.iteritems()
                    if length <= D and length > 0]
    
def mean_sd(Transactions):
    """
    Input:
        Transactions: is the input array that includes the purchase amounts
    
    Outputs:
        This function returns the followings:
        mean: is the average of the purchases
        sd: is the standard deviation
    """
    import numpy as np
    #mean = round(np.mean(Transactions),2)
    #sd = round(np.std(Transactions),2)

# To truncate instead of rounding
    mean = float(int(np.mean(Transactions)*100))/100
    sd = float(int(np.std(Transactions)*100))/100

    return mean, sd



def user_history(purchase_history, Graph, user_id, D=1, no_Trans=2):
    """
    This function uses the neighborhood and mean_sd functions
    to returns the mean and standard deviation for n-th neighbor of a user
    
    Inputs:
        purchase_history: purchase history of the network
        This is a dictionar witht he following format
        {user_id: [[amount, timestamp], ...]}
    
        Graph: A graph object that contains the social network conection data.
        user_id: user id
        D: Degree of friendship which does not includes the user itself
        D has a default value of 1.
        no_Trans: number of transactions
        This has a default value of 2.
    
    Outputs:
        This function returns
        mean: average of the purchases in ones network
        sd: standard deviation of purchases in ones netwrok
    """
    # Finding D-th neighbor of a user.
    # this function returns the user id and all D-th neighbor ids
    neighbor_list=neighborhood(Graph, user_id , D)

    # initialize the transaction list
    Transactions = []
    
    # Generating Purchase list for D-th neighbour of a user
    for node in neighbor_list:
        if node in purchase_history:
            # each row of purchase history contains an amount and a timestamp.
            # When transposed the first row contains transactions.
            Transactions.extend(purchase_history[node][-no_Trans:])
   
    
    # Calculate mean and standard deviation for a user social network history
    if len(Transactions) >= 2:
        # if no of transactions in the social network is greater than no_Trans
        # the data needs to be sorted. Otherwise all available data can be used 
        # to find mean and sd
        if len(Transactions) > no_Trans:
            # Sorting Transactons by timestamp
            Transactions.sort(key=lambda Column:Column[1])
            # Removing extra data. Just because we don't need it.
            del(Transactions[0:len(Transactions)-no_Trans])
            
        # To find the mean and sd for the last no_Trans or all Transaction< no_Trans
        mean, sd= mean_sd(zip(*Transactions)[0])
    else:
        # if less than two Transactions exists in the social network
        mean = []
        sd = []
    
    return mean, sd