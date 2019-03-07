import imageio_ffmpeg
import moviepy.editor as mp
from pytube import Playlist, YouTube
import os


# ask for whether its playlist or youtube
print("What would you like to download from youtube?")
while True:
    try:
        choice = int(input("(1)Playlist (2)Video: "))
        return True
    except:
        print("Has to be 1 or 2")


link = str(input("Link: "))
print()

print("Default: /home/usr/Downloads/")
oldpath = str(input("Create a path where you want to save playlist/video to: "))
if oldpath == "":
    oldpath = "/home/pandazaar/Downloads/"


# if playlist, download playlist
if choice == 1:

    folder = str(input("Create a map to save to: "))
    
    # for instance "~/Downloads/Mac_Miller
    path = oldpath + folder + "/"

    # check if folder exists, create a new one if not
    if not os.path.isdir(path):
        os.makedirs(path)

    # download mp4 playlist
    yt = Playlist(link)
    print("downloading playlist..")
    yt.download_all(download_path=path)

    # ask if convert folder to mp3
    convert = str(input("Would you like to convert the folder to audio?(y/n): "))
   
    # magically does the converting
    if convert.lower() == "y" or convert.lower() == "yes":
        
        print("converting")
        # list of files
        files = os.listdir(path)
        
        # create new folder for mp3 files
        mp3folder = folder + "mp3"
        
        # save the path to the new folder
        mp3path = oldpath + mp3folder + "/"

        if not os.path.isdir(mp3path):
            os.makedirs(mp3path)
        mp3files = os.listdir(mp3path)

        for file in files:
            clip = mp.VideoFileClip(path + file)
            clip.audio.write_audiofile(mp3path + file[:-1] + '3')
            clip.close()

# if video  
if choice == 2:
    yt = YouTube(link)
    
    # download video to ~/Downloads
    print("downloading video..")
    dl_streams = yt.streams.filter(progressive=True, subtype='mp4',).order_by('resolution').desc().first().download("/home/pandazaar/Downloads/")
    
    # ask if convert file to mp3
    print("NOTE: if the title from youtube isn't the same as the title that was downloaded, this won't work.. though you can fix it by just editing the title")
    convert = str(input("Would you like to convert the folder to audio only?(y/n): "))

    if convert.lower() == "y" or convert.lower() == "yes":

        mp3path = oldpath +  yt.title + ".mp3"
        print(mp3path)

        clip = mp.VideoFileClip(oldpath + yt.title + ".mp4")
        clip.audio.write_audiofile(mp3path)
        clip.close()


if __name__ == '__main__':
	main()

