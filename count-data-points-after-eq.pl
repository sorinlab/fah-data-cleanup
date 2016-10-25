#!/usr/bin/env perl

# Author: Khai Nguyen
# Date:   Mar 2015
# Purpose: This script counts the number of data points after a pre-determined
#          conformational equilibrium time point (in microseconds).

$input = $ARGV[0];
$cutoff = 6000; # conformational equilibrium established at 6000 microseconds
$count = 0; # number of data points 

# -------- Read all-data points and count the number of data points after
#          the cut-off time ----------------------------------------------------
	open (INPUT, "<", $input)
	or die "Cannot open $input. $!.\n";

	while (my $line = <INPUT>)
	{
		chomp($line);

		foreach ($line)
		{
			s/^\s+//;
			s/\s+$//;
			s/\s+/ /g;
		}

		my @items = split(' ', $line);

		my $time = $items[3];
		if ($time >= $cutoff) 
		{
			$count++;
		}

	}

	close INPUT;
	print("Number of data point after $cutoff microseconds: $count.\n");