# fah-data-cleanup

Scripts used for cleaning up the Folding@Home data

## fah-data-clean-up.pl

```sh
./fah-data-clean-up.pl <Absolute path to PROJ# directory>
```

Run this script to clean up unwanted files.
Currently removes all `*.tpr` and `*.edr` other than `frame0.tpr` and `ener.edr`. It also removes
`*#`, `*.xvg`, `*.pdb`, `*.out`, `*.nat`, `*.nat6`, `*.txt`, and `temp*`.
