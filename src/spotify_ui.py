import time
import logging
import argparse
import pygame
import pygame.freetype  # Import the freetype module.
import os
import sys
import numpy as np
import subprocess
import signal
import requests
import io
import pyaudio
import struct
import numpy as np
import time
import sys
import spotipy2
import datetime
from PIL import Image
from spotipy2.oauth import SpotifyOAuth

import spotify_lib

# This is the important bit
def refresh(lcd):
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
    f = open("/dev/fb1","wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth
    # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
    # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.convert(16,0).get_buffer())
    # We can then close our access to the framebuffer
    f.close()
    time.sleep(0.1)

def format_min_sec(miliseconds):
    hours, remainer = divmod(miliseconds//1000, 60*60)
    minutes, seconds = divmod(remainer, 60)

    return ('0' if minutes < 10 else '') + str(minutes) + ':' + ('0' if seconds < 10 else '') + str(seconds)

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.float32)
    # print(audio_data)
    # fft_data = np.fft.fft(audio_data)
    # fft_freq = np.fft.fftfreq(len(fft_data))
    print(audio_data)
    callback_output.append(
        audio_data
    )
    return None, pyaudio.paContinue

if __name__ == "__main__":
    SCREEN_SIZE = (320, 240)
    COLOR_WHITE = (255, 255, 255)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)

    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)

    screen = pygame.Surface(SCREEN_SIZE)

    root = os.path.dirname(os.path.abspath(__file__))
    whitrabt_14 = pygame.font.Font(root + '/../assets/fonts/whitrabt.ttf', 14)
    whitrabt_20 = pygame.font.Font(root + '/../assets/fonts/whitrabt.ttf', 20)
    oblivious_70 = pygame.font.Font(root + '/../assets/fonts/ObliviousFont.ttf', 70)

    # audio = pyaudio.PyAudio()
    # numDevices = audio.get_device_count()

    # for id in range(numDevices):  # Get inputs
    #     info = audio.get_device_info_by_index(id).get('hostApi')
    #     api = audio.get_host_api_info_by_index(info).get('name')
    #     name = audio.get_device_info_by_index(id).get('name')

    # stream = audio.open(
    #         input_device_index=0,
    #         format=pyaudio.paInt16,
    #         channels=2,
    #         rate=44100,
    #         output=False,
    #         input=True
    #         # ,stream_callback=callback
    #         )

    # while True:
    #     while stream.get_read_available():
    #         data = stream.read(1, exception_on_overflow=False)
    #         if not split:
    #             dataArr[i] = (sum(struct.unpack("2h", data)) // 2)
    #         else:
    #             dataArr[i] = (sum(struct.unpack("2h", data)[:1]))   # Left
    #             dataArr2[i] = (sum(struct.unpack("2h", data)[1:]))  # Right

    # stream.start_stream()

    # stream.close()
    # audio.terminate()

    spotify = spotipy.Spotify(auth='BQB5Nh036qwDFHQiLVbe-7pURzb_it_wYpHFtwpSZyVRz-OQpEeaEEp1yKKmgmZcCrs595g53Us8I7_CERZ29TkaBHM6JasvFZ68fDEVgFvV8Bn7BsV_x_9PP_cV6SsscxUDqGCu53f_eHV4h9lhEL4C')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        track = spotify.current_user_playing_track()

        if (track is not None):
            artist = track['item']['artists'][0]['name']
            image = track['item']['album']['images'][-1]
            name = track['item']['name']
            is_playing = bool(track['is_playing'])
            elapsed_ms = int(track['progress_ms'])
            total_ms = int(track['item']['duration_ms'])

            response = requests.get(image['url'])
            albom_cover_image = Image.open(io.BytesIO(response.content)).convert("RGBA")
            albom_cover_pyimage = pygame.image.fromstring(albom_cover_image.tobytes(), albom_cover_image.size, albom_cover_image.mode)

            now_playing_text = whitrabt_20.render("Now playing...", True, COLOR_WHITE)
            artist_name_text = whitrabt_20.render(artist, True, COLOR_WHITE)
            track_name_text = whitrabt_14.render(name, True, COLOR_WHITE)
            status_text = whitrabt_14.render('Playing' if is_playing else 'Stopped', True, COLOR_GREEN if is_playing else COLOR_RED)

            total_time_text = whitrabt_14.render(format_min_sec(total_ms), True, COLOR_WHITE)
            elapsed_time_text = whitrabt_14.render(format_min_sec(elapsed_ms), True, COLOR_WHITE)
            
            screen.blit(artist_name_text, (100, 20))
            screen.blit(track_name_text, (100, 40))
            screen.blit(status_text, (100, 60))
            screen.blit(albom_cover_pyimage, (20, 20))

            screen.blit(elapsed_time_text, (20, 186))
            screen.blit(total_time_text, (260, 186))

            progress = float(elapsed_ms/total_ms)
            pygame.draw.rect(screen, [255, 255, 255], [20, 200, 280, 10], 0)
            pygame.draw.rect(screen, [0, 0, 0], [21, 201, 278*progress, 8], 0)
        else:
            time.sleep(5)

        refresh(screen)

        time.sleep(1)

    pygame.quit()
