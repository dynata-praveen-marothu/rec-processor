import subprocess,sys,sqlite3,traceback

def convert2mp3(bpath , wfile):

    lamecmd = [ "/usr/local/bin/lame", "-b", "16", "-m", "m", "-q", "9-resample" , bpath + "/incoming/" + wfile , bpath + "/mp3/" + wfile.replace(".wav",".mp3") ]

    ret=1

    try:
        res = subprocess.Popen(lamecmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
        output,error = res.communicate()
        ret=res.returncode
        if res.returncode == 0:
            print "SUCCESS : Convert to MP3 ..." + wfile
        else:
            print "ERROR : Convert to MP3 ..." + wfile
        
        print output
        print error

    except OSError as e:
        print "OSError > ",e.errno
        print "OSError > ",e.strerror
        print "OSError > ",e.filename
        traceback.print_exc()
    except:
        print "Error > ",sys.exc_info()[0]
        traceback.print_exc()

def syncRecordings(bpath,s3path):

    synccmd=["aws" , "s3" , "sync" , bpath , s3path]

    try:
        res = subprocess.Popen(synccmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
        output,error = res.communicate()
        ret=res.returncode
        if res.returncode == 0:
            print "SUCCESS : Syncing recordings"
        else:
            print "ERROR : Syncing recordings"

        print output
        print error

    except OSError as e:
        print "OSError > ",e.errno
        print "OSError > ",e.strerror
        print "OSError > ",e.filename
        traceback.print_exc()
    except:
        print "Error > ",sys.exc_info()[0]
        traceback.print_exc()

def copyRecordingDB(dbpath):

    synccmd=["aws" , "s3" , "cp" , dbpath , "s3://ssi-eic-recording/"]

    try:
        res = subprocess.Popen(synccmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
        output,error = res.communicate()
        ret=res.returncode
        if res.returncode == 0:
            print "SUCCESS : Copy recordings DB"
        else:
            print "ERROR : Copy recordings DB"

        print output
        print error

    except OSError as e:
        print "OSError > ",e.errno
        print "OSError > ",e.strerror
        print "OSError > ",e.filename
        traceback.print_exc()
    except:
        print "Error > ",sys.exc_info()[0]
        traceback.print_exc()



def save2DB(rec,recordingsdb):

    try:
        conn = sqlite3.connect(recordingsdb)
        cur = conn.cursor()
        cur.execute('insert or ignore into recordings values (?,?,?,?)', rec)
        conn.commit()
        conn.close()
    except sqlite3.Error as er:
        print er


