# Require youtube-dl package

import requests
import re
import os
import sys
#url = "http://glglz.co.il/1213-he/Galgalatz.aspx" # Heb playlist 
url = "http://glglz.co.il/1215-he/Galgalatz.aspx" # Eng Playlist
download_youtube_mp3_cmd_format = "youtube-dl --audio-format \"mp3\" -x {youtube_url}"# -o \"{filename}\"" # % yotube url

OUTPUT_DIR = u".\\songs"
TEMP_FILENAME = u"in_progress.mp3"
FINAL_FILENAME_PATTERN = u"{song_name} - {artist_name}.mp3"

print "Get urls page...",
urls_page = requests.get(url)
print "Done!"

youtube_url_regex = "(?:https?:\/\/)?(?:youtu\.be\/|(?:www\.)?youtube\.com\/watch(?:\.php)?\?.*v=)[a-zA-Z0-9\-_]+"
youtube_urls = re.findall(youtube_url_regex, urls_page.text)

artist_and_song_name_regex = "<td><span>(.+?)</span>"
artist_and_song_names = re.findall(artist_and_song_name_regex, urls_page.text)


temp_file_path = os.path.join(OUTPUT_DIR, TEMP_FILENAME)
if os.path.exists(temp_file_path):
	os.remove(temp_file_path)

for i in range(len(youtube_urls)):
	song_name = unicode(artist_and_song_names[i*2])
	artist_name = unicode(artist_and_song_names[i*2+1])
	finall_file_path = os.path.join(OUTPUT_DIR,FINAL_FILENAME_PATTERN.format(song_name=song_name, artist_name=artist_name))
	if not os.path.exists(finall_file_path):
		os.system(download_youtube_mp3_cmd_format.format(youtube_url=youtube_urls[i], filename=temp_file_path))
#		os.rename(temp_file_path, finall_file_path)
	else:
		print u"file exists."
	