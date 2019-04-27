import cv2
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

def moviePyVideo():
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith(".mp3")]
    video_clips = []
    audio_clips = []
    for image in images:
        audio_clip = AudioFileClip(__getAudioFile(image))
        audio_clips.append(audio_clip)
        video_clip = ImageClip(os.path.join(image_folder, image)).set_duration(__getAudioFileLength(image))   
        video_clip.set_audio(audio_clip)
        video_clips.append(video_clip)
        audio_clip.close()
        video_clip.close()
    final_audio = concatenate_audioclips(audio_clips)
    final_video = concatenate_videoclips(video_clips, method="compose")
    buildAudio()
    final_video.write_videofile(os.path.join(video_folder, video_name), fps=24, audio=os.path.join(video_folder, 'concatAudio.mp3'))

def buildAudio():
    narrations = [nar for nar in os.listdir(narrations_folder) if nar.endswith('mp3')]
    concat_audio = AudioSegment.silent(duration=10)
    for narr in narrations:
        concat_audio = concat_audio + AudioSegment.from_mp3(os.path.join(narrations_folder, narr))
    concat_audio.export(os.path.join(video_folder, 'concatAudio.mp3'), format="mp3")

def buildVideo():
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