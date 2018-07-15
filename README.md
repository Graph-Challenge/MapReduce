# GraphChallenge - MapReduce Software Implementation

Social network graphs become larger, the computational cost of using a single process to perform graph analytics may be too high. For example, if there are more than 100,000,000 edges, it may take a long time to read in each edge and count the degree of each vertex for a single process on computer. As such, we apply MapReduce in three different steps of the PHC algorithm, <i>(1) pruning step</i>, <i>(2) counting of intra-level triangles</i>, and <i>(3) counting of inter-level triangles</i>, so that our PHC algorithm can be run in parallel.

## High-level Architecture of the MapReduce implementation
As shown below, we firstly put the data file on the HDFS, such that the NameNode can manage the file system namespace and determine the mapping blocks of DataNodes. Job Tracker can then monitor the the Task Trackers to perform MapReduce jobs.<br />
<img width="550" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/MapReduceHighLevelArchitecture.png"/>

## Pruning Step
Applying MapReduce on the pruning step could significantly improve the performance of the PHC algorithm. In the example below, there are totally six vertices, each row in the edge list represents an edge, and each column contains two nodes. We put the edge list on the HDFS, such that Hadoop could split the file based on the block size and place them in different mappers.<br />
<img width="800" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/PruningMapReduce.png"/>
