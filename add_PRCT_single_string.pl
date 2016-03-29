#!/usr/bin/env perl

$usage = "$0  -i <input.txt>  -o <output.txt>";

if (scalar @ARGV == 4)
{
    for (my $i = 0; $i < scalar @ARGV; $i++)
    {
        if ($ARGV[$i] eq "-i")
        {
            $i++;
            $input = $ARGV[$i];
            next;
        }

        elsif ($ARGV[$i] eq "-o")
        {
            $i++;
            $output = $ARGV[$i];
            next;
        }
    }
}
elsif ($ARGV[0] =~ m/[(-h)(--help)]/)
{
    print "$usage\n";
    exit;
}
else
{
    print "ERROR: There is one or more invalid arguments.\n";
    print "$usage\n";
    exit;
}

open INPUT, "<$input" or die "Cannot open $input. $!.\n";
open OUTPUT, ">$output" or die "Cannot open $output. $!\n";

while (my $line = <INPUT>)
{
    if ($. % 20000 == 0) { print "."; }
    my $original_line = $line; chomp $original_line;
    foreach($line) { s/^\s+//; s/\s+$//; s/\s+/ /g; }
    my @items = split(' ', $line);
    my $timestamp = "$items[0]:$items[1]:$items[2]:$items[3]";
    print OUTPUT "$timestamp\t$original_line\n";
}
