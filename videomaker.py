import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
import os
from ffpyplayer.player import MediaPlayer
from mutagen.mp3 import MP3
from pydub import AudioSegment
from moviepy.editor import *

image_folder = 'images'
video_folder = 'videos'
video_name = 'video.mp4'
narrations_folder = 'narrations'

def __getAudioFile(image):
    return os.path.join(narrations_folder, image.replace('png', 'mp3'))

def __getAudioFileLength(currentImage):
    currentNarration = currentImage.replace("png", "mp3")
    audio = MP3(os.path.join(narrations_folder, currentNarration))
    return audio.info.length

def buildTransition():
    width = 1280
    height = 720
    FPS = 24
    seconds = 1

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('utility\\transition.avi', fourcc, float(FPS), (width, height))

    for _ in range(FPS*seconds):
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        video.write(frame)
    video.release()

def moviePyVideo():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith(".mp3")]
    video_clips = []
    audio_clips = []
    transition = VideoFileClip('utility\\tv_transition.mp4').set_end(0.8)   
    transition_audio = transition.audio
    transition_audio.write_audiofile('utility\\tv_transition.mp3')
    for image in images:
        audio_clip = AudioFileClip(__getAudioFile(image))
        audio_clips.append(audio_clip)
        video_clip = ImageClip(os.path.join(image_folder, image)).set_duration(__getAudioFileLength(image))   
        video_clip.set_audio(audio_clip)
        video_clips.append(video_clip)
        audio_clip.close()
        video_clip.close()
        video_clips.append(transition)
        audio_clips.append(transition.audio)
    final_audio = concatenate_audioclips(audio_clips)
    final_video = concatenate_videoclips(video_clips, method="compose")
    buildAudio()
    final_video.write_videofile(os.path.join(video_folder, video_name), fps=15, audio=os.path.join(video_folder, 'concatAudio.mp3'))


def buildAudio():
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith('mp3')]
    concat_audio = AudioSegment.silent(duration=10)
    transition_audio = AudioSegment.from_mp3('utility\\tv_transition.mp3')
    for narr in narrations:
        concat_audio = concat_audio + AudioSegment.from_mp3(os.path.join(narrations_folder, narr))
        concat_audio = concat_audio + transition_audio
    concat_audio.export(os.path.join(video_folder, 'concatAudio.mp3'), format="mp3")

def buildVideo():
    #buildTransition()
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith(".mp3")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(os.path.join(video_folder, video_name), 0, 1, (1280, 720))
    concatAudio = AudioSegment.silent(duration=100)
    for image in images:
        audioLength = round(__getAudioFileLength(image))        
        for i in range(0, audioLength):
            try:
                b = cv2.imread(os.path.join(image_folder, image))
                video.write(b)
            except Exception as e:
                print("gotcha")
                print(e)
        concatAudio = concatAudio + AudioSegment.from_mp3(os.path.join(narrations_folder, image.replace('png', 'mp3')))
    concatAudio.export(os.path.join(video_folder, 'concatAudio.mp3'), format="mp3")
    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    moviePyVideo()