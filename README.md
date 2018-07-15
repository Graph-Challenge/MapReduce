# GraphChallenge - MapReduce Software Implementation

<p align="justify">Social network graphs become larger, the computational cost of using a single process to perform graph analytics may be too high. For example, if there are more than 100,000,000 edges, it may take a long time to read in each edge and count the degree of each vertex for a single process on computer. As such, we apply MapReduce in three different steps of the PHC algorithm, <i>(1) pruning step</i>, <i>(2) counting of intra-level triangles</i>, and <i>(3) counting of inter-level triangles</i>, so that our PHC algorithm can be run in parallel.</p>

## High-level architecture of the MapReduce implementation
<p align="justify">As shown below, we firstly put the data file on the HDFS, such that the NameNode can manage the file system namespace and determine the mapping blocks of DataNodes. Job Tracker can then monitor the the Task Trackers to perform MapReduce jobs.</p><br />
<img width="550" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/MapReduceHighLevelArchitecture.png"/>

## Pruning Step
<p align="justify">Applying MapReduce on the pruning step could significantly improve the performance of the PHC algorithm. In the example below, there are totally six vertices, each row in the edge list represents an edge, and each column contains two nodes. We put the edge list on the HDFS, such that Hadoop could split the file based on the block size and place them in different Mappers. In the example, we have four Mappers and each Mapper contains four key-value pairs. To count the degree of each vertex in the Reducer, we use the node ID as the key, and value 1 for all vertices. After shuffling, the total degree can be calculated by adding up the values of each key in the Reducer. Lastly, the Reducer can filter out the nodes that do not have degrees 0, 1 and N' - 1.</p><br />
<img width="800" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/PruningMapReduce.png"/>


## Intra-level Triangles
<p align="justify">We can create a data structure to store nodes in each level and set the custom input split size to ensure that each Mapper can access a complete cluster at any one time. Because we could know the size of each cluster, we can set the inpt split size based on the cluster size. We can then apply the PHC algorithm to count the intra-level triangles of cluster in each Mapper and send the result to Reducer. Reducer can add up the number of triangles in each cluster and calculate the total number of intra-level triangles of all clusters.</p><br />
<img width="900" height="350" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Images/IntraLevelMapReduce.png"/>
