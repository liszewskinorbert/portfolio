# import modulow do programow
import os, time
import shutil, arrow, smtplib
from pathlib import Path
import locale
import configparser

config = configparser.RawConfigParser()
config.read('.\config.txt')
details_dict = dict(config.items('mysection'))

#Read config settings
user = details_dict['user']
pasw = details_dict['pasw']
maxUsage = details_dict['maxusage']
filesPath = details_dict['filespath']
ctime1 = details_dict['ctime1']
ctime2 = details_dict['ctime2']
Delete = details_dict['delete']
email = details_dict['email']
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
raportinfo=[] # raport content


def usageDisk():
    total, used, free = shutil.disk_usage("d://")
    rap=[]
    raportinfo.append("Total: %d GiB" % (total // (2**30)))
    raportinfo.append("Used: %d GiB" % (used // (2**30)))
    raportinfo.append("Free: %d GiB" % (free // (2**30)))
    raportinfo.append("Used in procent %d" %(used*100//total))
    cap = used*100/total
    return cap


def testCapacity():
    if capacity > int(maxUsage):
        value = "Disk used above %d percent" % int(maxUsage)
        return True, value
    else:
        value = "Disk used below %d percent" % int(maxUsage)
        return False, value



def deletingFiles():
    if testCap == True:
        val = "Sufficient disk space, we can remove files and directory"
        return val
    else:
        val = "Forget it, date raport %d" % time.time()
        return val

def lookForOldFiles():
    sizeOfFiles = 0
    onlyfiles = next(os.walk(filesPath))[2] #dir is your directory path as string
    raportinfo.append("We find %d backup files in main directory" % len(onlyfiles))
    if len(onlyfiles) < 3:
        raportinfo.append("Too small backup files")
    else:
        for item in Path(filesPath).glob('*'):
            criticalTime = arrow.now().shift(days=int(ctime1))
            #criticalTime = arrow.now().shift(days=ctime1)
            itemTime = arrow.get(item.stat().st_mtime)
            if itemTime < criticalTime and item.is_file():
                sizeOfFiles = sizeOfFiles + os.path.getsize(item)
                #print(os.path.getsize(item))
                #print(item)
                raportinfo.append(str(item))
            else:
                continue
    return sizeOfFiles



def lookForOldDirectory():
    countDir = 0
    countFile = 0

    raportinfo.append("\nFiles and Directory`s in backup`s")
    for root, dirs, files in os.walk(filesPath):
        for dir in dirs:
            countDir += 1
            raportinfo.append(os.path.join(root, dir))
            for file in files:
                #print(type(file))
                countFile += 1
                raportinfo.append(os.path.join(root, dir, file))
                #print(os.path.join(root, dir, file))

    if countDir >2:
        raportinfo.append("Directory count is above 2, is %d" % countDir)
        raportinfo.append("Count files is %d" % countFile)
        raportinfo.append("\n")
    else:
        pass
        #print("Too small backup files")


def directoryForDelete():
    raportinfo.append("\n")
    if Delete == "False":
        raportinfo.append("Passive mode, olny show files and directory`s to remove")
    else:
        raportinfo.append("Aggresive mode, files and directory`s was deleted")
    raportinfo.append("Files and directory`s to delete:")
    sizeOfDeleteFiles = 0

    for item in Path(filesPath).glob('*'):
        #criticalTime = arrow.now().shift(days=ctime2)

        criticalTime = arrow.now().shift(days=int(ctime2))
        itemTime = arrow.get(item.stat().st_mtime)

        if itemTime < criticalTime and item.is_dir():

            raportinfo.append(str(item))
            for root, dirs, files in os.walk(item):
                for file in files:
                    #print("test")
                    path = (os.path.join(root, file))
                    raportinfo.append(os.path.join(root, file))
                    sizeOfDeleteFiles = sizeOfDeleteFiles + os.path.getsize(path)
                    if Delete == "True":
                        os.remove(os.path.join(root, file))
                        raportinfo.append("Aggesive mode, data was deleted")

                if Delete == "True":
                    shutil.rmtree(os.path.join(item))

        else:
            continue
    return  sizeOfDeleteFiles

def sendEmail():

    mailFrom = 'Management system backup'
    mailTo = [email, ]
    mailSubject = 'Report from maked changes'
    raportFormat = ('\n'.join(raportinfo))
    mailBody = '''Hello, this is report from delete data\n
{}\nGood luck and have nice day'''.format(raportFormat)
    message='''From: {}
    Subject: {}

    {}
    '''.format(mailFrom, mailSubject, mailBody)


    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, pasw)
        server.sendmail(user, mailTo, message)
        server.close()
        print('Success')
    except:
        print('Error')



def main():
    usage = usageDisk()
    capacity = usage
    testCapacityValue = testCapacity()
    testCap = testCapacityValue[0]
    raportinfo.append(testCapacityValue[1])
    status = deletingFiles()
    raportinfo.append(status)
    oldFiles = lookForOldFiles()
    raportinfo.append("Files and directory in main place:" + f"{oldFiles:,} byte")
    lookForOldDirectory()
    lookForOldParm = directoryForDelete()
    raportinfo.append("We removed data  : " + f"{lookForOldParm:,} byte")

    #print(raportinfo)
    sendEmail()

if __name__ == '__main__':
        main()

