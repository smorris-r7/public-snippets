########## git
gpdowning - Glen Downing glen downing
ebanner   - Edward Banner edward banner
aseal134  - Aseal Yousef aseal yousef

quick setup -- if you've done this kind of thing before
https://github.com/sfmorris/cs373-collatz.git
...or create a new repository on the command line
echo "# cs373-collatz" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/sfmorris/cs373-collatz.git
git push -u origin master
...or push an existing repository from the command line
git remote add origin https://github.com/sfmorris/cs373-collatz.git
git push -u origin master

git clone https://github.com/sfmorris/somerepo.git -> p4 sync
git status 
git add somelocalfile -> mark for add
git diff HEAD -> view all changes between local workspace and HEAD
git commit -m "changelist description" -> p4 submit, only submits to repo, not github
git config --global --edit -> edit submitter's name and email
git push -> pushes to github.com
git branch -a -> list all branches local client knows about
git fetch -> syncs up branches (say, after one was created by hand on github.com)
git rev-parse HEAD -> get a SHA

git branching tutorial -> https://www.atlassian.com/git/tutorials/using-branches/git-branch

########## vi
:set list -> show invisible characters
:set nolist -> hide invisible characters

~/.exrc
set expandtab -> uses spaces instead of tab characters
set tabstop=4 -> use 4 spaces in a tab
set shiftwidth=4 -> use 4 spaces when block indenting

v -> visual mode, hit enter after marking some text and then d to delete

:%s/pattern/replace/g -> search and replace entire document (leave out '%' to just search/replace on one line), 'g' makes it do more than just the first instance on a line

0 -> jump to beginning of line

####### python
print("value of foo: %s, value of bar: %s".format(foo, bar))

virtualenv venv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install rauth
python3 ./SomeFile.py
python -c "import somemodule; print(somemodule.__file__)"
python -c "import sys; print(sys.path)"

###### bash
~/.profile -> has ultimate word on environment setup (well, for loggign in from home at least, see more at http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_03_01.html)
head -100 /u/downing/cs/netflix/probe.txt > ~/100.txt -> grab first 100 lines and dump to a file
python3.4 ./SomeScript.py < SomeInfile.txt > SomeOutfile.txt
for f in ../netflix-tests/*-RunNetflix.in; do echo "processing $f" && ./RunNetflix.py < $f | grep RMSE; done
top tutorial -> http://www.tecmint.com/12-top-command-examples-in-linux/

###### other misc etc
pydoc3 -w SomePythonFileNotIncludingDotPy -> creates SomePythonFile...DotPy.html
makefile tutorial http://mrbook.org/blog/tutorials/make/
to clear dns cache: ipconfig /flushdns
what shares are being mounted: /etc/auto.netmount
symbol store: Options > Debugging > Symbols > Symbol file (.pdb) locations

##### puppet
1. How do I tell the lasttime puppet ran:
# cat /tmp/last*

2. How do I see if the puppet daemon is running so I know it is getting automatic updates:
# service puppet status

3. How do I start the puppet daemon:
# service puppet start

4. How do I initiate a puppet run and see the output of the run at once:
#sudo /usr/sbin/puppetd --test

##### sql
$ sqlplus mgd/mgd@//ausmgddb01.aus.biowareonline.int:1521/bwamgdd1

set pagesize 0
set newpage 0

SELECT username FROM all_users ORDER BY username ASC;

MGD_1462_14_0,MGD_29_0,MGD_1478_10_0,MGD_1478_11_0,MGD_1478_11_0,MGD_1478_12_0,MGD_1478_9_0,MGD_1481_1_0,MGD_1481_12_0,MGD_1481_19_0,MGD_1481_23_0,MGD_1481_28_0,MGD_1481_33_0,MGD_1481_7_0,MGD_1482_2_0,MGD_1484_11_0,MGD_1484_12_0,MGD_1484_17_0,MGD_1484_26_0,MGD_1484_31_0,MGD_1484_6_0,MGD_1489_1_0,MGD_1489_11_0,MGD_1489_23_0,MGD_1489_15_0,MGD_1489_16_0,MGD_1489_19_0,MGD_1489_2_0,MGD_1489_20_0,MGD_1489_24_0,MGD_1489_25_0,MGD_1489_3_0,MGD_1489_4_0,MGD_1489_5_0,MGD_1489_6_0,MGD_1489_7_0,MGD_1490_10_0,MGD_1490_12_0,MGD_1490_18_0,MGD_1490_19_0,MGD_1490_25_0,MGD_1490_28_0,MGD_1490_31_0,MGD_1490_5_0,MGD_1492_0_0,MGD_1492_3_0

##### perforce
The -Dt flag allows integration around a deleted target file; if the target file is deleted, it is restored with the branched source file.
The -Ds flag allows integration around a deleted source file; if the source file has been deleted, any modified target file is also deleted.
The -Di flag ignores the fact that a source file was deleted and re-added when searching for an integration base.

get info about a changelist, -S flag will allow shelved: p4 describe -S 12345
latest revision synced (?): p4 -P armadill0! changes -m1 @prodpatcher01-shardtool_scripts

p4 -p osperforce01.bwa.biowareonline.int:1234 integrate -t -n -v -b sam14RepoHE2toHE6 //sam14Repo/repository/HE6/...@7979726

edit a bunch of stuff: grep -lr "node\.getAttribute(\"shareDrive" /cygdrive/c/auto/austin1/mmo1/build_system/release17/{scripts,configurations} | sed 's/\/cygdrive\/c/C\:/' | xargs -I {} p4 -p bwa-perforce01.bioware.com:1234 -c bwasammorris edit {}

preview resolve, list resolves needed: p4 resolve -n

settings: p4 set or ~/.p4qt/appsettings.xml

p4 unshelve -s <shelved cl> -c <desired pending cl>
-f forces

##### qb quickbuild
wrapper
    pre
    execute condition
    node selection
    command
    post

##### sed
grep -lr "node\.getAttribute(\"shareDrive" /cygdrive/c/auto/austin1/mmo1/build_system/release17/{scripts,configurations} | sed 's/\/cygdrive\/c/C\:/' | sed 's/\ /\\ /g' | xargs sed -i 's/node\.getAttribute(\"shareAddress/server\.getAttribute(\"shareAddress/g

##### windows
register a dll: regsvr32 MSVCR90.dll
unregister a dll: regsvr32 /u MSVCR90.dll
