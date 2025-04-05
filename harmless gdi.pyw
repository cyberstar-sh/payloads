import ctypes
from ctypes import wintypes
import random
import numpy as np
import sounddevice as sd
import time
import threading

# Windows API setup
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Screen dimensions
sw = user32.GetSystemMetrics(0)
sh = user32.GetSystemMetrics(1)

# Constants
SRCCOPY = 0x00CC0020
PATINVERT = 0x005A0049

def RGB(r, g, b):
    return r + (g << 8) + (b << 16)

def play_loud_bytebeat(duration=3):
    """Generate and play louder 8-bit style sounds"""
    samplerate = 8000
    t = np.arange(samplerate * duration)
    
    # More intense sound formulas (fixed parentheses)
    formulas = [
        "np.array((t|(t>>9|t>>7))*t&(t>>11|t>>9)) & 255",
        "np.array(t*((t>>12|t>>8)&63&t>>4)) & 255",
        "np.array((t>>7|t|t>>6)*10+4*(t&t>>13|t>>6)) & 255"
    ]
    
    try:
        formula = random.choice(formulas)
        signal = eval(formula, {'t': t, 'np': np})
        signal = (signal - 128) / 64.0  # Louder normalization
        sd.play(signal, samplerate=samplerate, blocking=False)
    except:
        pass

def draw_chaos(hdc, duration):
    """Draw random lines, shapes and glitches"""
    end_time = time.time() + duration
    
    # Pre-create some pens and brushes
    pens = []
    brushes = []
    for _ in range(10):
        pen = gdi32.CreatePen(0, random.randint(1,5), 
                    RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        pens.append(pen)
        
        brush = gdi32.CreateSolidBrush(
                    RGB(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        brushes.append(brush)
    
    while time.time() < end_time:
        # Random lines
        for _ in range(20):
            pen = random.choice(pens)
            gdi32.SelectObject(hdc, pen)
            gdi32.MoveToEx(hdc, random.randint(0,sw), random.randint(0,sh), None)
            gdi32.LineTo(hdc, random.randint(0,sw), random.randint(0,sh))
        
        # Random rectangles/ellipses
        for _ in range(15):
            brush = random.choice(brushes)
            gdi32.SelectObject(hdc, brush)
            left = random.randint(0, sw-100)
            top = random.randint(0, sh-100)
            right = left + random.randint(50, 300)
            bottom = top + random.randint(50, 300)
            
            if random.choice([True, False]):
                gdi32.Rectangle(hdc, left, top, right, bottom)
            else:
                gdi32.Ellipse(hdc, left, top, right, bottom)
        
        # Screen glitch effects
        if random.random() < 0.7:
            x, y = random.randint(0, sw-200), random.randint(0, sh-200)
            w, h = random.randint(100, 400), random.randint(100, 400)
            gdi32.PatBlt(hdc, x, y, w, h, PATINVERT)
        
        time.sleep(0.05)
    
    # Cleanup
    for pen in pens:
        gdi32.DeleteObject(pen)
    for brush in brushes:
        gdi32.DeleteObject(brush)

def main():
    hdc = user32.GetDC(0)
    
    try:
        # Run effects for 15 seconds
        end_time = time.time() + 15
        
        while time.time() < end_time:
            # Start sound in separate thread
            threading.Thread(target=play_loud_bytebeat, daemon=True).start()
            
            # Visual effects
            draw_chaos(hdc, 1)  # Shorter duration for more frequent updates
            
            # Occasionally invert entire screen
            if random.random() < 0.3:
                gdi32.PatBlt(hdc, 0, 0, sw, sh, PATINVERT)
    finally:
        # Cleanup
        user32.ReleaseDC(0, hdc)

if __name__ == "__main__":
    main()
