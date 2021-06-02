from os import path
import imgui
from state import actionTypes, actions, thunks

kFile = 'File'
kDir = 'Directory'


def file_browser_popup(state, dispatch):

    if state.filePickingFires:
        imgui.open_popup("File Picker")
        dispatch(actions.filePickingFired())

    imgui.set_next_window_size(500, 500)
    if imgui.begin_popup_modal(
            "File Picker", True, flags=imgui.WINDOW_NO_COLLAPSE)[0]:

        imgui.separator()
        imgui.push_item_width(280)
        imgui.text('Directory:')

        text_val = state.tmpDir
        changed, text_val = imgui.input_text('', text_val, 500)
        if changed:
            if path.isdir(text_val):
                dispatch(actions.updateTmpDir(text_val))

        if False:
            imgui.text('You wrote:')
            imgui.same_line()
            imgui.text(text_val)
            imgui.pop_item_width()

            imgui.text('Validated cur dur:')
            imgui.same_line()
            imgui.text(state.curDir)

        # columns
        imgui.separator()

        up_dir = [
            ('..', kDir),
        ]
        tempDirs = list(zip(state.tmpDirs, [kDir] * len(state.tmpDirs)))
        tempFiles = list(zip(state.tmpFiles, [kFile] * len(state.tmpFiles)))
        master_list = up_dir + tempDirs + tempFiles

        imgui.begin_group()
        imgui.text("Filename")
        f_output = write_column_files(master_list, [])
        imgui.end_group()

        imgui.same_line()

        imgui.begin_group()
        imgui.text('FileType')
        write_column_filetype(master_list)

        imgui.end_group()

        imgui.separator()

        for index, pick in enumerate(f_output):
            if pick[1] and imgui.is_mouse_double_clicked(0):

                target = master_list[index]
                if target[1] == kDir:
                    newDir = path.abspath(path.join(state.tmpDir, target[0]))
                    dispatch(actions.updateTmpDir(newDir))
                else:
                    imgui.close_current_popup()
                    dispatch(
                        actions.loadFile(
                            path.abspath(path.join(state.tmpDir, target[0]))))

        if state.closePopupFires:
            imgui.close_current_popup()
            dispatch(actions.clearClosePopup())

        imgui.end_popup()


def write_column_files(files, f_output=[]):
    for f in files:
        fpick = imgui.selectable(f[0], False,
                                 imgui.SELECTABLE_ALLOW_DOUBLE_CLICK
                                 | imgui.SELECTABLE_DONT_CLOSE_POPUPS)
        #   imgui.SELECTABLE_SPAN_ALL_COLUMNS
        f_output.append(fpick)
    return f_output


def write_column_filetype(files):
    for f in files:
        imgui.text(f[1])

    return
