#!/usr/bin/perl
my $old_fh = select(STDOUT);
$| = 1;
select($old_fh);

# ====================================================================================
# USAGE INFO & GETTING ARGUMENTS
	$usage  = "$0  [input]  [column#]  [column label]\n";
	$input  = $ARGV[0] or die $usage;
	$column = $ARGV[1] or die $usage;
    $label  = $ARGV[2] or die $usage;
# ====================================================================================


# ====================================================================================
# DETERMINING MIN & MAX BY BUBBLE SORTING
	open (INPUT,  "<$input")  or die "ERROR: Cannot open input file $input. $!.\n";

	while (my $line = <INPUT>) 
    {
		foreach($line) { s/^\s+//;s/\s+$//; s/\s+/ /g; }
		@line = split(/ /,$line);

        if ($. % 10000 == 0) { print "|"; }

        if ($. == 1)
        {
            $min = $line[$column];
            $max = $line[$column];
        }
        else
        {
		    if ($line[$column] > $max) { $max = $line[$column]; }
		    if ($line[$column] < $min) { $min = $line[$column]; }
        }
	}

    print "\nFor column [$column] ($label)\n";
	print "Max value is $max\n";
	print "Min value is $min\n";

	close INPUT;
