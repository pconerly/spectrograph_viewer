## Spikes

Spikes is a desktop program to view a spectograph of a selected mp3. It's written in python, using py-imgui for GUI, openGL for the spectograph, and scipy for fourier analysis.

### Set up Guide

I recommend using `virtualenv-wrapper` and python 3.9.5

```
mkvirtualenv spikes
pip install -r requirements.txt
```

To run for development:

```
python imgui_desktop_app.py
```
