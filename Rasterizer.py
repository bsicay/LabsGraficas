from src.gl import Renderer
import src.shaders as shaders

width = 1200
height = 800

# medium shot
renderer = Renderer(width, height)
renderer.vertexShader = shaders.vertexShader
renderer.cartoonShader = shaders.cartoonShader
renderer.glLookAt(camPos=(0.9, 1, 0), eyePos=(0, 0, -5))
renderer.gl_load_model(
    filename="models/wooden.obj",
    textureName="models/textures/wood.bmp",
    translate=(0, -1, -5),
    rotate=(0, 75, 0),
    scale=(1, 1, 1)
)
renderer.glRender()
renderer.glFinish("out/gradientShader.bmp")


# # low angle
# renderer = Renderer(width, height)
# renderer.vertexShader = shaders.vertexShader
# renderer.fragmentShader = shaders.fragmentShader
# renderer.glLookAt(camPos=(0, -3, 0), eyePos=(0, 0, -5))
# renderer.gl_load_model(
#     filename="models/wooden.obj",
#     textureName="models/textures/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, 0),
#     scale=(2, 2, 2)
# )
# renderer.glRender()
# renderer.glFinish("out/lowAngle.bmp")


# # high angle
# renderer = Renderer(width, height)
# renderer.vertexShader = shaders.vertexShader
# renderer.fragmentShader = shaders.fragmentShader
# renderer.glLookAt(camPos=(0, 5, 0), eyePos=(0, 0, -5))
# renderer.gl_load_model(
#     filename="models/wooden.obj",
#     textureName="models/textures/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, 0),
#     scale=(2, 2, 2)
# )
# renderer.glRender()
# renderer.glFinish("out/hightAngle.bmp")


# # dutch angle
# renderer = Renderer(width, height)
# renderer.vertexShader = shaders.vertexShader
# renderer.fragmentShader = shaders.fragmentShader
# renderer.glLookAt(camPos=(1, 2.3, 0), eyePos=(0, 0, -5))
# renderer.gl_load_model(
#     filename="models/wooden.obj",
#     textureName="models/textures/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, -15),
#     scale=(2, 2, 2)
# )
# renderer.glRender()
# renderer.glFinish("out/dutchAngle.bmp")
