import math
from math import pi, sin, cos, tan
from src.struct import color, char, dword, word
from .mathLB import barycentric_coords, formatMatrix, formatVector
from .obj import Obj
from .texture import Texture


TRIANGLES = 2

class Model:
    def __init__(self, filename, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        
    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)

class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.currColor = color(1, 1, 1)
        self.objects = []
        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.activeTexture = None
        self.glViewport(0, 0, width, height)
        self.glCamMatrix()
        self.glProjectionMatrix()
        self.glClearColor(63/255,64/255,53/255)
        self.glClear()

    def glClear(self):
        self.pixels = [[self.clearColor for _ in range(self.height)]
                       for _ in range(self.width)]
        self.zbuffer = [[float('inf') for _ in range(self.height)]
                        for _ in range(self.width)]

    def glClearColor(self, r: float, g: float, b: float):
        self.clearColor = color(r, g, b)

    def glColor(self, r: float, g: float, b: float):
        self.currColor = color(r, g, b)

    def glPoint(self, x: int, y: int, clr=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x][y] = clr or self.curr_color

    def glTriangle(self, A, B, C, vtA, vtB, vtC):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    P = (x, y)
                    bCoords = barycentric_coords(A, B, C, P)

                    if bCoords is not None:
                        u, v, w = bCoords
                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z
                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                   u * vtA[1] + v * vtB[1] + w * vtC[1])

                            if self.fragmentShader is not None:
                                colorP = self.fragmentShader(
                                    tex_coords=uvs, 
                                    texture=self.activeTexture)
                                
                                self.glPoint(x, y, color(
                                    colorP[0], colorP[1], colorP[2]))
                            else:
                                self.point(x, y)

    def glPrimitiveAssembly(self, tVerts, tTexCoords):
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                triangle = []
                triangle.append(tVerts[i])
                triangle.append(tVerts[i + 1])
                triangle.append(tVerts[i + 2])

                triangle.append(tTexCoords[i])
                triangle.append(tTexCoords[i + 1])
                triangle.append(tTexCoords[i + 2])

                primitives.append(triangle)

        return primitives

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

        self.vpMatrix = formatMatrix([[width/2, 0, 0, x + width/2],
                                        [0, height/2, 0, y + height/2],
                                        [0, 0, 0.5, 0.5],
                                        [0, 0, 0, 1]])

    def glLookAt(self, camPos=(0, 0, 0), eyePos=(0, 0, 0)):

        world_up = formatVector([0, 1, 0])

        forward = formatVector(camPos) - formatVector(eyePos)
        forward = forward.normalize()

        right = world_up.cross(forward)
        right = right.normalize()

        up = forward.cross(right)
        up = up.normalize()
        self.camMatrix = formatMatrix([
            [right.data[0], up.data[0], forward.data[0], camPos[0]],
            [right.data[1], up.data[1], forward.data[1], camPos[1]],
            [right.data[2], up.data[2], forward.data[2], camPos[2]],
            [0, 0, 0, 1]
        ])

        self.view_matrix = self.camMatrix.inversa()

    def glCamMatrix(self, translate=(0, 0, 0), rotate=(0, 0, 0)):
        self.camMatrix = self.model_matrix(translate, rotate)
        self.view_matrix = self.camMatrix.inversa()

    def glProjectionMatrix(self, n=0.1, f=1000, fov=60):
        aspect_ratio = self.vpWidth / self.vpHeight
        t = tan((fov * pi / 180) / 2) * n
        r = t * aspect_ratio

        self.projectionMatrix = formatMatrix([[n/r, 0, 0, 0],
                                          [0, n/t, 0, 0],
                                          [0, 0, -(f+n)/(f-n), -
                                           (2*f*n)/(f-n)],
                                          [0, 0, -1, 0]])

    def model_matrix(self, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        translation = formatMatrix([[1, 0, 0, translate[0]],
                               [0, 1, 0, translate[1]],
                               [0, 0, 1, translate[2]],
                               [0, 0, 0, 1]])

        rot_mat = self.glRotationMatrix(rotate[0], rotate[1], rotate[2])

        scale_mat = formatMatrix([[scale[0], 0, 0, 0],
                             [0, scale[1], 0, 0],
                             [0, 0, scale[2], 0],
                             [0, 0, 0, 1]])

        return translation * rot_mat * scale_mat

    def glRotationMatrix(self, pitch=0, yaw=0, roll=0):
        pitch *= pi / 180
        yaw *= pi / 180
        roll *= pi / 180

        pitchMat = formatMatrix([[1, 0, 0, 0],
                              [0, cos(pitch), -sin(pitch), 0],
                              [0, sin(pitch), cos(pitch), 0],
                              [0, 0, 0, 1]])

        yawMat = formatMatrix([[cos(yaw), 0, sin(yaw), 0],
                              [0, 1, 0, 0],
                              [-sin(yaw), 0, cos(yaw), 0],
                              [0, 0, 0, 1]])

        rollMat = formatMatrix([[cos(roll), -sin(roll), 0, 0],
                              [sin(roll), cos(roll), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        return pitchMat * yawMat * rollMat

    def line(self, v0, v1, clr=None):

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y0 == y1:
            self.point(x0, y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x, clr or self.currColor)
            else:
                self.point(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def gl_load_model(self, filename, textureName, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(textureName)
        self.objects.append(model)

    def glRender(self):

        transformedVerts = []
        texCoords = []

        for model in self.objects:

            self.activeTexture = model.texture
            mMat = self.model_matrix(model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0, model_matrix=mMat, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    v1 = self.vertexShader(v1, model_matrix=mMat, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    v2 = self.vertexShader(v2, model_matrix=mMat, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(v3, model_matrix=mMat, view_matrix=self.view_matrix,
                                                projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]

                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)
                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)

        primitives = self.glPrimitiveAssembly(transformedVerts, texCoords)

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(prim[0], prim[1], prim[2], prim[3], prim[4], prim[5])

    def glFinish(self, filename):
        with open(filename, "wb") as file:
             # BMP header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # DIB header    
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Pixel data
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

        print(f"{filename} creado!")
