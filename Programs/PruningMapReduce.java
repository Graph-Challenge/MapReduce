import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class PruningMapReduce {

  //Mapper Operation
  public static class MapperOperation
       extends Mapper<Object, Text, Text, IntWritable>{

    private final static IntWritable degree = new IntWritable(1);
    private Text nodeID = new Text();

    public void map(Object key, Text edgeList, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer node = new StringTokenizer(edgeList.toString());
      while (node.hasMoreTokens()) {
        nodeID.set(node.nextToken());
        context.write(nodeID, degree);
      }
    }
  }

  //Reducer Operation
  public static class ReducerOperation
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable finalDegree = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int degree = 0;
      for (IntWritable val : values) {
        degree += val.get();
      }
	  
      //self-define parameter, N, number of nodes
      int N = 6;

      //Emit the nodes that do not have degrees 0, 1 and N - 1
      if (degree != 0 && degree != 1 && degree != N - 1){
        finalDegree.set(degree);
        context.write(key, finalDegree);
      }
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String temp_path = "temp";

    Job job = Job.getInstance(conf, "pruning");
    job.setJarByClass(PruningMapReduce.class);
    job.setMapperClass(MapperOperation.class);
    job.setReducerClass(ReducerOperation.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);

  }
}
