#!/usr/bin/perl 
use POSIX;

########## global variables ####################
$usage = "\nUsage: \.\/make_2D_histogram\.pl [starting number] [end number] [X-column] [X-min] [X-max] [X-resolution]\n";

$startNum = 0;
$endNum = $ARGV[0] || die "$usage\n";
$Xmin  = $ARGV[1] || die "$usage\n";
$Xmax  = $ARGV[2] || die "$usage\n";
$Xres  = $ARGV[3] || die "$usage\n";

for ($x=$startNum; $x<=$endNum; $x++){
print "Starting on cluster $x.....\n";
	$newFile = "Cluster_$x"."_population-data.txt";
	if (-e $newFile){
		for ($y=4;$y<11;$y++){
			$output = "$newFile"."-col$y".".bins";
			system("perl Make_1D_histogram.pl $newFile $y $Xmin $Xmax $Xres $output");
		}
	}
}
