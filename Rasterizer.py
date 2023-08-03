from gl import Renderer, V3
import shaders
from obj import Obj
width = 2000
height = 1500

rend = Renderer(width,height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader


rend.glLoadModel(filename= "head.obj", textureName="a.bmp",
                translate=(400,350,0), scale=(5,5,5), rotate=(-45,0,-45))

rend.glLoadModel(filename= "head.obj", textureName="a.bmp",
                translate=(1500,300,0), scale=(5,5,5), rotate=(0,0,180))

rend.glLoadModel(filename= "head.obj", textureName="a.bmp",
                translate=(400,900,0), scale=(5,5,5), rotate=(-90,0,180))

rend.glLoadModel(filename= "head.obj", textureName="a.bmp",
                translate=(1500,900,0), scale=(5,5,5), rotate=(-45,0,45))


rend.glRender()

rend.glFinish("output.bmp")
