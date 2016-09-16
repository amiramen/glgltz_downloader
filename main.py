# Require youtube-dl package

import requests
import re
import os
import sys

SONG_NAME_INDEX = 0
ARTIST_NAME_INDEX = 1
YOUTUBE_URL_INDEX = 2

OUTPUT_DIR = u".\\songs"
TEMP_FILENAME = u"in_progress"
TEMP_FILENAME_BEFORE_FFMPEG_EXTENTION = '.webm'
TEMP_FILENAME_AFTER_FFMPEG_EXTENTION = '.mp3'
FINAL_FILENAME_PATTERN = u"{song_name} - {artist_name}.mp3"

url = "http://glglz.co.il/1213-he/Galgalatz.aspx" # Heb playlist 
#url = "http://glglz.co.il/1215-he/Galgalatz.aspx" # Eng Playlist
DOWNLOAD_MP3_FROM_YOUTUBE_UTL_COMMAND_FORMAT = "youtube-dl --audio-format \"mp3\" -x {youtube_url} -o \"{filename}\"" # % yotube url


def delete_temp_file_if_exists(file_path):
	if os.path.exists(file_path):
		print "Temp song file deleted: {temp_file_path}".format(temp_file_path=temp_file_path)
		os.remove(temp_file_path)

print "Get urls page...",
urls_page = requests.get(url)
print "Done!"

print "Search for songs... ",
artist_and_song_name_regex = '<td><span>(.+?)</span>.+\s+<td><span>(.+?)</span>.+\s+<td>.*</td>\s+.*?"(.+?)"'
song_details = re.findall(artist_and_song_name_regex, urls_page.text)

print "{number_of_songs_found} songs found.".format(number_of_songs_found=len(song_details))

# Delete temp song file
temp_file_path_before_ffmpeg = os.path.join(OUTPUT_DIR, TEMP_FILENAME + TEMP_FILENAME_BEFORE_FFMPEG_EXTENTION)
temp_file_path_after_ffmpeg = os.path.join(OUTPUT_DIR, TEMP_FILENAME + TEMP_FILENAME_AFTER_FFMPEG_EXTENTION)

# Clean temp files leftovers
delete_temp_file_if_exists(temp_file_path_before_ffmpeg)
delete_temp_file_if_exists(temp_file_path_after_ffmpeg)

# Download songs loop
for i in range(len(song_details)):
	
	# Set song details
	song_name = unicode(song_details[i][SONG_NAME_INDEX])
	artist_name = unicode(song_details[i][ARTIST_NAME_INDEX])
	youtube_url = song_details[i][YOUTUBE_URL_INDEX]
	finall_file_path = os.path.join(OUTPUT_DIR,FINAL_FILENAME_PATTERN.format(song_name=song_name, artist_name=artist_name))
	
	print "\n~~~~ Downloading Song #{song_num}: {youtube_url} ~~~~".format(song_num=i+1, youtube_url=youtube_url)
	
	# Check if song already downloaded
	if not os.path.exists(finall_file_path):
		
		# Download youtube link to temp_file_path_before_ffmpeg (because youtube-dl not support unicode chars)
		# Note: the command uses ffmpeg.exe that changes the output filenmae from temp_file_path_before_ffmpeg to temp_file_path_after_ffmpeg
		os.system(DOWNLOAD_MP3_FROM_YOUTUBE_UTL_COMMAND_FORMAT.format(youtube_url=youtube_url, filename=temp_file_path_before_ffmpeg))
		
		# Rename to the original song name
		os.rename(temp_file_path_after_ffmpeg, finall_file_path)
	
	else:
		print u"Song already exists."
	