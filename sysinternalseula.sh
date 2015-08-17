#!/bin/bash

# Hop out to build boxes and fire off all the Sysinternals tools once using the "-accepteula" flag.
# If the build box image is missing the accepted eula flag file, or if the build scripts don't use the "-accepteula"
# flag, the build scripts can hang displaying an "accept eula?" dialog box.

for HOST in {aus-dpatchbld01,aus-dcsiwin01}
do
    scp -r /cygdrive/c/SysinternalsSuite/ hedev@$HOST:/cygdrive/c
    ssh hedev@$HOST "for FILE in {Clockres,Contig,Coreinfo,FindLinks,Listdlls,PsExec,PsGetsid,PsInfo,PsLoggedon,PsService,Tcpvcon,accesschk,autorunsc,diskext,du,handle,junction,livekd,logonsessions,procdump,psfile,pskill,pslist,psloglist,pspasswd,psshutdown,pssuspend,sdelete,sigcheck,streams,strings}; do /cygdrive/c/SysinternalsSuite/\$FILE.exe -accepteula; done";
done
