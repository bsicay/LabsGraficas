from src.gl import Renderer
import src.shaders as shaders

width = 1200
height = 800

# medium shot
renderer = Renderer(width, height)
renderer.vertexShader = shaders.vertexShader
renderer.fragmentShader = shaders.fragmentShader
renderer.glLookAt(camPos=(0.9, 1, 0), eyePos=(0, 0, -5))
renderer.gl_load_model(
    filename="models/wooden.obj",
    textureName="models/textures/wood.bmp",
    translate=(0, -1, -5),
    rotate=(0, 75, 0),
    scale=(1, 1, 1)
)
renderer.glRender()
renderer.glFinish("out/mediumShot.bmp")


# # low angle
# renderer = Renderer(width, height)
# renderer.set_clear_color(63/255,64/255,53/255)
# renderer.clear()
# renderer.vertex_shader = shaders.vertex_shader
# renderer.fragment_shader = shaders.fragment_shader
# renderer.look_at(cam_pos=(0, -3, 0), eye_pos=(0, 0, -5), rotateZ=0)
# renderer.gl_load_model(
#     filename=f"{models_dir}/wooden.obj",
#     texture_name=f"{textures_dir}/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, 0),
#     scale=(2, 2, 2)
# )
# renderer.gl_render()
# renderer.gl_finish(f"{out_dir}/low_angle.bmp")


# # high angle
# renderer = Renderer(width, height)
# renderer.set_clear_color(63/255,64/255,53/255)
# renderer.clear()
# renderer.vertex_shader = shaders.vertex_shader
# renderer.fragment_shader = shaders.fragment_shader
# renderer.look_at(cam_pos=(0, 5, 0), eye_pos=(0, 0, -5), rotateZ=0)
# renderer.gl_load_model(
#     filename=f"{models_dir}/wooden.obj",
#     texture_name=f"{textures_dir}/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, 0),
#     scale=(2, 2, 2)
# )
# renderer.gl_render()
# renderer.gl_finish(f"{out_dir}/high_angle.bmp")


# # dutch angle
# renderer = Renderer(width, height)
# renderer.set_clear_color(63/255,64/255,53/255)
# renderer.clear()
# renderer.vertex_shader = shaders.vertex_shader
# renderer.fragment_shader = shaders.fragment_shader
# renderer.look_at(cam_pos=(1, 2.3, 0), eye_pos=(0, 0, -5), rotateZ=-15)
# renderer.gl_load_model(
#     filename=f"{models_dir}/wooden.obj",
#     texture_name=f"{textures_dir}/wood.bmp",
#     translate=(0, 0, -5),
#     rotate=(0, 75, 0),
#     scale=(2, 2, 2)
# )
# renderer.gl_render()
# renderer.gl_finish(f"{out_dir}/dutch_angle.bmp")
