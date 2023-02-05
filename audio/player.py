import os
import sdl2
import sys
import audioread
import threading
from random import randint


class ReadAIFF:
    def __init__(self, filename):

        self.input_file = audioread.audio_open(os.path.realpath(filename))
        self.frameUpto = 0
        self.bytesPerFrame = self.input_file.channels * self.input_file.samplerate
        print('CHANNELS:', self.input_file.channels)
        print('SAMPLERATE', self.input_file.samplerate)
        nframes = self.input_file.samplerate * self.input_file.duration
        print('N FRAMES', nframes)
        # print('NFRAMES', self.input_file.nframes)

        self.gen = None
        self.numFrames = nframes
        # self.numFrames = self.input_file.nframes
        # self.numFrames = self.input_file.getnframes()
        self.done = threading.Event()

    def playNextChunk(self, unused, buf, bufSize):
        print('bufSize: %s' % bufSize)
        if self.gen is None:
            self.gen = self.input_file.read_data(bufSize)
        bytesWritten = 0
        try:
            data = next(self.gen)
            first = None
            for i, b in enumerate(data):
                if first is None:
                    first = True
                buf[i] = b
                bytesWritten += 1
            rest = bufSize - bytesWritten
            for i in range(bytesWritten, bufSize):
                buf[i] = 0

        except StopIteration:
            print("got stop iteration")
            self.input_file.close()
            self.done.set()

        return


class AudioPlayer(object):
    pass
    filename = None
    plyer = None
    devID = None

    def __init__(self):
        pass

    def setup(self, filename):
        print('setup with filename:%s' % filename)
        if sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO) != 0:
            raise RuntimeError('failed to init audio')

        input_file_format = sdl2.AUDIO_S16LSB
        samples = 512
        if (filename.endswith('.wav')):
            input_file_format = sdl2.AUDIO_S16
            samples = 4096

        self.plyer = ReadAIFF(filename)
        spec = sdl2.SDL_AudioSpec(
            self.plyer.input_file.samplerate,  #freq
            input_file_format,  #format
            self.plyer.input_file.channels,  #channels
            samples,  # samples
            sdl2.SDL_AudioCallback(self.plyer.playNextChunk))

        self.devID = sdl2.SDL_OpenAudioDevice(None, 0, spec, None, 0)
        print('devID', self.devID)
        if self.devID == 0:
            raise RuntimeError('failed to open audio device')

        # Tell audio device to start playing:
        # # Wait until all samples are done playing
        # # print('Got here')
        # # sdl2.SDL_Delay(5000)
        # sdl2.SDL_CloseAudioDevice(self.devID)

        # this worked
        # sdl2.SDL_PauseAudioDevice(self.devID, 1)
        # sdl2.SDL_PauseAudioDevice(self.devID, 0)
        # self.plyer.done.wait()

        # sdl2.SDL_Delay(8000)
        # sdl2.SDL_Delay(10000)
        # sdl2.SDL_CloseAudioDevice(self.devID)
        self.playAudio()

    def playAudio(self):
        if self.devID == 0:
            raise RuntimeError('failed to open audio device')
        sdl2.SDL_PauseAudioDevice(self.devID, 1)
        sdl2.SDL_PauseAudioDevice(self.devID, 0)
        self.plyer.done.wait()
        sdl2.SDL_CloseAudioDevice(self.devID)

    def pauseAudio(self):
        sdl2.SDL_PauseAudioDevice(self.devID, 1)


if __name__ == '__main__':
    fn = '/Users/peterconerly/code/spikes/treetop_01_intro.mp3'
    fn = '/Users/peterconerly/code/spikes/treetop_01_intro.wav'
    audioPlayer = AudioPlayer()
    # playAudio()
    audioPlayer.setup(fn)
    # audioPlayer.playAudio()
