import time
import imgui
from state import actionTypes, actions
from utils import pluck


def sirens_files_list(state, dispatch):
    if state.showSirensFiles and state.sirenfiles:

        imgui.set_next_window_size(520, 950)
        imgui.set_next_window_position(710, 20)

        beginResult = imgui.begin("Loaded Files in Database",
                                  closable=True,
                                  flags=imgui.WINDOW_NO_RESIZE
                                  | imgui.WINDOW_NO_MOVE
                                  | imgui.WINDOW_NO_COLLAPSE)
        if beginResult:
            (beginExpanded, beginOpened) = beginResult
            if not beginOpened:
                dispatch(actions.setShowSirensFiles(False))

            imgui.text('Analyzed files in the Database:')
            imgui.separator()

            imgui.begin_group()
            imgui.text("Id")
            imgui.separator()
            f_output = write_column_master(state.sirenfiles, 'id', f_output=[])
            imgui.end_group()
            imgui.same_line()

            imgui.begin_group()
            imgui.text("Filename")
            imgui.separator()
            write_column(state.sirenfiles, 'filename')
            imgui.end_group()
            imgui.same_line()

            imgui.begin_group()
            imgui.text('Last Updated')
            imgui.separator()
            write_datetime_column(state.sirenfiles, 'last_updated')
            imgui.end_group()

            imgui.separator()

            imgui.end()

            for index, pick in enumerate(f_output):
                if pick[1]:
                    target = state.sirenfiles[index]
                    print('picked item:', target)
                    dispatch(actions.sirenfilePopupFires(index))


def write_column_master(files, attr, f_output=[]):
    for f in files:
        fpick = imgui.selectable("%s" % getattr(f, attr), False)
        f_output.append(fpick)
    return f_output


def write_datetime_column(files, attr):
    for f in files:
        dt = getattr(f, attr)
        if dt is None:
            imgui.text('None')
        else:
            imgui.text(dt.strftime("%m-%d-%y - %H:%M:%S"))

    return


def write_column(files, attr):
    for f in files:
        imgui.text(getattr(f, attr))

    return
