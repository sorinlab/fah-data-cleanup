#!/usr/bin/perl

use strict;
use warnings;
use Cwd;
use Getopt::Long qw(HelpMessage :config pass_through);

my $projpath   = $ARGV[0] or die HelpMessage();

if (-d $projpath) {
    my @runs = &pattern_walk("RUN", $homedir);
    foreach my $run (@runs) {
        my @clones = &pattern_walk("CLONE", $run);
        foreach my $clone (@clones) {
            print STDOUT "Working on directory $clone ...\n";
            # `rm *# *.xvg *.pdb *.out *.nat *.nat6 temp* 2> /dev/null`;
            # `mv frame0.tpr temp`;
            # `rm *.tpr 2> /dev/null`;
            # `mv temp frame0.tpr`;
            # `mv ener.edr temp`;
            # `rm *.edr 2> /dev/null`;
            # `mv temp ener.edr`;
            # `rm *.txt 2> /dev/null`;
        }
    }
}
print STDOUT "Done!\n";

# Arguments: pattern to search for, absolute path of directory
sub pattern_walk {
    my ($pattern, $path, @dirs, $num_dirs);
    $pattern  = $_[0];
    $path     = $_[1];
    @dirs     = `ls $path | grep $pattern`;
    $num_dirs = scalar(@dirs);
    for (my $x = 0 ; $x < $num_dirs ; $x++) {
        my $dir = $dirs[$x];
        chomp $dir;
        $dirs[$x] = "$path/$dir";
    }
    return @dirs;
}

=head1 NAME

fah-data-clean-up.pl - Remove unwanted files from a F@H dataset

=head1 SYNOPSIS

./fah-data-clean-up.pl <Absolute path to PROJ# directory>

Run this script to clean up unwanted files.
Currently removes all *.tpr and *.edr other than frame0.tpr and ener.edr. It also removes
*#, *.xvg, *.pdb, *.out, *.nat, *.nat6, and temp*.

=cut
