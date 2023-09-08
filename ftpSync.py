#the file doesn't delete a file in ftp if it is removed update that

while(True):

    import os,sys,json,argparse,time
    from ftplib import FTP

    argParser = argparse.ArgumentParser()

    argParser.add_argument("-r", "--root",required=True, help="the root of the folder in this exact format no starting commas /wamp64/www/public ")
    argParser.add_argument("-o", "--outfile",required=False,default='previousMD.json',help="the name of the output file the default is 'previousMD.json'")

    args = argParser.parse_args()

    root = args.root
    outfile=args.outfile

     
     
    print(root)
    print(outfile)


    path= os.path.join(root,"targetdirectory")

    mydic = {}
    ftpList = []
    fileExist = False
    global ftp


    if(os.path.isfile(outfile)):    
        with open(outfile) as infile:
            previousMD = json.load(infile)
            fileExist = True


    for path, subdirs, files in os.walk(root):
        
        for name in files:
            filePath = os.path.join(path, name)
            modifiedDate = os.path.getmtime(os.path.join(path, name))
            mydic[filePath] = modifiedDate



    if(fileExist):
        for key in mydic:
            try:
                if(mydic[key] == previousMD[key]):
                    continue
                else:
                    ftpList.append(key)
            except KeyError:
                ftpList.append(key)
                pass
                
    else:
        ftpList = list(mydic.keys())


    ftp = FTP('ftpupload.net','epiz_34296651','9AESNB4wG4b0')

    ftp.cwd('htdocs')


    for key in ftpList:
        
        strippedKey=key.split(root+"\\",1)[1].split("\\")
        for i in strippedKey[:-1]:
            try:
                ftp.mkd(i)
            except:
                pass
            ftp.cwd(i)
        file = open(key,'rb')
        store = ftp.storbinary('STOR {}'.format(strippedKey[-1]), file)
        print(strippedKey[-1],store)
        
        file.close()
        ftp.cwd('/htdocs')

    ftp.close()

    with open(outfile, "w") as out:
        json.dump(mydic, out)


    time.sleep(10)

