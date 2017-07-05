# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 00:25:26 2017

@author: Aboozar Mapar
@email: A.Mapar@gmail.com


The functions that are used to check the command line arguments and 
to parse `batch_log.json` are placed in this module.
"""


"""
This function checks the input arguments and terminates the program if there is 
and error.

Input:
    Command line argurments
    
Output:
    Boolean

"""
def Check_CLArg(Arguments):
    import os.path
    # Reading the command line parameters
    
    if len(Arguments) == 4:
        flag = True
        for Arg in Arguments[1:3]:
            if not os.path.isfile(Arg):
                print "\n*** Error: {} does not exist.".format(Arg)
                flag= False
        
        if not os.path.exists(os.path.split(Arguments[3])[0]):
            try:
                os.makedirs(os.path.split(Arguments[3])[0])
                print "\n*** Warning: {} does not exist. Creating a new directory.".format(os.path.split(Arguments[3])[0])
            except:
                print "\n*** Error: {} does not exist and cannot be created.".format(os.path.split(Arguments[3])[0])
                flag= False

    else:
        print "\n*** Error: This script takes exactly 3 arguments ({} given).".format(len(Arguments)-1)
        print "If you want to run the code with default filenames, do not enter any command line arguments."
        flag= False

    if flag == False:
        print "\nPlease run the script with the following filenames:"
        print "python {} batch_log_file  stream_log_file  flagged_purchase_file".format(Arguments[0])

    return flag


"""
This function checks the input arguments and returns the name of the input and 
output json files.
and error.

Input:
    Command line argurments
    
Output:
    File names for batch_fullname, stream_fullname, flagged_fullname

"""
def Process_CLArg(Arguments):
    import sys
    import os.path
    
    if len(Arguments) == 1:
        batch_fullname = os.path.abspath(os.path.join(os.path.dirname(Arguments[0]), '..', 'log_input','batch_log.json'))
        stream_fullname = os.path.abspath(os.path.join(os.path.dirname(Arguments[0]), '..', 'log_input','stream_log.json'))
        flagged_fullname = os.path.abspath(os.path.join(os.path.dirname(Arguments[0]), '..', 'log_output','flagged_purchases.json'))
        print "\n*** Warning: No command line arugument provided. Asumming the default filenames."
        print "python {} {}  {}  {}".format(Arguments[0],os.path.relpath(batch_fullname),
                      os.path.relpath(stream_fullname), os.path.relpath(flagged_fullname))
        

    elif len(Arguments) == 3:
        flagged_fullname = os.path.abspath(os.path.join(os.path.dirname(Arguments[0]), '..', 'log_output','flagged_purchases.json'))
        print type(Arguments), Arguments, flagged_fullname
        
        Arguments.append(flagged_fullname)
        print type(Arguments), Arguments, flagged_fullname
        print "\n*** Warning: No filename for flagged purchase file is provided. Asumming the default the filename."                
        print "python {} {}  {}  {}".format(Arguments[0],os.path.relpath(Arguments[1]),
                      os.path.relpath(Arguments[2]), os.path.relpath(flagged_fullname))
        if Check_CLArg(Arguments):
            batch_fullname = os.path.abspath(Arguments[1])
            stream_fullname = os.path.abspath(Arguments[2])
        else:
            sys.exit("\nWrong command line arguments. Terminating the process.")           

    elif Check_CLArg(Arguments):
        batch_fullname = os.path.abspath(Arguments[1])
        stream_fullname = os.path.abspath(Arguments[2])
        flagged_fullname = os.path.abspath(Arguments[3])

    else:
        sys.exit("\nWrong command line arguments. Terminating the process.")

    return batch_fullname, stream_fullname, flagged_fullname



"""
This functions checks if a string contains an interger.

Input:
    String
    
Output:
    True/False
"""
def checkInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False




"""
This function parse the batch_data.

Input:
    filename
    
Outputs:
    D: the number of degrees that defines a user's social network
    T: the number of consecutive purchases made by a user's social network
        (not including the user's own purchases)
    purchase_history: A dictionary with the following format
        { User_ID, [amount, timestamp], [amount, timestamp], ...}
        This variable contains information of all social network history.
    G: is a Graph object that defines the social network conection data.
"""

def parser(filename):
    
    import json
    from collections import OrderedDict
    import networkx as nx
    
    
    # Initialize the graph
    G=nx.Graph()
    
    # Initializing a list to track purchase activity of each user
    purchase_history={}
    
    # Reading past data and writing separating the purchases and friendship events
    with open(filename) as batch_data:
        Line_No = 1
        
        # Reading the first line and saving D and T
        line=batch_data.readline()
        line_content = json.loads(line, object_pairs_hook=OrderedDict)
        
        if checkInt(line_content['D']):
            D=int(line_content['D'])
        else:
            D=1
            print "\n** Warning: Bad data format in line {} of for D. Assuming default value D=1.".format(Line_No)

        if checkInt(line_content['T']):
            T=int(line_content['T'])
        else:
            T=2
            print "\n** Warning: Bad data format in line {} of for T. Assuming default value T=2.".format(Line_No)
        
        
        # Separating purchases and friendship events
        for line in batch_data:
            Line_No = Line_No + 1
            # handeling exceptions            
            try:
                line_content = json.loads(line, object_pairs_hook=OrderedDict)      
    
                # purchase event
                if line_content['event_type'] == 'purchase':
                    purchase_history.setdefault(int(line_content['id']), [])
                    purchase_history[int(line_content['id'])].append([float(line_content['amount']), 
                                    str(line_content['timestamp'])])
                # friendship event    
                elif line_content['event_type'] == 'befriend':
                    G.add_edge(int(line_content["id1"]),int(line_content["id2"]))
                # break up event        
                elif line_content['event_type'] == 'unfriend':
                    G.remove_edge(int(line_content["id1"]),int(line_content["id2"]))
              
                else:
                    print "\n** Warning: Bad data format in line {} of {}.".format(Line_No, filename)                    

            # handeling exceptions                    
            except:
                print "\n** Warning: Bad data format in line {} of {}.".format(Line_No, filename)                          
             
    return D, T, purchase_history, G




