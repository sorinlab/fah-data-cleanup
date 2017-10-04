# fah-data-cleanup

Scripts used for cleaning up the Folding@Home data

## fah-data-clean-up.pl

```sh
./fah-data-clean-up.pl <project_dir> <#_of_runs> <#_of_clones>
```

Run this script from the location of the F@H PROJ* directories to clean up unwanted files.
Currently removes all `*.tpr` and `*.edr` other than `frame0.tpr` and `ener.edr`. It also removes
`*#`, `*.xvg`, `*.pdb`, `*.out`, `*.nat`, `*.nat6`, and `temp*`.