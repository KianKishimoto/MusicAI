from pytube import YouTube

def fetchVid(link):
    
    try:
        vid = YouTube(link)
        vid.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("media")
    except:
        print("Connection failed. Try again later.")
    print("Title: ", vid.title)
    print("Length: ", vid.length)
        
    



if __name__ == "__main__":
    print("Paste music video link below: ")
    fetchVid(input())