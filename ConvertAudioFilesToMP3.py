#!/usr/bin/env python
# -*-coding:Latin-1 -*

# Converts audio files to MP3 files in directory <CONVERT_DIR>


import os
from pathlib import Path
import re
import shutil

def main():

    # Files directory (replace '\' with '/')
    CONVERT_DIR = "C:/DIRECTORY/TO/CONVERT"

    # Program (absolute) path (replace '\' with '/')
    PROGRAM_PATH = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"

    # Bitrate
    BIT_RATE = 128

    convertFilesToMP3(CONVERT_DIR, PROGRAM_PATH, BIT_RATE)


def convertToDOSPath(dir):
    return dir.replace("/", "\\")

def convertToPythonPath(dir):
    return dir.replace("\\", "/")


def convertFilesToMP3(CONVERT_DIR, PROGRAM_PATH, BIT_RATE):

    # Check VLC location 
    if(not os.path.isfile(PROGRAM_PATH)):
        print("ERROR: VLC not found. Please check your VLC installation path.")
        os.system("pause")
        exit()

    # Check directory
    if(not os.path.isdir(CONVERT_DIR)):
        print("ERROR: Directory", CONVERT_DIR, "does not exist")
        os.system("pause")
        exit()
        
    #os.chdir(source_dir)
    print("Converting files in", CONVERT_DIR, "...")
    print()

    CONVERT_DIR = convertToPythonPath(CONVERT_DIR)
    PROGRAM_PATH = convertToPythonPath(PROGRAM_PATH)

    # Convert files in directory
    nbTotal  = 0
    nbConverted = 0
    for dirname, dirnames, filenames in os.walk(CONVERT_DIR):

        #print("Processing directory", dirname)
        dirname = convertToDOSPath(dirname)

        # Browse files
        for filename in filenames:
            if(re.search('.aac', filename) is not None or re.search('.m4a', filename) is not None or re.search('.ogg', filename) is not None):
                nbTotal += 1
                srcFile = os.path.join(dirname, filename)
                srcFileBase = os.path.basename(srcFile)
                srcFileWithoutExt = Path(srcFileBase).stem
                dstFileBase = re.sub('\s\(\d{2,3}kbit_(AAC|Opus)\)', "", srcFileWithoutExt)
                dstFileBase = re.sub('_OLD_', "", dstFileBase)
                dstFile = os.path.join(dirname, dstFileBase + ".mp3")
                oldFile = os.path.join(dirname, "_OLD_" + filename)
                #print(srcFile)
                #print(dstFile)
                
                # Execute program command
                progDir = os.path.dirname(os.path.abspath(PROGRAM_PATH))
                progExe = os.path.basename(os.path.abspath(PROGRAM_PATH))
                os.chdir(progDir)

                print("Converting file", srcFile, "...")
                tmpFile = os.path.join(dirname, "_output_.mp3")
                cmd = progExe + " -I dummy \"" + srcFile + "\" " + "\":sout=#transcode{acodec=mpga,ab=" + str(BIT_RATE) + "}:std{dst=" + tmpFile + ",access=file}\" vlc://quit"
                #print(cmd)
                os.system(cmd)
                
                # Post-process: replace filenames
                os.rename(srcFile, oldFile)
                os.rename(tmpFile, dstFile)
                nbConverted += 1        

    # Print result
    print()
    if( nbTotal == nbConverted ):
        print("OK")
    else:
        print("Error")
        
    print("Total Files      ", nbTotal)
    print("Converted Files  ", nbConverted)


main()

# Wait for user input to close program (Windows)
os.system("pause")
