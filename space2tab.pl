#!/usr/bin/perl

$fileInfo = "perl script.pl [input-file] [output-file]";

$input  = $ARGV[0] or die $fileInfo;
$output = $ARGV[1] or die $fileInfo;

open (INPUT, "<$input") or die "Cannot open input file $input. $!.\n";
open (OUTPUT, ">$output") or die "Cannot open output file $output. $!.\n";

while (my $line = <INPUT>){
	chomp ($line);
	foreach($line) { s/^\s+//;s/\s+$//; s/\s+/\t/g; }
	print OUTPUT "$line\n";
}
close INPUT;
close OUTPUT;
