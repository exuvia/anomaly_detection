# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:53:00 2017

@author: Aboozar Mapar
@email: A.Mapar@gmail.com

This project is written in Python 2.7 and contains a 'main.py` source file and
two supporting module `parse_input.py` and `tools.py`. 

Processing of `stream_log.json` is done in the `main.py` file.

The functions that are used to parse `batch_log.json` are placed in
`parse_input.py` module.

Additional functions that are used to find `D-th` degree friends of and to
process purchase history are placed in `tools.py` module.

"""

import sys
import os
import json
from collections import OrderedDict
import tools
import parse_input as prs



# Checking command line arguments
batch_fullname, stream_fullname, flagged_fullname = prs.Process_CLArg(sys.argv)

# Parsing the training data    
D, T, purchase_history, G = prs.parser(batch_fullname)


# Checking the validity of flagged purchase filename
try: 
    flagged_file= open(flagged_fullname, 'w')
except:
        print "\n*** Error: {} is not a valid filename.".format(os.path.split(flagged_fullname)[1])
        print "Please run the script with the following filenames:"
        print "python {} batch_log_file  stream_log_file  flagged_purchase_file".format(sys.argv[0])
        sys.exit("Terminating the process.")

# Initialize process history
processed_history={}

# Parsing the streaming data
Line_No = 0
with open(stream_fullname) as data_file:
    
    # Separating purchases and friendship events
    for line in data_file:
        Line_No = Line_No + 1
        # handeling exceptions        
        try:
            line_content = json.loads(line, object_pairs_hook=OrderedDict)
            
            # purchase event
            if line_content['event_type'] == 'purchase':
                mean, sd = tools.user_history(purchase_history, G, int(line_content['id']), D, T)
                purchase_history.setdefault(int(line_content['id']), [])
                purchase_history[int(line_content['id'])].append([float(line_content['amount']),
                                str(line_content['timestamp'])])

                # if there is two or more purchases in a user social network history
                # mean and sd will have some value. Otherwise mean and sd
                # can't be calculated. 
                if mean != []:
                    # checking to see if a purchase is anomalous 
                    if float(line_content['amount']) > mean + 3*sd:
                        # Adding mean and sd to the flag
                        flag = line_content
                        flag['mean'] = "{:.2f}".format(mean)
                        flag['sd']= "{:.2f}".format(sd)
                        
                        #writing the flag to file
                        json.dump(flag, flagged_file)
                        flagged_file.write('\n')
                        
            # friendship event                            
            elif line_content['event_type'] == 'befriend':
                G.add_edge(int(line_content["id1"]),int(line_content["id2"]))

            # break up event    
            elif line_content['event_type'] == 'unfriend':
                G.remove_edge(int(line_content["id1"]),int(line_content["id2"]))
                
            else:
                print "\n** Warning: Bad data format in line {} of {}.".format(Line_No, stream_fullname)

        # handeling exceptions
        except:
            print "\n** Warning: Bad data format in line {} of {}.".format(Line_No, stream_fullname)
               
flagged_file.close() 

print "\nThe following files were processed:"
print "    1- Batch log data was read from: {}".format(batch_fullname)
print "    2- Stream log data was read from: {}".format(stream_fullname)
print "Results were saved in: {}".format(flagged_fullname)
print "Done!"
