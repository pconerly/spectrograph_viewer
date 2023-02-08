import time
import imgui
from state import actionTypes, actions, AudioState
from gl_modern import Wrapper  #, getFBOforSpectograph
from utils import pluck

wrap = Wrapper()

xPosStart = 15


class ClickTracker(object):
    down = 0

    def clicked(self, newDown):
        if newDown and self.down == 0:
            self.down = newDown
            return True
        self.down = newDown
        return False


clickTracker = ClickTracker()


def file_viewer(state, dispatch):
    if state.filename is not None:
        imgui.set_next_window_size(700, 950)
        imgui.set_next_window_position(5, 20)
        beginResult = imgui.begin("File Viewer",
                                  closable=True,
                                  flags=imgui.WINDOW_NO_RESIZE
                                  | imgui.WINDOW_NO_MOVE
                                  | imgui.WINDOW_NO_COLLAPSE)
        if beginResult:
            (beginExpanded, beginOpened) = beginResult
            if not beginOpened:
                dispatch(actions.closeFileViewer())

            # file info
            imgui.text('Current file: %s' % state.filename)

            if state.file.spectograph is not None:
                imgui.text('spectograph size: %s' %
                           state.file.spectograph.size)
            if state.file.data is not None:
                imgui.text('f_mels: %s' % state.file.data['f_mels'])

                data = state.file.data
                for k in data.keys():
                    imgui.bullet()
                    if k in [
                            'n_mels', 'f_mels', 'hop_l', 'sr', 'x_length',
                            'y_length', 'duration'
                    ]:
                        imgui.text('%s: %s' % (k, data[k]))
                    else:
                        imgui.text(k)

            # audio controls
            imgui.separator()
            playPauseBtn = imgui.button('Play/Pause')
            imgui.same_line()
            stopBtn = imgui.button('Stop')
            if playPauseBtn:
                print('Play/Pause')
                dispatch(actions.playPauseAudio())
            if stopBtn:
                print("Stop")
                dispatch(actions.stopAudio())

            diffTime = state.localStartTime

            (sr, hop_l, duration, x_length,
             y_length) = pluck(state.file.data, 'sr', 'hop_l', 'duration',
                               'x_length', 'y_length')

            audioStateText = '\t %s' % state.audioState.name
            if state.audioState == AudioState.Playing:
                diffTime = state.curTime - state.universalStartTime + state.localStartTime

                audioStateText = '\t %s %.2f' % (state.audioState.name,
                                                 diffTime)

                if diffTime > duration:
                    dispatch(actions.stopAudio())

            drawline = diffTime * (sr / hop_l)
            imgui.same_line()
            imgui.text(audioStateText)

            imgui.separator()
            imgui.text('Viewport position')
            imgui.push_item_width(wrap.viewportSize)

            # max_value is slightly less than the duration
            max_slider = duration - (wrap.viewportSize / (sr / hop_l))

            spectoSlider = imgui.slider_float('', state.spectoPos, 0,
                                              max_slider)

            if spectoSlider[0]:
                # print('Got slider change: %s' % spectoSlider[1])
                dispatch(actions.setSpectoPosition(spectoSlider[1]))

            wrap.setup()
            wrap.tryRender(state.file.spectograph,
                           state.file.data,
                           drawline=drawline,
                           spectoPos=state.spectoPos,
                           sr=sr,
                           hop_l=hop_l,
                           audioState=state.audioState,
                           x_len=x_length,
                           y_len=y_length)
            if wrap.fbo is None:
                imgui.end()
                return

            targetId = wrap.fbo.color_attachments[0].glo

            imgui.separator()
            imgui.image(targetId,
                        wrap.viewportSize,
                        y_length,
                        uv0=(0, 1),
                        uv1=(1, 0),
                        border_color=(1, 0, 0, 1))

            if imgui.is_item_hovered():
                io = imgui.get_io()
                if clickTracker.clicked(io.mouse_down[0]):
                    framesOfViewport = (wrap.viewportSize / (sr / hop_l))
                    viewX = imgui.get_io().mouse_pos.x - xPosStart
                    pos = state.spectoPos + (framesOfViewport *
                                             (viewX / wrap.viewportSize))

                    dispatch(actions.setLocalStartTime(pos))

            imgui.end()
