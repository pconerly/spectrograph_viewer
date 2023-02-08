# -*- coding: utf-8 -*-
import os
import sys
import traceback
import ctypes
import time
import traceback

import sdl2
from sdl2 import *
import ctypes
import OpenGL.GL as gl
from functools import partial
import imgui
from imgui.integrations.sdl2 import SDL2Renderer
from setup_imgui_window import impl_pysdl2_init
from attrdict import AttrDict

from components import root_component
from state import actions, actionTypes, setup_store
from state.loadsave import saveState
from db import SirensFile, create_tables

from utils import getRightDirs

resource_dir, data_path = getRightDirs()
print('--------------------')
print('resource_dir', resource_dir)
print('data_path', data_path)

c_uint8 = ctypes.c_uint8

# state_change = True
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

start = time.time()


def print_progress():
    now = time.time()
    print("%s has elapsed" % (now - start))


class ChangeManager(object):

    def __init__(self):
        self.state_change = True

    def changed(self, ch=True):
        self.state_change = ch


def notify(store):
    store.dispatch({'type': 'INCREMENT'})


class Window_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ('SDL_WINDOW_FULLSCREEN', c_uint8, 1),  # asByte & 1
        ('SDL_WINDOW_OPENGL', c_uint8, 1),  # asByte & 2
        ('SDL_WINDOW_SHOWN', c_uint8, 1),  # asByte & 4
        ('SDL_WINDOW_HIDDEN', c_uint8, 1),  # asByte & 8
        ('SDL_WINDOW_BORDERLESS', c_uint8, 1),
        ('SDL_WINDOW_RESIZABLE', c_uint8, 1),
        ('SDL_WINDOW_MINIMIZED', c_uint8, 1),
        ('SDL_WINDOW_MAXIMIZED', c_uint8, 1),
        ('SDL_WINDOW_INPUT_GRABBED', c_uint8, 1),
        ('SDL_WINDOW_INPUT_FOCUS', c_uint8, 1),
        ('SDL_WINDOW_MOUSE_FOCUS', c_uint8, 1),
        ('SDL_WINDOW_FULLSCREEN_DESKTOP', c_uint8, 1),
        ('SDL_WINDOW_FOREIGN', c_uint8, 1),
        ('SDL_WINDOW_ALLOW_HIGHDPI', c_uint8, 1),
        ('SDL_WINDOW_MOUSE_CAPTURE', c_uint8, 1),
        ('SDL_WINDOW_ALWAYS_ON_TOP', c_uint8, 1),
        ('SDL_WINDOW_SKIP_TASKBAR', c_uint8, 1),
        ('SDL_WINDOW_UTILITY', c_uint8, 1),
        ('SDL_WINDOW_TOOLTIP', c_uint8, 1),
        ('SDL_WINDOW_POPUP_MENU', c_uint8, 1),
        ('SDL_WINDOW_VULKAN', c_uint8, 1),
    ]


class Flags(ctypes.Union):
    _anonymous_ = ("bit", )
    _fields_ = [("bit", Window_bits), ("asByte", c_uint8)]


windowFlags = Flags()


def show_window_flags(windowFlags):
    print("---- window flags")
    for field in Window_bits._fields_:
        if getattr(windowFlags, field[0]) == True:
            print('got true flag: %s' % field[0])


def main():
    cm = ChangeManager()
    create_tables()
    store = setup_store()
    store.subscribe(cm.changed)
    dispatch = store.dispatch

    window, gl_context = impl_pysdl2_init()
    imgui.create_context()
    p_note = partial(notify, store)
    renderer = SDL2Renderer(window)

    running = True
    startup = True
    window_has_focus = False
    event = SDL_Event()

    while running:
        renderThisIter = window_has_focus or startup
        if renderThisIter:
            startup = False
            pass
        else:
            # does not have focus
            print('.', end='', flush=True)
            time.sleep(0.1)  # half a second

        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                print("SDL_QUIT")
                saveState(state)
                running = False
                break

            if (event.type == SDL_KEYDOWN):
                keysym = event.key.keysym
                # 'LGUI' is 'CMD' in OSX.
                if keysym.mod == KMOD_LCTRL or keysym.mod == KMOD_LGUI:
                    if keysym.scancode == SDL_SCANCODE_N:
                        dispatch(actions.openFilepicker())

                if keysym.scancode == SDL_SCANCODE_ESCAPE:
                    dispatch(actions.closePopup())

            if event.type == SDL_WINDOWEVENT:
                windowFlags.asByte = event.window.event

                # These flags are reversed and I have no idea why.
                if windowFlags.SDL_WINDOW_SHOWN:
                    # print("got window shown")
                    window_has_focus = False
                elif windowFlags.SDL_WINDOW_HIDDEN:
                    # print("HIDDEN WINDOW")
                    window_has_focus = True
                elif windowFlags.SDL_WINDOW_INPUT_FOCUS:
                    # print("SDL_WINDOW_INPUT_FOCUS")
                    pass
                else:
                    # print("got other window event: %s" % windowFlags)
                    pass

            renderer.process_event(event)
        renderer.process_inputs()

        if renderThisIter:
            state = store.get_state()
            # supplement time?
            state.curTime = time.time()

            imgui.new_frame()

            root_component(state, dispatch)

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            imgui.render()
            renderer.render(imgui.get_draw_data())

            SDL_GL_SwapWindow(window)

    renderer.shutdown()
    SDL_GL_DeleteContext(gl_context)
    SDL_DestroyWindow(window)
    SDL_Quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error running main')
        print(e)
        traceback.print_exc()
