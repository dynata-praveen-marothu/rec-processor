#!/usr/bin/python

import os, sys ,datetime,sqlite3,pwd,grp
from fn import convert2mp3,save2DB,syncRecordings,copyRecordingDB

now = datetime.datetime.now()
dtnow = now.strftime("%Y%m%d")

print "[" + now.strftime("%Y%m%d %H:%M:%S") + "] : Executing process-recordings.py"

if len(sys.argv) > 1:
    dtnow=sys.argv[1]
    
basepath     = "/vox/" + dtnow 
s3recpath    = "s3://ssi-eic-recording/recordings/" + dtnow
mp3path      = basepath + "/mp3"
wavpath      = basepath + "/incoming"
recordingsdb = "/vox/db/recordings.db"

if not os.path.exists(basepath):
    sys.exit()

if not os.path.exists(wavpath):
    sys.exit()

if not os.path.exists(wavpath + "/processed.txt"):
    open( wavpath + "/processed.txt" , 'a').close()

if not os.path.exists(mp3path):
    os.makedirs(mp3path)


pifiles = set([ line.rstrip('\n') for line in open( wavpath + "/processed.txt" )])
aifiles = set([ file + "~" + str(os.path.getmtime( wavpath + "/" + file )) for file in os.listdir( wavpath ) if file.endswith(".wav") ])

pfiles = [ file_t for file_t in list( aifiles - pifiles ) ]


for file_t in pfiles:
    file= file_t.split("~")[0]
    lst = file.split('-')
    dt  = lst[0][0:4] + '-' + lst[0][4:6] + '-' + lst[0][6:8] 
    tm  = lst[1][0:2] + ':' + lst[1][2:4] + ':' + lst[1][4:6]

    dtm = dt + ' ' + tm
    agt = lst[2]
    phn = lst[3]
    rec = file

    if os.path.getsize( wavpath + "/" + file) > 50:
        convert2mp3(basepath , file)
        save2DB( ( dtm,agt,phn,rec ),recordingsdb )
        with open( wavpath + "/processed.txt", 'a') as f:
            f.write( file_t + "\n" )
    
syncRecordings( basepath,s3recpath )
copyRecordingDB( recordingsdb )

