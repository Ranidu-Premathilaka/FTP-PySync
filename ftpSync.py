#the file doesn't delete a file in ftp if it is removed update that

while(True):

    import os,sys,json,argparse,time
    from ftplib import FTP

    argParser = argparse.ArgumentParser()

    argParser.add_argument("-r", "--root",required=True, help="The root of the folder in this exact format no starting commas /wamp64/www/public ")
    argParser.add_argument("-o", "--outfile",required=False,default='previousMD.json',help="The name of the output file the default is 'previousMD.json'")
    argParser.add_argument("-t", "--time",required=False,default=10,help="The time gap between each check if a file is edited")
    argParser.add_argument("-H", "--host",required=True, help="The host name of the FTP server ex: ftpupload.net")
    argParser.add_argument("-u", "--user",required=True, help="The username of the FTP account")
    argParser.add_argument("-p", "--password",required=True, help="The password of the FTP account")
    argParser.add_argument("-d", "--directory",required=True, help="The directory of the FTP server the files should be coppied. ex: 'htdocs/test'")    
    
    args = argParser.parse_args()

    root = args.root
    outfile = args.outfile
    time = args.time
    host = args.host 
    user = args.user
    password = args.password
    directory = args.directory
     
     
    print(root)
    print(outfile)
    print("press ctrl + c to quit")


    path= os.path.join(root,"targetdirectory")

    mydic = {}
    delList = {}
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
                    
                del previousMD[key]
                
            except KeyError:
                ftpList.append(key)
                pass
        
        delList=previousMD;
        
        
                
    else:
        ftpList = list(mydic.keys())


    ftp = FTP(host,user,password)

    ftp.cwd(directory)


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
        ftp.cwd(directory)

    for key in delList:
        strippedKey=key.split(root+"\\",1)[1]
        ftp.delete(strippedKey)
    
    
        """
        strippedKey=key.split(root+"\\",1)[1].split("\\")
        ftp.cwd("/".join(strippedKey[:-1]))
        ftp.delete(strippedKey[-1])
       
        if not ftp.nlst(){
            
        }
        
        for i in strippedKey[1::-1]:
        
            try:
                ftp.mkd(i)
            except:
                pass
            ftp.cwd(i)
        file = open(key,'rb')
        store = ftp.storbinary('STOR {}'.format(strippedKey[-1]), file)
        print(strippedKey[-1],store)
        
        file.close()
        ftp.cwd(directory)
        """
        
    
    
    
    ftp.close()

    with open(outfile, "w") as out:
        json.dump(mydic, out)


    time.sleep(10)

