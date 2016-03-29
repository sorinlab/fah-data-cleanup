#!/usr/bin/perl 
use POSIX;
use Math::Complex;

########## global variables ####################
	$usage = "$0  [input]  [y] [y-min] [y-max] [y-resolution]   [x] [x-min] [x-max] [x-resolution] [TimeCut] [output]\n";

	$input   = $ARGV[0] || die "$usage\n";
	$Ycol    = $ARGV[1] || die "$usage\n";
	$Ymin    = $ARGV[2] || die "$usage\n";
	$Ymax    = $ARGV[3] || die "$usage\n";
	$Yreso   = $ARGV[4] || die "$usage\n";

	$Xcol    = $ARGV[5] || die "$usage\n";
	$Xmin    = $ARGV[6] || die "$usage\n";
	$Xmax    = $ARGV[7] || die "$usage\n";
	$Xreso   = $ARGV[8] || die "$usage\n";

	$TimeCut = $ARGV[9] || die "$usage\n";
	$output  = $ARGV[10]|| die "$usage\n";
	
    $maxX = (($Xmax - $Xmin)/$Xreso);
	$maxY = (($Ymax - $Ymin)/$Yreso);

##  Initializing
	for ($i=0; $i<$maxY; $i++){
	    for ($j=0; $j<$maxX; $j++){
	        $BIN{"$i:$j"} = 0;
	    }
	}

### open and read in the file and  ### 
	$totaldata = 0;
	open(INP,"<$input") || die "Cannot open input file $input. $!\n";
	while ($line = <INP>) {
	    chomp $line;
	    foreach($line) { s/^\s+//;s/\s+$//; s/\s+/ /g; }
	    @lines = split(/ /,$line);
	    if ($lines[3] >= $TimeCut){ #column where time is located, if time is greater than or equal to $TimeCut then proceed
	        $x = (($lines[$Xcol] - $Xmin)/$Xreso);
	        $y = (($lines[$Ycol] - $Ymin)/$Yreso);
	        $newx = floor($x);
	        $newy = floor($y);
	        $BIN{"$newy:$newx"}++;
	        $totaldata++;
	    }
	}
	close(INP);

### and print out the resulting matrix  ###
	open(OUT,">$output");
	#open(OUT2, ">$output2");
	# Rows are written
	for ($yy=0; $yy<$maxY; $yy++) {
	  for ($xx=0; $xx<$maxX; $xx++) { 
		printf OUT "%8d", $BIN{"$yy:$xx"}; 
		#if ($BIN{"$yy:$xx"} > 0){
		#	$freeEnergy = (-0.0019872 * 300 * logn($BIN{"$yy:$xx"}, 10));
		#	printf OUT2 "%8d  %8d  %8.4f\n", $xx, $yy, $freeEnergy;
		#}
	  } 
	  print OUT "\n";
	}
	print "\n";
	close(OUT);
