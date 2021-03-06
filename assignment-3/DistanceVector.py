﻿# Assignment 3 for OMS6250
#
# This defines a DistanceVector Node that can fun the Bellman-Ford
# algorithm. The TODOs are all related to implementing BF. Students should
# modify this file as necessary, guided by the TODO comments and the
# assignment instructions. This is the only file that needs to be modified
# to complete the project.
#
# Copyright 2015 Dave Lillethun & Sean Donovan

from Node import *
from helpers import *

class DistanceVector(Node):
    #TODO: You need to have a structure that contains current distances
   
    def __init__(self, name, topolink, neighbors):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structors
        specific to a DV node is done here.'''
	
        super(DistanceVector, self).__init__(name, topolink, neighbors)
        #TODO: You may need to initialize your distance vector data structure
	self.distances = {}
	self.distances[self.name] = 0
	
    def __str__(self):
        ''' Returns a string representation of the Distance Vector node. '''

        #TODO: (optional) You may want to modify this to print your distance info.
        retstr = self.name + " : links ( "
        for neighbor in self.links:
            retstr = retstr + neighbor #+ " , distance = " + str(self.distances[neighbor])  + " " 
        return retstr + ")"


    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. '''

        for neighbor in self.links:
            # TODO - Build message
            msg = self.distances

            # Send message to neighbor
            self.send_msg(msg, neighbor)


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # TODO: The Bellman-Ford algorithm needs to be implemented here.
        # 1. Process queued messages
        # 2. Send neighbors updated distances
	
	updated = False
        # Process queue:
        for msg in self.messages:
            # TODO: Do something
	    print msg
	    for node in msg.keys():
		# all links have a weight of one
		new_weight = msg[node] + 1 
		if node in self.distances:
		   # we have a link to the node in the message 
		   if self.distances[node] > new_weight: 
		       self.distances[node] = new_weight
		       updated = True
                else:
                    self.distances[node] = new_weight
		    updated = True
                        
        # Empty queue
        self.messages = []

	# update links
        print "Update Links"
   	if updated == True:
	    self.send_initial_messages()


    def log_distances(self):
        ''' Prints distances in the following format (no whitespace either end):
        A:A0,B1,C2
        A is the node were on,
        B is the neighbor, 1 is it's distance
        A0 shows that the distance to self is 0
        Taken from topo1.py '''

        # TODO: The string in the format above (no newlines, no whitepsace) must
        # be defined. Then log with write_entry, example below. You'll need to 
        # make a loop over all the switches and call add_entry() (see helpers.py)
        # for each switch.
        
	 
	for key in  self.topology.topodict.keys():
	    logstring = ""
	    switch = self.topology.topodict[key]
	    for node in sorted(switch.distances):
	        logstring = logstring + node + str(switch.distances[node]) + ","
	    logstring = logstring[:-1]
	    add_entry(switch.name, logstring)