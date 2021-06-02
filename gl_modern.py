import math
import moderngl
import numpy as np

import OpenGL.GL as gl

from PIL import Image

from state import AudioState


def getXYBox():
    x = np.array([-1., 1., 1., 1., -1., -1.])
    y = np.array([1., 1., -1., -1., -1., 1.])
    return x, y


def get01XYBox():
    x = np.array([0., 1., 1., 1., 0., 0.])
    y = np.array([1., 1., 0., 0., 0., 1.])
    return x, y


class Wrapper(object):
    isSetup = False
    verbose = False
    fbo = None
    props = None
    ctx = None
    viewportSize = 680

    def setup(self):
        if not self.isSetup:
            try:
                self.ctx = moderngl.create_context()
            except (Exception, ) as e:
                print('Couldnt find context, creating my own')
                self.ctx = moderngl.create_standalone_context()

            self.prog = self.ctx.program(
                vertex_shader='''
                    #version 330

                    uniform sampler2D specto;

                    in vec2 in_vert;
                    in vec3 in_color;

                    out vec3 v_color;
                    out vec2 myCoord;

                    void main() {
                        v_color = in_color;

                        myCoord = in_vert;
                        gl_Position = vec4(in_vert, 0.0, 1.0);
                        gl_Position = vec4(in_vert * 2.0 - 1.0, 0.0, 1.0);
                    }
                ''',
                fragment_shader='''
                    #version 330

                    in vec3 v_color;
                    in vec2 myCoord;

                    out vec4 f_color;
                    uniform sampler2D specto;
                    uniform float drawline;
                    uniform float x_length;

                    void main() {
                        vec4 red = texture(specto, myCoord);
                        float str = red.r * 1.;

                        float g = min(
                            step(drawline / x_length, myCoord.x),
                            step(myCoord.x, (drawline + 1) / x_length));
                        f_color = red;
                        f_color = vec4(str, g, 0., 1.0);
                    }
                ''',
            )

            self.isSetup = True

    def makeProps(self, drawline, spectoPos, sr, hop_l, audioState, x_len,
                  y_len):
        spectoPosFrame = int(spectoPos * (sr / hop_l))
        if audioState == AudioState.Playing:
            if drawline + 100 > spectoPosFrame + self.viewportSize:
                spectoPosFrame = int(drawline + 100 - self.viewportSize)

            # correct for overzealousness
            spectoPosFrame = min(spectoPosFrame, x_len - self.viewportSize)

        return (drawline, spectoPos, sr, hop_l, spectoPosFrame, audioState,
                x_len, y_len)

    def tryRender(self,
                  specto,
                  data,
                  drawline=-1,
                  spectoPos=0,
                  sr=44100,
                  hop_l=512,
                  audioState=AudioState.Stopped,
                  x_len=0,
                  y_len=0):
        newProps = self.makeProps(drawline, spectoPos, sr, hop_l, audioState,
                                  x_len, y_len)
        if self.props == newProps:
            if self.verbose:
                print('_', end='', flush=True)
            return
        # else, we should rerender
        self.props = newProps
        self.getFBOforSpectograph(specto, data)

    def getFBOforSpectograph(self, specto, data, show_image=False):
        if self.verbose:
            print('+', end='', flush=True)
        (drawline, spectoPos, sr, hop_l, spectoPosFrame, audioState, x_len,
         y_len) = self.props

        desiredShape = (x_len, y_len)
        if specto.shape != desiredShape:
            # print('Reshaping array from %s to %s' % (specto.shape,
            #                                          desiredShape))
            specto = np.reshape(specto, desiredShape)
            specto = (specto + 80) / 80.

        drawlineRelativePos = math.ceil(drawline - spectoPosFrame)

        specto = specto[spectoPosFrame:spectoPosFrame + self.viewportSize]

        floatSpecto = specto.astype('f4')
        registerNumber = 1
        spectoTx = self.ctx.texture(specto.shape,
                                    1,
                                    data=floatSpecto.tobytes(order='F'),
                                    dtype='f4')

        spectoTx.filter = (moderngl.NEAREST, moderngl.NEAREST)
        spectoTx.swizzle = 'RRR1'

        spectoTx.use(registerNumber)
        self.prog['specto'].value = registerNumber
        self.prog['drawline'].value = drawlineRelativePos
        self.prog['x_length'].value = self.viewportSize

        x, y = get01XYBox()
        r = np.random.rand(6)
        g = np.random.rand(6)
        b = np.random.rand(6)

        vertices = np.dstack([x, y, r, g, b])

        vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        vao = self.ctx.simple_vertex_array(self.prog, vbo, 'in_vert',
                                           'in_color')

        tx = self.ctx.texture((self.viewportSize, y_len), 4)
        fbo = self.ctx.framebuffer((tx, ))
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)

        vao.render(moderngl.TRIANGLES)
        if show_image:
            Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0,
                            -1).show()

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        self.fbo = fbo
        return fbo


if __name__ == '__main__':
    # THIS EXAMPLE IS GOING TO FAIL SPECTACULARLY
    x_len = 200
    y_len = 100
    specto = np.random.rand(x_len * y_len)

    print('------------')
    specto = np.reshape(specto, (-1, y_len))
    print('specto.shape', specto.shape)

    data = {
        'x_length': x_len,
        'y_length': y_len,
    }
    fbo = getFBOforSpectograph(specto, data, show_image=True)
    Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1).show()
