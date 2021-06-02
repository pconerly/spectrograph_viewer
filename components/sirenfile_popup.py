from os import path
import imgui
from state import actionTypes, actions, thunks


def sirenfile_popup(state, dispatch):

    if state.sirenPopupFires:
        imgui.open_popup("File info")
        # state.filePickingFires = False
        dispatch(actions.sirenfilePopupFired())

    imgui.set_next_window_size(500, 500)
    if imgui.begin_popup_modal(
            "File info", True, flags=imgui.WINDOW_NO_COLLAPSE)[0]:

        imgui.separator()

        target = state.sirenfiles[state.sirenPopupIndex]
        imgui.text('File: %s' % target.filename)
        imgui.text('Full path: %s' % target.filepath)
        imgui.text('Status: %s' % target.status)
        imgui.text('Last updated: %s' % target.last_updated)

        openBtn = imgui.button('Open file')
        imgui.same_line()
        deleteBtn = imgui.button('Delete')

        if openBtn:
            dispatch(actions.loadFile(target.filepath))
            imgui.close_current_popup()

        if deleteBtn:
            dispatch(actions.deleteSirenfile(target.id))
            imgui.close_current_popup()

        if state.closePopupFires:
            imgui.close_current_popup()
            dispatch(actions.clearClosePopup())

        imgui.end_popup()
