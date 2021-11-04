# MasterThesis-JazzNetwork

## Introduction

There are many systems that take the form of networks, i.e. a set of nodes connected to each other by edges.
Among the systems most commonly studied in the literature, we find, among others, the network of hypertext
links on the *World Wide Web*, the network of scientific citation, the network of roads between cities in a country
or the networks related to biology.

This document (*and this code*) aims to answer the following question : **What are the parameters favouring the preferential attachment among jazz
musicians within a collaborative network ?**

## Requirements
`pip install networkx requests panda csv re unidecode BeautifulSoup scipy numpy itertools matplotlib powerlaw dynetx csv cv2 glob`


## Screenshot

![alt text](https://raw.githubusercontent.com/jbaudru/MasterThesis-JazzNetwork/main/data/pictures/community.png)

![alt text](https://raw.githubusercontent.com/jbaudru/MasterThesis-JazzNetwork/main/data/pictures/community1.png)


## To Do
- [ ] Refactor : move some main function to network class, create utility class
- [ ] Refactor : create class for video and dynamic networkx
- [ ] Delete : gender guesser et ethnicolr
- [ ] Create network for instrument (size of node depend of # musician)
