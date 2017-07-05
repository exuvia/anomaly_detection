# Table of Contents
1. [Project Summary](README.md#project-summary)
2. [Dependencies](README.md#dependencies)
3. [Running instructions](README.md#running-instructions)


# Project Summary
This project is written in `Python 2.7` and contains a `main.py` source file and two supporting module `parse_input.py` and `tools.py`. 

Processing of `stream_log.json` is done in the `main.py` file.

The functions that are used to parse `batch_log.json` are placed in `parse_input.py` module.

Additional functions that are used to find `D-th` degree friends of each user and functions to process purchase history are placed in `tools.py` module.


# Dependencies
The following python libraries are used in this project:

`sys`, `os`, `json`, `collections`, `numpy`, `networkx`


# Running instructions
The project can be executed with the following command:

```
python main batch_log.json stream_log.json flagged_purchases.json
```

as can be seen from the above, `main.py` takes three arguments from the command line. The first argument is the `batch_log.json` filename. This file contains the history of the social network events. The second argument is the `stream_log.json` filename. This file includes data that come from the real-time network stream. The code processes these two files and writes the flagged anomalous purchases in the file that is specified in the third argument `flagged_purchases.json`.
