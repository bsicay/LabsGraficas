from src.gl import Renderer
from src.model import Model
import src.shaders as shaders


width = 1920
height = 1080

renderer = Renderer(width, height)

rock = Model(f"./models/CaveCrystal01.obj",
             translate=(-2, -25, -40), scale=(0.2, 0.2, 0.2), rotate=(0, 0, 0))
rock.loadTexture(f"./models/textures/CaveCrystal1_Lava1_Diffuse.bmp")
rock.normalMap(f"./models/textures/CaveCrystal1_Lava1_Normal.bmp")
rock.customShaders(shaders.vertex_shader, shaders.cartoonShader)

charizard = Model(f"./models//Charizard.obj",
             translate=(-2, -1, -5), scale=(0.1, 0.1, 0.1), rotate=(0, 90, 0))
charizard.loadTexture(f"./models/textures/charizard.bmp")
charizard.customShaders(shaders.vertex_shader, shaders.phong_shader)


groudon =  Model(f"./models/11.obj",
             translate=(2, 0, -5), scale=(0.06, 0.06, 0.06), rotate=(0, 155, 0))
groudon.loadTexture(f"./models/textures/groudon.bmp")
groudon.customShaders(shaders.vertex_shader, shaders.cartoonShader)


pokeball =  Model(f"./models/Pokeball.obj",
             translate=(-1, -1, -5), scale=(0.1, 0.1, 0.1), rotate=(0, 3, 0))
pokeball.loadTexture(f"./models/textures/pokeball.bmp")
pokeball.customShaders(shaders.vertex_shader, shaders.cartoonShader)

pokeball =  Model(f"./models/Pokeball.obj",
             translate=(-1, -1, -5), scale=(0.1, 0.1, 0.1), rotate=(0, 3, 0))
pokeball.loadTexture(f"./models/textures/pokeball.bmp")
pokeball.customShaders(shaders.vertex_shader, shaders.gradientShader)

renderer.setDirectionalLight(-1, -1, -1)
renderer.glLookAt(camPos=(1, 5, 0), eyePos=(0, 0, -7.5))
renderer.glBackgroundTexture(f"./models/background/stadium.bmp")
renderer.glClearBackground()


renderer.add_model(rock)
renderer.add_model(charizard)
renderer.add_model(groudon)
renderer.add_model(pokeball)



renderer.glRender()
renderer.glFinish("final.bmp")
