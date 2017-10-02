#!/usr/bin/perl

use strict;
use warnings;
use Cwd;
use Getopt::Long qw(HelpMessage :config pass_through);

my $proj     = $ARGV[0] or die HelpMessage();
my $maxrun   = $ARGV[1] or die HelpMessage();
my $maxclone = $ARGV[2] or die HelpMessage();

my $currentrun = 0;
my $homedir    = getcwd();

while ($currentrun < $maxrun) {
    my $currentclone = 0;
    while ($currentclone < $maxclone) {
        my $workdir = "$homedir/PROJ$proj/RUN$currentrun/CLONE$currentclone/";
        chdir $workdir;
        my $test = getcwd();
        print STDOUT "Working on directory $test ...\n";
        `rm *# *.xvg *.pdb *.out *.nat *.nat6 temp* 2> /dev/null`;
        `mv frame0.tpr temp`;
        `rm *.tpr 2> /dev/null`;
        `mv temp frame0.tpr`;
        `mv ener.edr temp`;
        `rm *.edr 2> /dev/null`;
        `mv temp ener.edr`;
        $currentclone++;
    }
    $currentrun++;
}

print STDOUT "Done!\n";

=head1 NAME

fah-data-clean-up.pl - Remove unwanted files from a F@H dataset

=head1 SYNOPSIS

./fah-data-clean-up.pl <project_dir> <#_of_runs> <#_of_clones>

Run this script from the location of the F@H PROJ* directories to clean up unwanted files.
Currently removes all *.tpr and *.edr other than frame0.tpr and ener.edr. It also removes
*#, *.xvg, *.pdb, *.out, *.nat, *.nat6, and temp*.

=cut
