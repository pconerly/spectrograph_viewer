import os
import sdl2
from sdl2 import SDL_Init, SDL_Quit, rwops, version
from typing import List

print('version.SDL_COMPILEDVERSION', version.SDL_COMPILEDVERSION)

import numpy as np
import sys
import audioread
import threading
from random import randint

try:
    from sdl2 import sdlmixer
    _HASSDLMIXER = True
except:
    _HASSDLMIXER = False
print('_HASSDLMIXER', _HASSDLMIXER)

# SDL_QueueAudio


class AudioQueuer(object):
    pass
    filename = None
    plyer = None
    devID = None
    datas: List[int] = []
    done: threading.Event
    gen = None
    verbose = True
    bufferSize = 2048

    def setup(self, filename: str):
        if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
            raise RuntimeError('failed to init audio')

        self.datas = []
        self.done = threading.Event()
        self.filename = filename
        if self.verbose:
            print('self.filename', self.filename)
        self.input_file = audioread.audio_open(os.path.realpath(self.filename))

        if self.verbose:
            print('duration', self.input_file.duration)
            nframes = self.input_file.samplerate * self.input_file.duration

            print('frames', nframes)

        spec = sdl2.SDL_AudioSpec(self.input_file.samplerate,
                                  sdl2.AUDIO_S16LSB, self.input_file.channels,
                                  512)

        self.devID = sdl2.SDL_OpenAudioDevice(None, 0, spec, None, 0)
        self.gen = self.input_file.read_data(self.bufferSize)

        try:
            while True:
                data = next(self.gen)
                self.datas.append(data)
                sdl2.SDL_QueueAudio(self.devID, data, self.bufferSize)

        except StopIteration:
            if self.verbose:
                print("got stop iteration")
            self.input_file.close()
            self.done.set()

    def playAudio(self):
        if self.verbose:
            print('play audio')
        pass
        sdl2.SDL_PauseAudioDevice(self.devID, 1)
        sdl2.SDL_PauseAudioDevice(self.devID, 0)

    def pauseAudio(self):
        if self.verbose:
            print('pause audio')
        pass
        sdl2.SDL_PauseAudioDevice(self.devID, 1)

    def rewind(self):
        self.seekToFrame(0)

    def seekToTime(self, t):
        frame = int(t * self.input_file.samplerate / self.bufferSize) * 4
        self.seekToFrame(frame)

    def seekToFrame(self, frame):
        sdl2.SDL_ClearQueuedAudio(self.devID)

        # pos is frame
        for i in range(frame, len(self.datas)):
            sdl2.SDL_QueueAudio(self.devID, self.datas[i], self.bufferSize)


if __name__ == '__main__':
    fn = '/Users/peterconerly/code/sirens/treetop_01_intro.mp3'
    aq = AudioQueuer()
    aq.setup(fn)
    aq.done.wait()

    # play for 4
    aq.playAudio()
    sdl2.SDL_Delay(4000)

    # pause for 2
    aq.pauseAudio()
    sdl2.SDL_Delay(2000)

    # finish
    aq.playAudio()
    sdl2.SDL_Delay(6000)
