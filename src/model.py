
from .obj import Obj
from .texture import Texture

class Model:
    def __init__(self, filename: str, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        self.loadModel(filename)
        self.filename = filename
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.texture = None
        self.normal_map = None
        self.customShaders(None, None)

    def loadModel(self, filename: str) -> None:
        model = Obj(filename)

        self.vertices = model.vertices
        self.tex_coords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

    def loadTexture(self, texture_name: str) -> None:
        self.texture = Texture(texture_name)

    def normalMap(self, normal_name: str) -> None:

        self.normal_map = Texture(normal_name)

    def customShaders(self, vertex_shader, fragment_shader) -> None:

        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
