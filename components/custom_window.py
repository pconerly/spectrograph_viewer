def test_window(state, dispatch):

    imgui.set_next_window_size(300, 500)
    imgui.set_next_window_position(0, 20)
    if imgui.begin("Custom window",
                   flags=imgui.WINDOW_NO_RESIZE
                   | imgui.WINDOW_NO_MOVE):
        beep = imgui.button('Beep')
        # if beep:
        #     messages.append('beep clicked')
        incr = imgui.button('UP')
        decr = imgui.button('DOWN')
        if incr:
            dispatch({'type': 'INCREMENT'})
        if decr:
            dispatch({'type': 'DECREMENT'})

        # for m in messages:
        #     imgui.text(m)
        # imgui.menu_item

        if imgui.begin_menu('what'):
            imgui.menu_item('Foobar??')
            if imgui.begin_menu('iters'):
                imgui.menu_item('1??')
                imgui.menu_item('2??')
                imgui.menu_item('3??')
                imgui.menu_item('4??')
                imgui.end_menu()
            imgui.end_menu()

        imgui.text("Derp a little derp")
        imgui.text('FILES')
        imgui.text('\n'.join(state['files']))
        imgui.text('\n\n')
        imgui.text_colored("Eggs", 0.2, 1., 0.)
    imgui.end()
