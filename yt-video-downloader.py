from pytube import YouTube
print("***AD FREE OPPAI DOWNLOADER***")
print() # for space
print("HENTAI KING")
print() #for space

link = input("enter link of video: ")
videoLink = YouTube(link)
videoL = videoLink.streams.filter(file_extension="mp4") 

video720 = videoL.filter(res="720p")
video480 = videoL.filter(res="480p")
video360 = videoL.filter(res="360p") 

print(f"Title: {videoLink.title}")

print()  

if len(video720) > 0:
   print(f"1. Video Resolution: 720p | Video Size: {video720[0].filesize/(1024*1024)}MB")
else:
   print("Resolution 720p not available")
   
print() #for spacing
if len(video480) > 0:
   print(f"2. Video Resolution: 480p | Video Size:{video480[0].filesize/(1024*1024)}MB")
else:
    print("Resolution 480p not available")
    
print()  #for space

if len(video360) > 0:
   print(f"3. Video Resolution: 360p | Video Size: {video360[0].filesize/(1024*1024)}MB")
else:
    print("Resolution 360p not available")
print() 

choosen = int(input("Enter Oppai number of the video: "))

if choosen == 1:
    print("downloading.....")
    video720[0].download("/data/data/com.termux/files/home/storage/downloads")
    print("downloaded successfully:3")

if choosen == 2:
    print("downloading.....")
    video480[0].download("/data/data/com.termux/files/home/storage/downloads")
    print("downloaded successfully:3")
if choosen == 3:
    print("downloading.....")
    video360[0].download("/data/data/com.termux/files/home/storage/downloads")
    print("downloaded successfully:3")



