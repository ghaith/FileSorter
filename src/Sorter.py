'''
Created on Feb 20, 2012

@author: ghaith
'''

import os
import Image
from ExifTags import TAGS
from datetime import datetime
from mutagen.easyid3 import EasyID3
import mutagen
from shutil import copyfile

class Sorter(object):
    '''
    classdocs
    '''
    
    def __init__(self,origin,destination):
        '''
        Constructor
        '''
        
        #Get Files from path
        global files
        files = os.listdir(origin)
        global originFolder
        originFolder = origin
        global destinationFolder
        destinationFolder = destination
        global music
        music = ['mp3','wma','ogg','wav','aac','m4a']
        global images
        images = ['jpg','png','bmp','gif','raw','jpeg','tif']
        global documents
        documents = ['doc','xls','ppt','odt','ods','pdf','docx','pptx','xlsx','zip','rar','7z','gz']
        global videos
        videos = ['avi','mov','mpg','mp4','flv','wmv']
    
    def parseFiles(self):
        count = 1
        total = len(files)
        for fname in files:
            newname = None
            fileName = os.path.join(originFolder,fname)
            print "Processing " + fileName
            extension = os.path.splitext(fileName)[1][1:].lower()
            if extension in music:
                newname = self.parseMusic(fileName)
            elif extension in images:
                newname = self.parseImage(fileName)
            elif extension in documents:
                newname = self.parseDocument(fileName)
            elif extension in videos:
                newname = self.parseVideo(fileName)
            if newname is not None:
                #Before renaming, let's test teh first new runs to make sure it's printing correctly
                #os.rename(fname, newname)
                newname = os.path.join(destinationFolder,newname)
                print 'Operation: ' + str(count) + ' of ' + str(total) + ' - copy ' + fileName + ' to ' + newname
                newdir = os.path.split(newname)[0]
                if not os.path.exists(newdir):
                    os.makedirs(newdir)
                
                copyfile(fileName, newname)
                
            else:
                print fname + ' skipped'
            count = count +1
        #print count
        
    def parseMusic(self,oldName):
        if os.path.splitext(oldName)[1].lower() == '.mp3':
            newname = self.__parseMp3(oldName)
        else:
            #newname = os.path.join(os.path.split(oldName)[0],"Audio",os.path.split(oldName)[1])
            newname = os.path.join("Audio",os.path.split(oldName)[1].strip())
        return newname
    
    def parseImage(self,oldName):
        if os.path.splitext(oldName)[1].lower() in ('.jpg','.jpeg'):
            newname = self.__parsePicture(oldName)
        else:
            #newname = os.path.join(os.path.split(oldName)[0],"Images",os.path.split(oldName)[1])
            newname = os.path.join("Images",os.path.split(oldName)[1].strip())
        return newname
    
    def parseDocument(self,oldName):
        #This should be made smarter, maybe split each document to a folder
        #return os.path.join(os.path.split(oldName)[0],"Documents",os.path.split(oldName)[1])
        return os.path.join("Documents",os.path.split(oldName)[1].strip())
        
    def parseVideo(self,oldName):
        if os.path.splitext(oldName)[1].lower() in ('.avi'):
            newname = self.__parseMovie(oldName)
        else:
            #newname = os.path.join(os.path.split(oldName)[0],"Videos",os.path.split(oldName)[1])
            newname = os.path.join("Videos",os.path.split(oldName)[1].strip())
        return newname
        
    def __parseMp3(self,oldName):
        addedPath = 'Music'
        try:
            m = EasyID3(oldName)#MP3(oldName,id3=EasyID3)
            artist = m['artist'][0] if 'artist' in m else ''
            album = (m['date'][0] if 'date' in m else '') + (' - ' if 'album' in m or 'date' in m else '') + (m['album'][0] if 'album' in m else '')
            for path in artist,album:
                addedPath = os.path.join(addedPath,path)
        except mutagen.id3.ID3NoHeaderError:
            addedPath = os.path.join(addedPath,'No ID3')
        except mutagen.id3.ID3BadUnsynchData:
            addedPath = os.path.join(addedPath,'Damaged ID3')
        return os.path.join(addedPath,os.path.split(oldName)[1].strip())
        #This should contain id3 tags reading logic, for now just create a folder called music
        #return os.path.join(os.path.split(oldName)[0],"Music",os.path.split(oldName)[1])
    
    def __parsePicture(self,oldName):
        #This should return image parsing logic, for now just create a folder called Pictures
        addedPath = 'Pictures'
        #Open the image here, if it's damaged, we saved it in Damaged folder under creation date 
        try: 
            i = Image.open(oldName)
            damaged = False
        except IOError:
            damaged = True
            addedPath = os.path.join(addedPath,'Damaged')
            print 'Could not open image' + oldName
            
        
        info = self.__get_exif(i) if not damaged else {}
        #if the image has exif data, we parse it
        camera = ''
        model = ''
        if len(info) != 0:
            print info['DateTime'] if 'DateTime' in info else 'No Date'
            try :
                imageDate = datetime.strptime(info['DateTime'].replace('\x00',''),'%Y:%m:%d %H:%M:%S') if 'DateTime' in info and info['DateTime'] != '' else ''
            except:
                imageDate = ''
            camera = info['Make'].strip().replace('.','').replace('\x00','') if 'Make' in info else ''
            model = info['Model'].strip().replace('.','').replace('\x00','') if 'Model' in info else ''
            
        else:
            imageDate = datetime.fromtimestamp(os.path.getctime(oldName))
        dateFolder = os.path.join(str(imageDate.year),str(imageDate.month)) if imageDate != '' else ''
        for path in camera,model,dateFolder:
            addedPath = os.path.join(addedPath,path)
        #return os.path.join(os.path.split(oldName)[0],addedPath,os.path.split(oldName)[1])
        return os.path.join(addedPath,os.path.split(oldName)[1].strip())
    
    def __get_exif(self,i):
        ret = {}
        try:
            info = i._getexif()
            if info is not None:
                for tag,value in info.items():
                    decoded = TAGS.get(tag,tag)
                    ret[decoded] = value
        
        except: 
            ret = {} 
        return ret
            
    def __parseMovie(self,oldName):
        #This should contain logic to parse movies, for now just create a folder called Movies
        #return os.path.join(os.path.split(oldName)[0],"Movies",os.path.split(oldName)[1])
        return os.path.join("Movies",os.path.split(oldName)[1].strip())
    