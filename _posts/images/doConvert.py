#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import os
import time
import subprocess
import shutil
import sys

os.chdir(sys.path[0])
print(os.getcwd())

cacheFolder = os.getcwd() + "/temp/"
cacheFile = cacheFolder + "temp"
caches = []
generalSize = "640X640"

if(len(sys.argv) > 1) :
    wishSize = 640 * int(sys.argv[1])
    generalSize = "%dx%d" % (wishSize, wishSize)

def initRunner():
    path = os.getcwd()
    os.chdir(path)
    files = os.listdir(path)

    for file in files:
        arr = os.path.splitext(file)
        suffix = arr[-1]
        convert(file, suffix)

def checkTempFileExist():
    if not os.path.exists(cacheFolder):
        print("缓存文件生成.")
        os.makedirs(cacheFolder)

def loadCache():
    if not os.path.exists(cacheFile):
        return
    fp = open(cacheFile, "r")
    for c in fp:
        caches.append(c.replace("\n", ""))

def save(cache):
    fp = open(cacheFile, "a")
    fp.write(cache + "\n")

def replace_file_cache(currentTime, filename, who):
    curfile = os.getcwd() + "/" + filename
    shutil.move(curfile, cacheFolder + filename)
    shutil.move(who, curfile)
    save(filename)

def convert(filename, suffix):
    if filename in caches:
        print("%s已经转换" % filename)
        return
    currentTime = time.strftime('%Y%m%d', time.localtime(time.time()))
    who = ""
    if(suffix == ".gif"):
        print(filename + "开始转换")
        temp = "%s.gif" % currentTime
        who = cacheFolder + temp
        cmd = "gifsicle %s --colors 256 --resize-fit %s -o %s" % (filename, generalSize, who)
        os.system(cmd)
        replace_file_cache(currentTime, filename, who)
    elif(len(suffix) > 0):
        if(suffix == ".png"
           or suffix == ".jpg"):
            print(filename + "开始转换")
            temp = "%s.png" % currentTime
            who = cacheFolder + temp
            os.system("%s\/convert.sh %s %s %s" % (os.getcwd(), os.getcwd() + "/" + filename, generalSize, who))
            replace_file_cache(currentTime, filename, who)

print("开始...")
checkTempFileExist()
loadCache()
initRunner()
print("已结束.")
