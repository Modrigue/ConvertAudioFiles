#!/usr/bin/env python
# -*-coding:Latin-1 -*

# Converts all audio files in specified directory to MP3 files


import os
from pathlib import Path
import re
import shutil
import subprocess
import sys, getopt

# Files to be converted directory (replace '\' with '/')
CONVERT_DIR = ""

# Default program (absolute) path (replace '\' with '/')
PROGRAM_PATH = "C:/Program Files/VideoLAN/VLC/vlc.exe"
#PROGRAM_PATH = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"

# Default output format
OUTPUT_FORMAT = "mp3"

# Default bitrate
BIT_RATE = 128

def main(argv):

    global CONVERT_DIR
    global PROGRAM_PATH
    global OUTPUT_FORMAT
    global BIT_RATE
    
    try:
        opts, args = getopt.getopt(argv,"hd:r:p:o:",["help","dir=","rate=","program=","output-format="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-d", "--dir"):
            CONVERT_DIR = arg
        elif opt in ("-r", "--rate"):
            BIT_RATE = arg
        elif opt in ("-p", "--program"):
            PROGRAM_PATH = arg
        elif opt in ("-o", "--output-format"):
            OUTPUT_FORMAT = arg

    if(not CONVERT_DIR):
        print('Error: conversion directory is missing')
        printHelp()
        return

    convertFilesToMP3(CONVERT_DIR, PROGRAM_PATH, OUTPUT_FORMAT, BIT_RATE)


def convertToDOSPath(dir):
    return dir.replace("/", "\\")

def convertToPythonPath(dir):
    return dir.replace("\\", "/")


def convertFilesToMP3(convertDir, programPath, outputFormat, bitRate):

    # Check VLC location 
    if(not os.path.isfile(programPath)):
        print("ERROR: VLC not found. Please check your VLC installation path.")
        os.system("pause")
        exit()

    # Check directory
    if(not os.path.isdir(convertDir)):
        print("ERROR: Directory", convertDir, "does not exist")
        os.system("pause")
        exit()
        
    #os.chdir(source_dir)
    print("Converting files in", convertDir, "...")
    print()

    convertDirStr = convertToPythonPath(convertDir)
    programPathStr = convertToPythonPath(programPath)
    
    extString = f".{outputFormat.lower()}"
    formatsToProcess = [".aac", ".m4a", ".ogg", ".opus", ".wma"]
    if (extString == ".wav"):
        formatsToProcess.append(".mp3")
    else:
        formatsToProcess.append(".wav")


    # Convert files in directory
    nbTotal  = 0
    nbConverted = 0
    for dirname, dirnames, filenames in os.walk(convertDirStr):

        #print("Processing directory", dirname)
        dirname = convertToDOSPath(dirname)

        oldString = "_OLD_"

        # Browse files
        for filename in filenames:

            # Process file given format
            processFile = False
            for format in formatsToProcess:
                processFile |= (re.search(format, filename) is not None)

            if (processFile):
                nbTotal += 1
                srcFile = filename
                srcFileBase = os.path.basename(srcFile)
                srcFileWithoutExt = Path(srcFileBase).stem
                dstFileBase = re.sub('\s\(\d{2,3}kbit_(AAC|Opus)\)', "", srcFileWithoutExt)
                dstFileBase = re.sub(oldString, "", dstFileBase)
                dstFile = dstFileBase + extString
                if(not filename.startswith(oldString)):
                    oldFile = oldString + filename
                else:
                    oldFile = filename
                
                #print(srcFile)
                #print(dstFile)
                
                # Execute program command
                progDir = os.path.dirname(os.path.abspath(programPathStr))
                progExe = os.path.basename(os.path.abspath(programPathStr))
                os.chdir(dirname)
                #print("CURRENT DIR = " + os.getcwd())

                print("Converting file", os.path.join(dirname, filename), "...")
                tmpFile = f"_output_{extString}"
                if (extString == ".wav"):
                    cmd = "& " + "\'" + programPathStr  + "\'" + " -I dummy \"" + srcFile + "\" " + "\":sout=#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=" + tmpFile + ",access=file}\" vlc://quit"
                else:
                    cmd = "& " + "\'" + programPathStr  + "\'" + " -I dummy \"" + srcFile + "\" " + "\":sout=#transcode{acodec=mpga,ab=" + str(bitRate) + "}:std{dst=" + tmpFile + ",access=file}\" vlc://quit"
                #print(cmd)
                subprocess.run(['powershell', "-Command", cmd], capture_output=True)
                
                # Post-process: replace filenames
                os.rename(srcFile, oldFile)
                if(os.path.exists(dstFile)):
                    # if already existing, add (<n>)
                    dstFileBase = dstFile
                    dstFileCreated = False
                    index = 0
                    while(not dstFileCreated):
                        index += 1
                        dstFileWithoutExt = Path(dstFileBase).stem
                        dstFileWithoutExt += " (" + str(index) + ")"
                        dstFile = os.path.join(dirname, dstFileWithoutExt + extString)
                        if(not os.path.exists(dstFile)):
                            # ok, create file
                            os.rename(tmpFile, dstFile)
                            dstFileCreated = True
                else:
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


def printHelp():
    print()
    print('Usage: python ConvertAudioFilesToMP3.py -d <directory>')
    print()
    print("Options:")
    print("  -d, --dir <dir>:       directory to bulk convert audio files in")
    print("  -o, --output-format:   output format (mp3 or wav, default: mp3)")
    print("  -r, --rate <rate>:     bit rate (default: 128 kb)")
    print("  -p, --program <path>:  path to VLC program")
    print("  -h, --help:            display help")
    print()


if __name__ == "__main__":
    main(sys.argv[1:])

    # Wait for user input to close program (Windows)
    os.system("pause")
