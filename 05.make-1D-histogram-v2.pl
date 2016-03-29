#!/usr/bin/perl -w
use POSIX;


$usage = "\nUsage: ./make-1D-histogram-v2.pl  [data file]  [column]  [output]\n";

# ------------------------------------------------------------------------------------
# GET ARGUMENTS
	$data  = $ARGV[0] || die "$usage\n";
	$Xcol  = $ARGV[1] || die "$usage\n";
	$output= $ARGV[2] || die "$usage\n";





# ------------------------------------------------------------------------------------
# FIND MIN MAX
	open (INPUT, "<$data") or die "Cannot open input file $data. $!\n";
	$max = 0;
	$min = 0;
	while (my $line = <INPUT>){
		chomp($line);
		for($line) { s/^\s+//; s/\s+$//; s/\s+/ /g; }
		@items = split(/ /, $line);

		# If reading in the first line
		if (($.==1) and ($max==0)) { $max = $items[$Xcol]; }
		if (($.==1) and ($min==0)) { $min = $items[$Xcol]; }

		if ($.!=1){
			if ($max<$items[$Xcol]) { $max = $items[$Xcol]; }
			if ($min>$items[$Xcol]) { $min = $items[$Xcol]; }
		}
	}
	close INPUT;


# ------------------------------------------------------------------------------------
# ASK USER FOR RESOLUTION BASED ON MIN MAX
	print "For the ", $Xcol+1, "th column\n";
	print "\tMax value is: $max\n";
	print "\tMin value is: $min\n";
	print "\tRange is: ", $max-$min, "\n";
	print "Please enter appropriate bin size (resolution): ";
	$Xres  = <STDIN>;

### open and read in the file and  ### 
### store each data point as pairs ###
	$totaldata = 0;
	open(INPUT,"<$data") or die "Cannot open input file $data. $!\n";
	$totaldata = 0;
	while (my $line = <INPUT>) {
		chomp $line;
		for($line) { s/^\s+//; s/\s+$//; s/\s+/ /g; }
		@items = split(/ /,$line);
		$X{$totaldata} = $items[$Xcol];
		$totaldata++;
	} 
	close(INPUT);
	$totdat = $totaldata;
	print STDOUT "Total data points read = $totdat\n\n";


	### initialize the array that counts bin populations  ###
	$numXbins = ($max - $min)/$Xres;
	for($i=0;$i<=$numXbins;$i++){
		 $bins{"$i"} = 0;  
	}


	### transform data (i,j) indeces to match bin numbers ###
	### and do the binning of data points below ###
	for($dat=0;$dat<$totdat;$dat++){
		$i = ($X{$dat} - $min)/$Xres;
		$ii = floor($i);
		$bins{"$ii"}++;
	}

	### and print out the resulting matrix  ###
	open(OUT,">$output") or die "Cannot write to output file $output. $!\n";
	for ($p1=0;$p1<$numXbins;$p1++) {
		printf OUT "%8f\t%8d\n",$min+($p1*$Xres),$bins{"$p1"};   
	}
	close(OUT);