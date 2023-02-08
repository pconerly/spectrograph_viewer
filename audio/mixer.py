import os
import sdl2
from sdl2 import SDL_Init, SDL_Quit, rwops, version

print('version.SDL_COMPILEDVERSION', version.SDL_COMPILEDVERSION)

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


class AudioMixer(object):
    pass
    filename = None
    plyer = None
    devID = None

    def setup(self, filename):
        if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
            raise RuntimeError('failed to init audio')

        self.filename = filename
        print('self.filename', self.filename)
        self.input_file = audioread.audio_open(os.path.realpath(self.filename))
        samplerate = self.input_file.samplerate
        channels = self.input_file.channels
        self.input_file.close()

        # SDL_INIT_AUDIO
        sdlmixer.Mix_Init(sdlmixer.MIX_INIT_MP3)
        sdlmixer.Mix_OpenAudio(samplerate, sdl2.AUDIO_S16LSB, channels, 512)

        music = sdlmixer.Mix_LoadMUS(self.filename)
        if (music == None):
            return -1

        playresult = sdlmixer.Mix_PlayMusic(music, -1)
        print("playresult", playresult)
        # if ( Mix_PlayMusic( music, -1) == -1 )
        # 	return -1;

    def playAudio(self):
        pass

    def pauseAudio(self):
        pass


if __name__ == '__main__':
    fn = '/Users/peterconerly/code/sirens/treetop_01_intro.mp3'
    am = AudioMixer()
    am.setup(fn)