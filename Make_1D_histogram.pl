#!/usr/bin/perl 
use POSIX;

########## global variables ####################
$usage = "\nUsage: \.\/make_2D_histogram\.pl [data file] [X-column] [X-min] [X-max] [X-resolution] [CutOff]\n";

$data  = $ARGV[0] || die "$usage\n";
$Xcol  = $ARGV[1] || die "$usage\n";
$Xmin  = $ARGV[2] || die "$usage\n";
$Xmax  = $ARGV[3] || die "$usage\n";
$Xres  = $ARGV[4] || die "$usage\n";
$output =$ARGV[5] || die "$usage\n";
#$output= "$data".".bins";

### open and read in the file and  ### 
### store each data point as pairs ###
$totaldata = 0;
open(INP,"<$data");
while ($line = <INP>) {
  chomp $line;
  for($line) { s/^\s+//;s/\s+$//; s/\s+/ /g; }
  @temp = split(/ /,$line);
#  if (int($temp[11])>=int($TimeCut)) #specify column where time is located
#  {
     $X{$totaldata} = $temp[$Xcol]; 
     $totaldata++;
#  }
} 
close(INP);
$totdat = $totaldata;
print STDOUT "Total data points read = $totdat\n\n";


### initialize the array that counts bin populations  ###
$numXbins = ($Xmax - $Xmin)/$Xres;
for($i=0;$i<=$numXbins;$i++){
   $bins{"$i"} = 0;  
}


### transform data (i,j) indeces to match bin numbers ###
### and do the binning of data points below ###
for($dat=0;$dat<$totdat;$dat++){
  $i = ($X{$dat} - $Xmin)/$Xres;
  $ii = floor($i);
  $bins{"$ii"}++;
}

### and print out the resulting matrix  ###
open(OUT,">$output");
for ($p1=0;$p1<$numXbins;$p1++) {
  printf OUT "%8f\t%8d\n",$Xmin+($p1*$Xres),$bins{"$p1"};   
}
close(OUT);
