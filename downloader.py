import imageio_ffmpeg
import moviepy.editor as mp
from pytube import Playlist, YouTube
import os

def main():
	choice = prompt_type_of_download()
	link = prompt_link()
	initial_path = prompt_path()

	if choice is "Playlist":
		folder = prompt_folder_creation(initial_path)

		path_after = create_folder(folder, initial_path)

		download_playlist(link, path_after)

		if check_conversion() is True:
			path_mp3 = create_mp3_folder(initial_path, path_after, folder)

			magic_converting(path_after, path_mp3)


# Returns 1 for playlist and 2 for video
def prompt_type_of_download():
	print("What would you like to download from youtube?")
	while True:
	    try:
	        choice = int(input("(1)Playlist (2)Video: "))
	        if choice == 1:
	        	return "Playlist"
	        elif choice == 2:
	        	return "Video"
	        raise ValueError("Invalid value")
	    except:
	        print("Has to be 1 or 2")

def prompt_link():
	while True:
		try:
			link = input("Link: ")
			if "youtube.com" in link:
				return link
			raise ValueError("Link not from youtube")
		except:
			print("The link is not from youtube")	
	
def prompt_path():
	print("\n(Usually: /home/*usr*/Downloads/)")
	while True:
		try:
			initial_path = input("Create a path where you want to save playlist/video to: ")
			if os.path.exists(initial_path):
				return initial_path
			raise ValueError("Invalid path")
		except:
			print("Path doesn't exist")

def prompt_folder_creation(initial_path):
	print("\n(Leave empty if you don't want to create a new folder)")
	folder = input("Choose a map name to save playlist to: ")
    
	return folder

# Returns path to newly created folder
def create_folder(folder, initial_path):
	if folder:
		
		# for instance "~/Downloads/Mac_Miller/"
		path_after = initial_path + folder + "/"
	    
	    # check if folder exists, create a new one if not
		if not os.path.isdir(path_after):
			os.makedirs(path_after)

		return path_after
	else:
		return initial_path

def download_playlist(link, path_after):
    yt = Playlist(link)
    print("Downloading playlist...")
    try:
        yt.download_all(download_path=path_after)
    except:
    	print("\nSome video is unavailable and crashes the script")
    	print("\n~You can either try to find a similar playlist or download one by one~\n")
    	pass

def check_conversion():
    convert =  input("Would you like to convert the folder to audio?(y/n): ")
    if str(convert.lower()) in ('y', "ye", "yes", '1'):
        return True
    else:
        return False
	

# Returns path to mp3 folder
def create_mp3_folder(initial_path, path_after, folder):
    path_mp3 = initial_path + folder + "mp3/"

    if not os.path.isdir(path_mp3):
        os.makedirs(path_mp3)

    return path_mp3



# This is a magic trick, and I mustn't tell you how it works
def magic_converting(path_after, path_mp3):
	# Creates list of files that were previously downloaded
    files = os.listdir(path_after)

    for file in files:
            clip = mp.VideoFileClip(path_after + file)
            # Since the files end with ".mp4", we remove the 4 and replace it with 3
            clip.audio.write_audiofile(path_mp3 + file[:-1] + '3')
            clip.close()



# # if video  
# if choice == 2:
#     yt = YouTube(link)
    
#     # download video to ~/Downloads
#     print("downloading video..")
#     dl_streams = yt.streams.filter(progressive=True, subtype='mp4',).order_by('resolution').desc().first().download("/home/pandazaar/Downloads/")
    
#     # ask if convert file to mp3
#     print("NOTE: if the title from youtube isn't the same as the title that was downloaded, this won't work.. though you can fix it by just editing the title")
#     convert = str(input("Would you like to convert the folder to audio only?(y/n): "))

#     if convert.lower() == "y" or convert.lower() == "yes":

#         path_mp3 = oldpath +  yt.title + ".mp3"
#         print(path_mp3)

#         clip = mp.VideoFileClip(oldpath + yt.title + ".mp4")
#         clip.audio.write_audiofile(path_mp3)
#         clip.close()


if __name__ == '__main__':
	main()

