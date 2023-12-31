import struct
from collections import namedtuple
from obj import Obj
import math
from mathLB import mathLib
from texture import Texture

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point2', ['x', 'y', 'z'])
la = mathLib()

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3 

def char(c):
    #1 byte
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h',w)

def dword(d):
    #4 bytes
    return struct.pack('=l',d)

def color(r,g,b):
    return bytes([int(b*255),int(g*255),int(r*255)])

class Model(object):
    def __init__(self, filename, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
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
        
        

class Renderer(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.glClearColor(0,0,0)
        self.glClear()

        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

        self.activetexture = None

    def glAddVertices(self, vertices):
        for vert in vertices: 
            self.vertexBuffer.append(vert)

    def glPrimitiveAssemly(self, tVerts, tTextCoords):
        primitives = []
        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                triangle = []
                #vertices
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2])
                #texturas
                triangle.append(tTextCoords[i])
                triangle.append(tTextCoords[i+1])
                triangle.append(tTextCoords[i+2])

                primitives.append(triangle)
            
        
        return primitives

    def glClearColor(self,r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self,r,g,b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self,x,y,clr=None):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixels[x][y] = clr or self.currColor

    def glTriangle(self, v0, v1, v2, clr = None):
        self.glLine(v0, v1, clr or self.currColor)
        self.glLine(v1, v2, clr or self.currColor)
        self.glLine(v2, v0, clr or self.currColor)

    def glTriangle_bc(self, A, B, C, vtA, vtB, vtC):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        colorA = (1,0,0)
        colorB = (0,1,0)
        colorC = (0,0,1)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = (x,y)
                
                try :
                    u,v,w = libreria.barycentricCoords(A,B,C,P)
                    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1: 

                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                   u * vtA[1] + v * vtB[1] + w * vtC[1],
                                   u * vtA[2] + v * vtB[2] + w * vtC[2])

                            if self.fragmentShader != None:
                                colorP = self.fragmentShader(textCoords = uvs, 
                                                             texture = self.activetexture)
                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                self.glPoint(x, y, colorP)
                except:
                    pass

    def glModelMatrix(self, translate = (0,0,0), scale =(1,1,1), rotate=(0,0,0)):
        translation = [[1,0,0,translate[0]],
                                [0,1,0,translate[1]],
                                [0,0,1,translate[2]],
                                [0,0,0,1]]
        
        scaleMat = [[scale[0],0,0,0],
                                [0,scale[1],0,0],
                                [0,0,scale[2],0],
                                [0,0,0,1]]
        
        rx = [[1,0,0,0],
                                [0,math.cos(rotate[0]),-math.sin(rotate[0]),0],
                                [0,math.sin(rotate[0]),math.cos(rotate[0]),0],
                                [0,0,0,1]]
        
        ry = [[math.cos(rotate[1]),0,math.sin(rotate[1]),0],
                                [0,1, 0,0],
                                [-math.sin(rotate[1]),0,math.cos(rotate[1]),0],
                                [0,0,0,1]]
        
        rz = [[math.cos(rotate[2]),-math.sin(rotate[2]),0,0],
                                [math.sin(rotate[2]),math.cos(rotate[2]), 0,0],
                                [0,0,1,0],
                                [0,0,0,1]]
        
        mr = la.multiply_matrices(rx, ry, rz)

        # mr = rx*ry*rz
        
        # return translation * mr * scaleMat
        return la.multiply_matrices(translation, mr, scaleMat)
    
    def glLine(self, v0, v1, clr = None):
        #Bresenham line algorithm
        # y = mx + b
        # m = (v1.y - v0.y)/(v1.x - v0.x)
        # y = v0.y

        # for x in range(v0.x, v1.x + 1):
        #     self.glPoint(x,int(y))
        #     y += m
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Si el punto 0 es igual al punto 1, solo dibujar un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1 
        # intercambiamos las x por las y, y se dibuja la linea
        # de manera vertical en vez de horizontal 
        if steep: 
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # Si el punto inicial en x es mayor que el punto final en x, 
        # intercambiamos los puntos para siempre dibujar de 
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1): 
            if steep:
                # dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else: 
                    y -= 1
                limit += 1

    # edge_table toma una lista de vértices de un polígono y genera una tabla de bordes Edge Table.
    # La tabla almacena  los bordes del polígono y se utiliza en el algoritmo de Scanline para 
    # rellenar el polígono.

    def glLoadModel(self, filename, textureName, translate = (0,0,0),rotate = (0,0,0), scale = (1,1,1)):
        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(textureName)
        
        self.objects.append(model)

    def edge_table(self, vertices):
        et = {}
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i+1)%len(vertices)]

            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            if y1 == y2:
                continue

            if y1 not in et:
                et[y1] = []

            et[y1].append((y2, x1, (x2-x1)/(y2-y1)))

        return et

    # scanLine Toma una lista de vértices de un polígono 
    # y un color para rellenar.
    def scanline(self, vertices, r,g,b):
        # obtiene los bordes
        et = self.edge_table(vertices)
        ael = []
        self.glColor(r,g,b)
        # Itera sobre cada línea de barrido desde la mínima hasta la máxima línea de barrido
        for scanline in range(min(et), max(et)+1):
        # Si la línea de barrido actual está en la tabla de bordes,
        # añade todos los bordes que comienzan en esta línea a la lista de bordes activos
            if scanline in et:
                ael.extend(et[scanline])
            # Elimina de la lista de bordes activos cualquier borde que ya no cruce la línea de barrido
            ael = [i for i in ael if i[0] > scanline]

            ael.sort(key=lambda x: x[1])
            # Para cada par de bordes en la lista de bordes activos, 
            # rellena todos los píxeles entre ellos en la línea de barrido actual
            for i in range(0, len(ael), 2):
                for x in range(int(ael[i][1]), int(ael[i+1][1])):
                    self.glPoint(x, scanline, self.currColor)  # aqui es donde se dibuja el punto

            # Para cada borde en la lista de bordes activos, actualiza la coordenada x para la próxima línea de barrido
             # sumando la pendiente de la línea
            for i in range(len(ael)):
                y2, x, m = ael[i]
                ael[i] = (y2, x+m, m)

    # funcion para dibujar todo el contorno del poligono
    def glPolygon(self, vertices, clr=None):
        vertex_count = len(vertices)
        
        for i in range(vertex_count):
            v0 = vertices[i]
            v1 = vertices[(i + 1) % vertex_count]
            self.glLine(v0, v1, clr)


    def glRender(self):
        transformedVerts = []
        textCoords = []

        for model in self.objects:
            
            self.activetexture= model.texture

            mMat = self.glModelMatrix(model.translate, model.scale, model.rotate)

            for face in model.faces:
                verCount = len(face)

                v0 = model.vertices[ face[0][0]-1]
                v1 = model.vertices[ face[1][0]-1]
                v2 = model.vertices[ face[2][0]-1]
                if verCount == 4:
                    v3 = model.vertices[ face[3][0]-1]

                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix = mMat)
                    v1 = self.vertexShader(v1, modelMatrix = mMat)
                    v2 = self.vertexShader(v2, modelMatrix = mMat)
                    if verCount == 4:
                        v3 = self.vertexShader(v3, modelMatrix = mMat)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if verCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)
                
                vt0 = model.texcoords[face[0][1]-1]
                vt1 = model.texcoords[face[1][1]-1]
                vt2 = model.texcoords[face[2][1]-1]
                if verCount == 4:
                    vt3 =  model.texcoords[face[3][1]-1]
                textCoords.append(vt0)
                textCoords.append(vt1)
                textCoords.append(vt2)
                if verCount == 4:
                    textCoords.append(vt0)
                    textCoords.append(vt2)
                    textCoords.append(vt3)

        primitives = self.glPrimitiveAssemly(transformedVerts, textCoords)       

        for prim in primitives: 
            if self.primitiveType == TRIANGLES:
                self.glTriangle_bc(prim[0], prim[1], prim[2], 
                                   prim[3],prim[4],prim[5])


    def glFinish(self,filename):
        with open(filename,"wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height*3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

