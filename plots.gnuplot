
set title 'Change in key lookup time as more nodes are disabled'
set ylabel 'Average time per lookup (s)'
set xlabel 'Trial'
set key left

graph_upper_bound = 50
graph_lower_bound = 0
graph_increment = 5
set macros

output_type="jpeg"
combined_str = "plot "
linear_str = "plot "

# Build command strings
do for [i = graph_lower_bound:graph_upper_bound:graph_increment] {
   eval sprintf("f%d(x) = m%d*x + b%d", i, i, i)
   eval sprintf("fit f%d(x) '%d_increase.dat' via m%d,b%d", i, i, i, i)
   if (i == graph_upper_bound){
      combined_str = sprintf("%s \'%d_increase.dat\' title \"remove %d nodes per trial\", f%d(x)", combined_str, i, i, i)
      linear_str = sprintf("%s f%d(x)", linear_str, i)
   } else{
        combined_str = sprintf("%s \'%d_increase.dat\' title \"remove %d nodes per trial\", f%d(x),", combined_str, i, i, i)
        linear_str = sprintf("%s f%d(x),", linear_str, i)
   }

}

eval combined_str

set term @output_type
set output sprintf('combined.%s', output_type)
replot

set term x11

set xrange [0:100]
set yrange [0:4.5]

eval linear_str

set term output_type
set output sprintf('linear.%s', output_type)
replot

set term x11
