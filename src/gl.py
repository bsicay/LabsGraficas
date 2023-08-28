import math
from math import pi, sin, cos, tan
from src.struct import color, char, dword, word
from .mathLB import barycentric_coords, formatMatrix, formatVector
from .obj import Obj
from .texture import Texture


TRIANGLES = 2
    
class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.currColor = color(1, 1, 1)
        self.objects = []
        self.fragment_shader = None
        self.vertex_shader = None
        self.cartoonShader = None
        self.primitiveType = TRIANGLES
        self.activeTexture = None
        self.activeNormalMap = None
        self.glViewport(0, 0, width, height)
        self.glCamMatrix()
        self.glProjectionMatrix()
        self.glClearColor(63/255,64/255,53/255)
        self.glClear()
        self.background = None
        self.directionalLight = formatVector([0, 0, 0])
    
    def setDirectionalLight(self, x, y, z):
        self.directional_light = formatVector([x, y, z])

    def glBackgroundTexture(self, filename):
        self.background = Texture(filename)

    def glClearBackground(self):
        self.glClear()
        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                    u = (x - self.vpX) / self.vpWidth
                    v = (y - self.vpY) / self.vpHeight
                    texture_color = self.background.get_color(u, v)
                    if texture_color:
                        self.glPoint(x, y, color(
                            texture_color[0], texture_color[1], texture_color[2]))

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
    
    def add_model(self, model):
        self.objects.append(model)

    def glTriangle(self, transformed_verts,  u_verts, tex_coords, normals):
        A = transformed_verts[0]
        B = transformed_verts[1]
        C = transformed_verts[2]

        min_x = round(min(A[0], B[0], C[0]))
        max_x = round(max(A[0], B[0], C[0]))
        min_y = round(min(A[1], B[1], C[1]))
        max_y = round(max(A[1], B[1], C[1]))

        if self.active_normal_map is not None:
            A_untransformed = u_verts[0]
            B_untransformed = u_verts[1]
            C_untransformed = u_verts[2]

            edge1 = formatVector(B_untransformed) - formatVector(A_untransformed)
            edge2 = formatVector(C_untransformed) - formatVector(A_untransformed)

            delta_uv1 = formatVector(tex_coords[1]) - formatVector(tex_coords[0])
            delta_uv2 = formatVector(tex_coords[2]) - formatVector(tex_coords[0])

            delta = delta_uv1.data[0] * delta_uv2.data[1] - \
                delta_uv2.data[0] * delta_uv1.data[1]
            if delta == 0:
                f = 0
            else:
                f = 1 / delta

            tangent = formatVector([f * (delta_uv2.data[1] * edge1.data[0] - delta_uv1.data[1] * edge2.data[0]),
                               f * (delta_uv2.data[1] * edge1.data[1] -
                                    delta_uv1.data[1] * edge1.data[1]),
                               f * (delta_uv2.data[1] * edge1.data[2] - delta_uv1.data[1] * edge2.data[2])])

            tangent = tangent.normalize()
        else:
            tangent = None

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    P = (x, y)
                    b_coords = barycentric_coords(A, B, C, P)

                    if b_coords is not None:
                        u, v, w = b_coords
                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            if self.fragment_shader is not None:

                                colorP = self.fragment_shader(
                                    texture=self.active_texture,
                                    normal_map=self.active_normal_map,
                                    tex_coords=tex_coords,
                                    normals=normals,
                                    directional_light=self.directional_light,
                                    barycentric_coords=b_coords,
                                    cam_matrix=self.camMatrix,
                                    tangent=tangent)
                                if colorP is not None:
                                    self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                self.point(x, y)

    def primitive_assembly(self, t_verts, u_verts, t_tex_coords, normals):
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(t_verts), 3):
                triangle = []
                c_verts = []
                ux_verts = []
                c_tex_coords = []
                c_normals = []

                for j in range(3):
                    c_verts.append(t_verts[i + j])
                for j in range(3):
                    ux_verts.append(u_verts[i + j])
                for j in range(3):
                    c_tex_coords.append(t_tex_coords[i + j])
                for j in range(3):
                    c_normals.append(normals[i + j])

                triangle = [c_verts, ux_verts, c_tex_coords, c_normals]
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

    def glAddModel(self, model):
        self.objects.append(model)

    def glRender(self):

        transformed_verts = []
        tex_coords = []
        normals = []

        for model in self.objects:
            print("Rendering model: " + model.filename)
            transformed_verts = []
            untransformed_verts = []
            tex_coords = []
            normals = []

            self.vertex_shader = model.vertex_shader
            self.fragment_shader = model.fragment_shader

            self.active_texture = model.texture
            self.active_normal_map = model.normal_map
            model_matrix = self.model_matrix(
                model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                # first_triangle_normal = (
                #     evector(v1) - evector(v0)).cross(evector(v2) - evector(v0))
                # first_triangle_normal = first_triangle_normal.normalize()
                # normals.append(first_triangle_normal)
                # if vertCount == 4:
                #     second_triangle_normal = (
                #         evector(v2) - evector(v0)).cross(evector(v3) - evector(v0))
                #     second_triangle_normal = second_triangle_normal.normalize()
                #     normals.append(second_triangle_normal)
                untransformed_verts.append(v0)
                untransformed_verts.append(v1)
                untransformed_verts.append(v2)
                if vertCount == 4:
                    untransformed_verts.append(v0)
                    untransformed_verts.append(v2)
                    untransformed_verts.append(v3)

                if self.vertex_shader:
                    v0 = self.vertex_shader(v0, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    v1 = self.vertex_shader(v1, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    v2 = self.vertex_shader(v2, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)
                    if vertCount == 4:
                        v3 = self.vertex_shader(v3, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                                projection_matrix=self.projectionMatrix, viewport_matrix=self.vpMatrix)

                transformed_verts.append(v0)
                transformed_verts.append(v1)
                transformed_verts.append(v2)
                if vertCount == 4:
                    transformed_verts.append(v0)
                    transformed_verts.append(v2)
                    transformed_verts.append(v3)
                
                # print(face[0][0])

                vt0 = model.tex_coords[face[0][1] - 1]
                vt1 = model.tex_coords[face[1][1] - 1]
                vt2 = model.tex_coords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.tex_coords[face[3][1] - 1]

                tex_coords.append(vt0)
                tex_coords.append(vt1)
                tex_coords.append(vt2)
                if vertCount == 4:
                    tex_coords.append(vt0)
                    tex_coords.append(vt2)
                    tex_coords.append(vt3)

                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]
                if vertCount == 4:
                    vn3 = model.normals[face[3][2] - 1]

                normals.append(vn0)
                normals.append(vn1)
                normals.append(vn2)
                if vertCount == 4:
                    normals.append(vn0)
                    normals.append(vn2)
                    normals.append(vn3)

            primitives = self.primitive_assembly(
                transformed_verts, untransformed_verts, tex_coords, normals)

            for prim in primitives:
                if self.primitiveType == TRIANGLES:
                    self.glTriangle(prim[0], prim[1], prim[2], prim[3])


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
