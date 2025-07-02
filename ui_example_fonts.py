
import framebuf, gc
import SQUiXL as squixl
from time import sleep_ms
import math

from SQUiXL_ui_fonts import (
    UIManager,
    UIScreen,
    UILabel,
    UILabelWriter, # new label class for using fonts
    UIButton,
    UISlider,
    UICheckBox,
    UIProgressBar,
    TouchEvent,
    TOUCH_TAP,
    TOUCH_DRAG,
    TOUCH_DRAG_END,
    rgb_to_565,
    WriterDevice  # new import for fonts
    
)

# import the Cwriter class and a choice of fonts
from writer import CWriter
from fonts import arial35
from fonts import arial10 
from fonts import freesans20 as sans20
from fonts import font10

# import a helper where some predfined colours are specified for ease of use
from colors import *

# The SQUiXL library now supports context managers, so we now intitialise the library using a with block, which will automatically deinit() the LCD peripheral when you exit back to the REPL.

# This means no hard reset or even soft reset is required between stopping and re-starting your code.

with squixl as squixl:

    exiting = False

    buf = squixl.create_display()

    squixl.screen_init_spi_bitbanged()

    fb = framebuf.FrameBuffer(buf, 480, 480, framebuf.RGB565)
    
    # amendment to use the writer module for writing fonts to the framebuffer
    wbuf = WriterDevice(fb)
    
    # create Cwriters fonts and default colours 
    fontM = CWriter(wbuf, arial35, fgcolor=YELLOW, bgcolor=SQBLUE, verbose=False)
    fontS = CWriter(wbuf, sans20, fgcolor=WHITE, verbose=False)
    fontTiny = CWriter(wbuf, font10, fgcolor=WHITE, verbose=False)
    cw1 = CWriter(wbuf, arial10, GREEN, BLACK, verbose=False)
    
    
    # using the existing framebuffer with misicule text wite to framebuffer
    fb.fill(0x2112)
    fb.text("Hey! It's SQUiXL in MicroPython!", 100, 50, 0xffe0)
    
    # from now on the exmple uses various fonts of different sizes and
    # not the framebuffer text function.
    # ------------------------------------------------------------

    mgr = UIManager(wbuf)  #not that wbuf is passed.
    # Dark grey background
    settings = UIScreen('settings', bg_color=rgb_to_565(50, 50, 50))
    mgr.add_screen(settings)
    mgr.set_screen('settings')

    # Positions for controls
    # Four feature checkboxes starting at y=40, spaced 40px apart
    # note the addition parameter specifying a font.
    y_positions = [40, 40, 100, 100]
    x_pos = 20
    features = ['WiFi', 'Bluetooth', 'GPS', 'NFC']
    for y, feat in zip(y_positions, features):
        chk = UICheckBox(
            x=x_pos, y=y,
            title=feat, size=35, checked=True,
            callback=lambda s, f=feat: print(f"{f}: {s}"),
            fg_color=rgb_to_565(220, 220, 220),
            bg_color=rgb_to_565(60, 60, 60),
            check_color=rgb_to_565(100, 100, 100),
            label_color=rgb_to_565(220, 220, 220),
            font=fontTiny
        )
        x_pos += 140
        if x_pos > 180:
            x_pos = 20
        settings.add_control(chk)
    
    # Add some text to the famebuffer
    headertext = UILabelWriter(20, 150, 0, 0, 'Widget Demo', text_color=PUSE,font=fontM)
    settings.add_control(headertext)
    
    # Note - the use of the UILabelWriter in place of UILabel in order to use specified fonts
    # Brightness slider at y=220
    bright_lbl = UILabelWriter(20, 200, 0, 0, 'Brightness: 50', text_color=YELLOW,font=fontS)
    settings.add_control(bright_lbl)
    bright_sld = UISlider(
        x=20, y=220, w=440, h=30,
        min_val=0, max_val=100, value=50,
        callback=lambda v: bright_lbl.set_text(f"Brightness: {int(v)}"),
        track_color=rgb_to_565(180, 180, 180),
        knob_color=rgb_to_565(0, 120, 255),
        bg_color=rgb_to_565(60, 60, 60)
    )
    settings.add_control(bright_sld)

    # Volume slider at y=280
    vol_lbl = UILabelWriter(20, 260, 0, 0, 'Volume: 50', text_color=GREEN,font=fontS)
    settings.add_control(vol_lbl)
    vol_sld = UISlider(
        x=20, y=280, w=440, h=30,
        min_val=0, max_val=100, value=50,
        callback=lambda v: vol_lbl.set_text(f"Volume: {int(v)}"),
        track_color=rgb_to_565(180, 180, 180),
        knob_color=rgb_to_565(255, 100, 100),
        bg_color=rgb_to_565(60, 60, 60)
    )
    settings.add_control(vol_sld)

    # CPU usage bar at y=340
    cpu_lbl = UILabelWriter(20, 320, 0, 0, 'CPU Usage', text_color=PINK,font=fontS)
    settings.add_control(cpu_lbl)
    cpu_pb = UIProgressBar(
        x=20, y=340, w=440, h=25,
        min_val=0, max_val=100, value=55,
        track_color=rgb_to_565(200, 200, 200),
        fill_color=rgb_to_565(255, 100, 0),
        bg_color=rgb_to_565(60, 60, 60)
    )
    settings.add_control(cpu_pb)

    # Action buttons at bottom y=400
    btn_y = 400
    btn_w, btn_h = 120, 40
    labels = ['Apply', 'Reset', 'Exit']
    cbs = []

    def on_apply():
        print('Settings applied')
    
    def on_reset():
        for ctrl in settings.controls:
            if hasattr(ctrl, 'set_value'):
                ctrl.set_value(0)
            if hasattr(ctrl, 'set_checked'):
                ctrl.set_checked(False)
    
    def on_exit():
        global exiting
        print('Exiting settings')
        exiting = True

    callbacks = [on_apply, on_reset, on_exit]
    btn_x = 20
    button_cols = [RED, GREEN, CYAN]
    button_index = 0
    for lbl, cb in zip(labels, callbacks):
        btn = UIButton(
            x=btn_x, y=btn_y,
            w=btn_w, h=btn_h,
            title=lbl, callback=cb,
            fg_color=rgb_to_565(220, 220, 220),
            bg_color=rgb_to_565(60, 60, 60),
            text_color=button_cols[button_index],
            font=fontS
        )
        settings.add_control(btn)
        btn_x += btn_w + 20
        button_index += 1

    # Initial draw
    mgr.draw_all()


    # -------------------------------------------------------------------
    # Touch dispatch: call this function for each touch event.
    # -------------------------------------------------------------------
    def handle_touch(x, y, touch_type):
        evt = TouchEvent(touch_type, x, y)
        mgr.process_touch(evt)

    # In your main loop, call:
    #   handle_touch(tx, ty, TOUCH_TAP)
    #   handle_touch(tx, ty, TOUCH_DRAG)
    #   handle_touch(tx, ty, TOUCH_DRAG_END)
    # etc.

    last_x = -1
    last_y = -1

    while not exiting:
        got_new = False
        n, points = squixl.touch.read_points()
        for i in range(0, n):
            if last_y != points[i][1] and last_x != points[i][0]:
                got_new = True
                print(f"id {points[i][3]} x {points[i][1]} y {points[i][0]} size {points[i][2]}\n\n")
                last_x = points[i][0]
                last_y = points[i][1]
        
        # If we got a new touch position buzz the squixl
        if got_new:
            evt = TouchEvent(TOUCH_TAP, last_x, last_y)
            mgr.process_touch(evt)
        
        sleep_ms(100)

