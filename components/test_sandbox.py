def test_sandbox(state, dispatch):
    if imgui.begin("Custom window2", True):
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1., 0.)

        imgui.text('Directory:')
        changed, new_text_val = imgui.input_text('input', text_val, 400)
        if changed:
            text_val = new_text_val
        imgui.text('You wrote:')
        imgui.same_line()
        imgui.text(text_val)

        imgui.end()
