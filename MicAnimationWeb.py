
from js import document, window, console
from pyodide.ffi import create_proxy
import math

print("Python code is running!")

canvas = document.getElementById('micCanvas')
ctx = canvas.getContext('2d')
size = canvas.parentElement.clientWidth * 0.8
canvas.width = size
canvas.height = size

x = canvas.width / 2
y = canvas.height / 2

print("Canvas width: ", canvas.width, " Canvas height: ", canvas.height)

frame = 0
rotation_modifier = 0
smoothed_volume = 0
increasing = True
dots = range(50)

def animate(timestamp=None):
    global rotation_modifier
    global smoothed_volume
    global frame
    global increasing

    rotation_modifier += 0.1

    if(increasing):
        smoothed_volume += 1 
    if(smoothed_volume > canvas.width*0.35):
        increasing = False;
    else:
        smoothed_volume -= 1
    if(smoothed_volume < (canvas.width*0.01)):
        increasing = True;

    radius = canvas.width*0.1 + smoothed_volume

    # Clear HTML canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.fillStyle = '#777777'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = 'black'
    ctx.arc(x, y, canvas.width*0.48, 0, 2 * math.pi)
    ctx.fill()

    ctx.fillStyle = 'cyan'

    for i in range(len(dots)):

        rotateX = x + (radius / len(dots)) * i * math.cos(i + rotation_modifier)
        rotateY = y + (radius / len(dots)) * i * math.sin(i + rotation_modifier)

        color = f"rgb({255 - i * 5}, 255, 255)"
        ctx.fillStyle = color

        ctx.beginPath()
        ctx.strokeStyle = 'black'
        ctx.arc(
            rotateX,
            rotateY,
            canvas.width/20,
            0,
            2 * math.pi
        )
        ctx.stroke()
        ctx.fill()
    window.requestAnimationFrame(animation_callback)

animation_callback = create_proxy(animate)
window.requestAnimationFrame(animation_callback)