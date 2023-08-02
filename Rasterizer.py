from gl import Renderer, V2, V3
import shaders
width = 1024
height = 1024

rend = Renderer(width,height)
rend.glPolygon([V2(165, 380), V2(185, 360), V2(180, 330), V2(207, 345), V2(233, 330), V2(230, 360), V2(250, 380), V2(220, 385), V2(205, 410), V2(193, 383)])

# Poligono 2
rend.glPolygon([V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)])

# Poligono 3
rend.glPolygon([V2(377, 249), V2(411, 197), V2(436, 249)])

# Poligono 4
rend.glPolygon([V2(413, 177), V2(448, 159), V2(502, 88), V2(553, 53), V2(535, 36), V2(676, 37), V2(660, 52), V2(750, 145), V2(761, 179), V2(672, 192), V2(659, 214), V2(615, 214), V2(632, 230), V2(580, 230), V2(597, 215), V2(552, 214), V2(517, 144), V2(466, 180)])

# Poligono 5
rend.glPolygon([V2(682, 175), V2(708, 120), V2(735, 148), V2(739, 170)]) 


vertices = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
# Poligono 2
vertices_poly2 = [(321, 335), (288, 286), (339, 251), (374, 302), (321, 335)]

# Poligono 3
vertices_poly3 = [(377, 249), (411, 197), (436, 249)]

# Poligono 4
vertices_poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), 
                  (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), 
                  (597, 215), (552, 214), (517, 144), (466, 180), (413, 177)]

# Poligono 5
vertices_poly5 = [(682, 175), (708, 120), (735, 148), (739, 170), (682, 175)]

my_color = 1,0,0
rend.scanline(vertices, 1,0,1)
rend.scanline(vertices_poly2, 0,1,1)
rend.scanline(vertices_poly3,0,0,1)
rend.scanline(vertices_poly4,1,1,1)
rend.scanline(vertices_poly5, 1,0,0)
rend.glRender()
rend.glFinish("output.bmp")
