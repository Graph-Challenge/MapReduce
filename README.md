# GraphChallenge - MapReduce Software Implementation

We apply MapReduce in three different steps of the PHC algorithm, <i>(1) pruning step</i>, <i>(2) counting of intra-level triangles</i>, and <i>(3) counting of inter-level triangles</i>.

## High-level Architecture of the MapReduce implementation
As shown below, we firstly put the data file on the HDFS, such that the NameNode can manage the file system namespace and determine the mapping blocks of DataNodes. Job Tracker can then monitor the the Task Trackers to perform MapReduce jobs.
<img width="550" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/MapReduceHighLevelArchitecture.png"/>

