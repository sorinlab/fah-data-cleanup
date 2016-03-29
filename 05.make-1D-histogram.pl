#!/usr/bin/env perl
use strict;
use warning;
use POSIX;

########## global variables ####################
$usage = "Usage: $0 [data file] [X-column] [X-min] [X-max] [X-resolution]";

$data = $ARGV[0] || die "$usage\n";
$Xcol = $ARGV[1] || die "$usage\n";
$Xmin = $ARGV[2] || die "$usage\n";
$Xmax = $ARGV[3] || die "$usage\n";
$Xres = $ARGV[4] || die "$usage\n";
$output = $ARGV[5] || die "$usage\n";

# open and read in the file and
# store each data point as pairs
$totaldata = 0;

open(INP, "<", $data) || die "Cannot open $data.$!\n";
while (my $line = <INP>) 
{
    for($line) { s/^\s+//;s/\s+$//; s/\s+/ /g; }
    my @values = split(/ /, $line);
    $X{$totaldata} = $values[$Xcol];
    $totaldata++;
}
close(INP);
print STDOUT "Total data points read is $totaldata.\n";

### initialize the array that counts bin populations  ###
my $numXbins = ($Xmax - $Xmin)/$Xres;
my %bin = ();

for (my $i = 0; $i <= $numXbins; $i++)
{
    $bins{$i} = 0;
}

### transform data (i,j) indeces to match bin numbers
### and do the binning of data points below
for (my $dat = 0; $dat < $totdat; $dat++)
{
    my $i = ($X{$dat} - $Xmin)/$Xres;
    my $ii = floor($i);
    $bins{$ii}++;
}

### and print out the resulting matrix  ###
open(OUT, ">", $output);
for (my $i = 0; $i < $numXbins; $i++)
{   
    printf OUT "%8f\t%8d\n", $Xmin+($i * $Xres), $bins{$i};
}
close(OUT);
