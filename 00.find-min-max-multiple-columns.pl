#!/usr/bin/perl

$fileinfo="perl script.pl  [input]  [column-start]  [column-end]  [output]";

# -----------------------------------------------------------------------------
# GET INPUT
	$input = $ARGV[0] or die "$fileinfo\n";
	$colStart = $ARGV[1] or die "$fileinfo\n";
	$colEnd = $ARGV[2] or die "$fileinfo\n";
	$output = $ARGV[3] or die "$fileinfo\n";


# -----------------------------------------------------------------------------
# VARIABLES
	@mins = (); # stores min values for all columns
	@maxs = (); # stores max values for all columns
	$range = $colEnd-$colStart+1; # the number of columns to loop on

# -----------------------------------------------------------------------------
# FIND MIN MAX
	open (INPUT, "<$input") or die "Cannot open input file $input. $!\n";
	while (my $line = <INPUT>){
		if(($.%10000)==0) { print "Processed lines: $i\n"; }
		chomp($line);
		foreach($line) { s/^\s+//; s/\s+$//; s/\s+/ /g; }
		my @items = split(/ /,$line);

		for(my $i=0; $i<=$range; $i++){
			# assign values from the first line to the arrays
			if($mins[$i]==""){ $mins[$i]=$items[$i+$colStart]; }
			if($maxs[$i]==""){ $maxs[$i]=$items[$i+$colStart]; }

			if($mins[$i]>$items[$i+$colStart]) { $mins[$i]=$items[$i+$colStart]; }
			if($maxs[$i]<$items[$i+$colStart]) { $maxs[$i]=$items[$i+$colStart]; }
		} # end of for
	}#end of while
	close INPUT;
 # -----------------------------------------------------------------------------
 # WRITE MIN MAX VALUES TO OUTPUT
 	open (OUTPUT, ">$output") or die "Cannot write to output file $output. $!\n";
	print OUTPUT "Col\tMin\tMax\n";
	for(my $i=0; $i<scalar(@mins); $i++){
		print OUTPUT ($i+$colStart),"\t",$mins[$i],"\t",$maxs[$i],"\n";
	}
	close OUTPUT;
