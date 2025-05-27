# ConvertAudioFiles

Simple script to bulk convert all audio files in a specified directory to MP3 or WAV files.
(For Windows / Linux, requires VLC)

Usage:

Windows:

```Windows
python ConvertAudioFiles.py -d <directory>
```

Linux:

```Linux
python3 ConvertAudioFiles.py -d <directory>
```

> Options:
>
> * *-d, --dir \<dir\>*:                directory to bulk convert audio files in
> * *-o, --output-format \<format\>*:    output format (mp3 or wav)"
> * *-r, --rate \<rate\>*:               bit rate (mp3 format only)
> * *-p, --program \<path\>*:            path to VLC program
> * *-h, --help*:                        display help
