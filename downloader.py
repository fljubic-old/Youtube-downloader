import imageio_ffmpeg
import moviepy.editor as mp
from pytube import Playlist, YouTube
from pytube.helpers import safe_filename
import os

def main():
	choice = get_type()
	link = get_link()
	initial_path = get_path()

	if choice is "Playlist":
		folder = new_folder(initial_path)

		path_after = create_folder(initial_path, folder)

		download_playlist(link, path_after)

		if playlist_conversion() is True:
			path_after_mp3 = create_mp3_folder(initial_path, path_after, folder)

			magic_playlist_converting(path_after, path_after_mp3)
	
	elif choice is "Video":
		title = download_video(initial_path, link)

		if video_conversion() is True:
			magic_video_converting(initial_path, title)





# Prompts user for the type of download (Playlist or just 1 video)
# Returns "Playlist" or "Video"
def get_type():
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

# Prompts user for the link of playlist/video
# Returns the link
def get_link():
	while True:
		try:
			link = input("Link: ")
			if "youtube.com" in link:
				return link
			raise ValueError("Link not from youtube")
		except:
			print("The link is not from youtube")	
	
# Prompts user for the download path
# Returns the path
def get_path():
	print("\n(Usually: '/home/*usr*/Downloads/')")
	while True:
		try:
			initial_path = input("Create a path where you want to save playlist/video to: ")
			if os.path.exists(initial_path):
				return initial_path
			raise ValueError("Invalid path")
		except:
			print("Path doesn't exist")

# Prompt user to select a name for the folder that will be created, to download videos from playlist into
# Returns name of folder
def new_folder(initial_path):
	print("\n(Leave empty if you don't want to create a new folder)")
	folder = input("Choose a map name to save playlist to: ")
    
	return folder

# Creates a folder if it doesn't already exist
# Returns path to newly created folder or just the old path if no folder was created
def create_folder(initial_path, folder):
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

# Prompt user if he want's to convert the mp4 to mp3
def playlist_conversion():
    convert =  input("Would you like to convert the folder to audio?(y/n): ")
    if convert.lower() in ('y', "ye", "yes"):
        return True
    else:
        return False

# Creates a new folder that will hold all the converted files
# Returns path to new folder
def create_mp3_folder(initial_path, path_after, folder):
    path_mp3 = initial_path + folder + "mp3/"

    if not os.path.isdir(path_mp3):
        os.makedirs(path_mp3)

    return path_mp3

# Converts all mp4 videos to mp3 (into the mp3 folder)
def magic_playlist_converting(path_after, path_after_mp3):
	
	# Creates list of files that were previously downloaded
    files = os.listdir(path_after)

    # Goes file by file and converts each of them one by one
    for file in files:
    		# Location of file that will be converted
            path_mp4 = path_after + file

    		# Select the file to convert
            clip = mp.VideoFileClip(path_mp4)

            # The path looks complicated but it's actually really readable if you look at it as this:
            # It's the initial download path, but with the folder that we've just created and inside of it the
            # Name of the file that was just downloaded, just changed the ending to mp3 instead of mp4
			# (Since the files end with ".mp4", we remove the last letter (4) and replace it with 3)
            path_mp3 = path_after_mp3 + file[:-1] + '3'

			# Convert to mp3
            clip.audio.write_audiofile(path_mp3)
            
            # Close for no bugs (hopefully)
            clip.close()


# Returns the name of the file for later use
def download_video(initial_path, link):
	yt = YouTube(link)

	print("downloading video..")
	# Filters out streams which are mp4, ordered by resolution and in descending order(so that the best resolution is on top)
	# Takes the top stream and downloads it to the initial path set by the user
	dl_streams = yt.streams.filter(progressive=True, subtype='mp4',).order_by('resolution').desc().first().download(initial_path)

	return safe_filename(yt.title)

# Prompts user for mp3 conversion
def video_conversion():
	convert = input("Would you like to convert the folder to audio only?(y/n): ")

	if convert.lower() in ('y', "ye", "yes"):
		return True
	else:
		return False

# Converts video to mp3
def magic_video_converting(initial_path, title):

	# Location of file that will be converted
	path_mp4 =  initial_path + title + ".mp4"

	# Select the file to convert
	clip = mp.VideoFileClip(path_mp4)

	# This way we set the name of the new file to be the same as the old file, just as mp3 instead of mp4
	path_mp3 = initial_path +  title + ".mp3"

	# Convert it to mp3
	clip.audio.write_audiofile(path_mp3)

	# Close for no bugs (hopefully)
	clip.close()

if __name__ == '__main__':
	main()

