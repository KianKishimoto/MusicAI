from pytube import YouTube
from tqdm import tqdm
import moviepy
import moviepy.video.fx.all as vfx
from moviepy.editor import *
from collections.abc import MutableSequence
from madmom import *

def column(matrix, i):
    return [row[i] for row in matrix]

def fetchVid(link):
    try:
        vid = YouTube(link)
        print("Title: ", vid.title)
        print("Length: ", vid.length)
        vid.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="media",filename="video.mp4")
    except:
        print("Connection failed. Try again later.")
    
def fetchAudio(link):
    print("Converting mp3...")
    vid = YouTube(link)
    print("Title: ", vid.title)
    print("Length: ", vid.length)
    vid.streams.filter(only_audio=True).first().download(output_path="media/input",filename="audio.mp3")
    
    
def convertVid():
    video = VideoFileClip(os.path.join("media/video.mp4"))
    video.audio.write_audiofile(os.path.join("media/audio.mp3"))
    #audio.close()
    #video.close()

def beatTrack(directory):
    print("Beat tracking...")
    #Input: path to audio file
    #Output: array of beat times
    #This method will read in the audio file and return an array of beat times using madmom

    #processor = features.beats.DBNBeatTrackingProcessor(fps=100)
    downProcessor = features.downbeats.DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
    #act = features.beats.RNNBeatProcessor()(directory)
    downAct = features.downbeats.RNNDownBeatProcessor()(directory)
    #beats = processor(act)
    downBeats = downProcessor(downAct)
    beats = column(downBeats, 0)
    return beats #.tolist()

def beatMatch(beatVideo, beatInput, inputVideo, inputAudio):
    #Input: array of beat times for video, array of beat times for input
    #Output: array of beat times for input, scaled and shifted to match video
    #This method will take in the beat times for the video and the input and return the beat times for the input, scaled and shifted to match the video
    
    #Example Input beat1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] #Video (get modified)
    #Example Input beat2 = [4, 6, 7, 9, 10, 12, 13, 15, 16, 18]
    
    #loop over the min(len(beat1), len(beat2)) and find the best match

    #0-1 --> 4-6 so ==> Strech = 1/2, Shift = 4
    #1-2 --> 6-7 so ==> Strech = 1, Shift = 5
    tempDiffVideo = 0
    tempDiffInput = 0
    beatScale = []
    #beatShift = []
    clips = []
    index = min(len(beatVideo), len(beatInput))
    for i in tqdm(range(0, index-1)):
        if (i != 0):
            tempDiffVideo = beatVideo[i] - beatVideo[i-1]
            tempDiffInput = beatInput[i] - beatInput[i-1]
            beatScale.append(tempDiffVideo/tempDiffInput)
        #beatShift.append(beatInput[num] - x)
    
    for i in tqdm(range(0, index-1)):
        video = VideoFileClip(inputVideo)
        if (i < index-2):
            clip = video.subclip(beatVideo[i], beatVideo[i+1])
            vfx.speedx(clip,beatScale[i])
            clips.append(clip)
    tempVideo = concatenate_videoclips(clips)
    tempVideo.write_videofile(os.path.join("media/FinalVideo_NOAUDIO.mp4"), fps=24, codec='libx264', audio=False)
    music = AudioFileClip(inputAudio)
    music1 = CompositeAudioClip([music])
    finalVideo = VideoFileClip(os.path.join("media/FinalVideo_NOAUDIO.mp4"))
    finalVideo.audio = music1
    finalVideo.write_videofile(os.path.join("media/FinalVideo1.mp4"))
    

# def flashBeat(beats, directory):
#     #Input: numpy array of beat times and path to audio file
#     #Output: mp4 video with flashing lights to the beat
#     #This method will take in the beat times and audio file and create a video with flashing lights to the beat

#     #Create a video clip with the audio file
#     video = VideoFileClip(directory)

#     #iterate over the beats array and create a list of clips with the lights flashing
#     clips = []
#     for i in range(len(beats)-1):
#         clip = video.subclip(beats[i], beats[i]+0.1)
#         clips.append(vfx.rotate(clip, 180))
    
#     #Concatenate the clips together
#     final_clip = concatenate_videoclips(clips)
#     #save to media/output.mp4
#     final_clip.write_videofile(os.path.join("media/output.mp4"), fps=24, codec='libx264')


if __name__ == "__main__":
    print("Paste music video link below: ")
    fetchVid(input()) 
    print("Paste audio song link below: ")
    fetchAudio(input())
    convertVid()
    beatVideo = beatTrack("media/audio.mp3")
    beatInput = beatTrack("media/input/audio.mp3")
    #print(beatVideo)
    #print(beatInput)
    beatMatch(beatVideo, beatInput, "media/video.mp4","media/input/audio.mp3")


    #flashBeat(beatVideo, "media/video.mp4")

