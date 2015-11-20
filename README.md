# SuperFitter
HistFitter configuration scripts

## Recommendations and Setup
HistFitter has a recommended tag. But I recommend not to use that one. Currently I have confirmed that HistFitter-00-00-49 works (with ROOT 5.34).

To setup an area make sure that you have your kerberos ticket (to check out HistFitter from SVN) and do:

```
source checkoutHF.sh 00-00-49
cd HistFitter-00-00-49
source setup_UCIT3.sh
source setup.sh
cd src/
make
```
and then copy the LimitScripts/ directory here,
`cp -r ../LimitScripts/ .`

This last procedure is more for convenience and actually just clutters up your directory structure (duplicate LimitScripts/ directories :)). If you do not want to do it just be sure to adjust the calls to LimitScripts, etc... to have the correct relative paths. 

## Example run
Before running setup an environment variable that gets used by the scripts inside of LimitScripts/. Inside your HistFitter directory (e.g. HistFitter-00-00-49/),
```
source ../setlimits
```
which will setup the environment variable "LIMITDIR" pointing to the LimitScripts/ directory in this HistFitter directory. 

LimitScripts/LimitConfig.py now incorporates user arguments via OptionParser. To avoid HistFitter.py from grabbing these, you must provide the options to LimitConfig.py within the "-u" option of HistFitter.py, e.g.:

```
HistFitter.py -twfp -D "allPlots" -u '"-r SR -g bWN --doExcl"' LimitScripts/LimitConfig.py
```

## Making Combined Trees for HistFitter Inputs
There is the script `makeCombinedTrees.py`.
