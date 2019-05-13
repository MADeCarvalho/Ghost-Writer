import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
import os
from ffpyplayer.player import MediaPlayer
from mutagen.mp3 import MP3
from pydub import AudioSegment
from moviepy.editor import *
import math

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
    
def addAudioToMovie(final_video):
    final_video.write_videofile(os.path.join(video_folder, video_name), fps=15, audio='videos\\combined.mp3')
    final_video.close()


def moviePyVideo():
    buildAudio()
    buildBackgroundMusic()
    combineAudio("videos\\background_music.mp3","videos\\concatAudio.mp3")
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith(".mp3")]
    video_clips = []
    transition = VideoFileClip('utility\\tv_transition.mp4').set_end(0.8)  
    transition_audio = transition.audio
    transition_audio.write_audiofile('utility\\tv_transition.mp3')
    transition.close()
    for image in images:
        video_clip = ImageClip(os.path.join(image_folder, image)).set_duration(__getAudioFileLength(image))   
        video_clips.append(video_clip)
        video_clip.close()
        video_clips.append(transition)
    final_video = concatenate_videoclips(video_clips, method="compose")
    return final_video



def _getVideoLengthEarly():
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith('mp3')]   
    videoLength = 0
    for nar in narrations:
        videoLength = videoLength + AudioSegment.from_mp3(os.path.join(narrations_folder, nar)).duration_seconds
        videoLength = videoLength + AudioSegment.from_mp3("utility\\tv_transition.mp3").duration_seconds
    return videoLength

def combineAudio(music_file, voice_file):
    sound1 = AudioSegment.from_file(music_file)-14
    sound2 = AudioSegment.from_file(voice_file)
    combined = sound1.overlay(sound2)
    combined.export("videos\\combined.mp3", format='mp3')

def buildBackgroundMusic():
    background_music = AudioFileClip('utility\\jazz_lounge.mp3')
    my_clip = AudioFileClip('videos\\concatAudio.mp3')
    my_clip_duration = my_clip.reader.duration
    my_clip.close()
    quotient = math.floor(my_clip_duration / background_music.duration)
    remainder = my_clip_duration % background_music.duration
    final_file = []
    for i in range(quotient):
        final_file.append(background_music)
    background_music_remainder = background_music.set_end(my_clip_duration - (background_music.duration * quotient))
    final_file.append(background_music_remainder)
    bg_music_file = concatenate_audioclips(final_file)
    bg_music_file.write_audiofile('videos\\background_music.mp3')
    


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
    video = cv2.VideoWriter(os.path.join(video_folder, video_name), 0, 1, (1920, 1080))
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
   video = moviePyVideo()
   addAudioToMovie(video)