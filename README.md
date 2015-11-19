## SuperFitter
# SuperFitter
HistFitter configuration scripts

## Example run
LimitScripts/LimitConfig.py now incorporates user arguments via OptionParser. To avoid HistFitter.py from grabbing these, you must provide the options to LimitConfig.py within the "-u" option of HistFitter.py, e.g.:

`HistFitter.py -twfp -D "allPlots" LimitScripts/LimitConfig.py -u '"-r SR -g bWN --doExcl"'`
