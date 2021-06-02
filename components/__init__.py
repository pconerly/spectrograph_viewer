import sys
import OpenGL.GL as gl
import imgui

from .file_browser import file_browser_popup
from .file_viewer import file_viewer
from .sirens_files_list import sirens_files_list
from .sirenfile_popup import sirenfile_popup
from state import actionTypes, actions
from state.loadsave import saveState


def root_component(state, dispatch):  #imgui, gl):
    '''
        usage:
        state = store.get_state()
        imgui.new_frame()

        root_component(state)

        imgui.render()

        SDL_GL_SwapWindow(window)
    '''

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_new, selected_new = imgui.menu_item(
                'New', 'Cmd+N', False, True)

            if clicked_new:
                dispatch(actions.openFilepicker())

            click_sirensfiles, selected_new = imgui.menu_item(
                'Show Analyzed Files', None, state.showSirensFiles, True)

            if click_sirensfiles:
                dispatch(actions.setShowSirensFiles(not state.showSirensFiles))

            click_testwindow, selected_new = imgui.menu_item(
                'Show Imgui Test Window', None, state.showTestWindow, True)

            if click_testwindow:
                dispatch(actions.showTestWindow(not state.showTestWindow))

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", 'Cmd+Q', False, True)

            if clicked_quit:
                saveState(state)
                sys.exit(1)

            imgui.end_menu()
        imgui.end_main_menu_bar()

    if state.showTestWindow:
        imgui.show_test_window()

    file_browser_popup(state, dispatch)
    file_viewer(state, dispatch)

    sirens_files_list(state, dispatch)
    sirenfile_popup(state, dispatch)

    # gl.glClearColor(1., 1., 1., 1)
    # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
