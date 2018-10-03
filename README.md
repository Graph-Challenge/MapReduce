# GraphChallenge - MapReduce Software Implementation

<p align="justify">As network graphs become larger, the computational cost of using a single process to perform graph algorithms may be too high. For example, if there are more than 100,000,000 edges, it may take a long time to read in each edge and count the degree of each vertex for a program running on a single computer. We propose to apply MapReduce in three different steps in our PHC algorithm, <i>(1) pruning step</i>, <i>(2) counting of intra-level triangles</i>, and <i>(3) counting of inter-level triangles</i>, so that our PHC algorithm can enable parallel computation of graph algorithms.</p>

## High-level Architecture of the MapReduce Implementation
<p align="justify">As shown below, we first put the data file on the HDFS such that the Name Node can manage the file system namespace and determine the mapping blocks of each Data Node. Job Tracker can then monitor Task Tracker to perform MapReduce jobs.</p>
<p align="center">
  <img width="650" height="600" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Pictures/MapReduceHighLevelArchitecture.png"/>
</p>

## Pruning Step
<p align="justify">Applying MapReduce on the pruning step could significantly improve the performance of the PHC algorithm. In the example below, there are in total six vertices, each row in the edge list represents an edge, and each column contains two nodes. We put the edge list on the HDFS, such that Hadoop can split the file based on the block size and place them in different Mappers. In the example, we have four Mappers and each Mapper contains four key-value pairs. To count the degree of each vertex in the Reducer, we use the node ID as the key, and value 1 for all vertices. After shuffling, the total degree can be calculated by adding up the values of each key in the Reducer. Lastly, the Reducer can identify the nodes that do not have degrees 0, 1 and N' - 1.</p>
<p align="center">
  <img width="800" height="330" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Pictures/PruningMapReduce.png"/>
</p>

## Intra-level Triangles
<p align="justify">We can create a data structure to store nodes at each level and set the custom input split size to ensure that each Mapper can access a complete cluster at any one time. Since we know the size of each cluster, we can set the inpt split size based on the cluster size. We can then apply the PHC algorithm to count the intra-level triangles for each cluster in each Mapper and send the result to a Reducer. The Reducer can add up the number of triangles in each cluster and calculate the total number of intra-level triangles of all clusters.</p>
<p align="center">
  <img width="900" height="330" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Pictures/IntraLevelMapReduce.png"/>
</p>

## Inter-level Triangles
<p align="justify">We can use the same data structure to store nodes at each level and set a larger custom input split size to ensure that each Mapper can access two levels at any time. Similar MapReduce operation can be performed to count the inter-level triangles.</p>
<p align="center">
  <img width="900" height="340" src="https://github.com/Graph-Challenge/MapReduce/blob/master/Pictures/InterLevelMapReduce.png"/>
</p>
