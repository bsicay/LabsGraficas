from .mathLB import formatVector
import math

def vertex_shader(vertex, **kwargs):
    model_matrix = kwargs["model_matrix"]
    view_matrix = kwargs["view_matrix"]
    projection_matrix = kwargs["projection_matrix"]
    viewport_matrix = kwargs["viewport_matrix"]

    vt = formatVector([vertex[0], vertex[1], vertex[2], 1])
    vt = viewport_matrix * projection_matrix * view_matrix * model_matrix @ vt
    vt = formatVector([vt.data[0] / vt.data[3], vt.data[1] /
                 vt.data[3], vt.data[2] / vt.data[3]])

    return vt.data[:3]


def fragment_shader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]

    if texture is not None:
        color = texture.get_color(tex_coords[0], tex_coords[1])
    else:
        color = (1, 1, 1)

    return color

# carttonShader: 
def cartoonShader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]

    dot_size = 0.05  # Determina el tamaño de los puntos
    space_size = 0.01  # Determina el espacio entre los puntos

    # Calcula si estamos en un punto o en un espacio
    if texture is not None:
        color = texture.get_color(tex_coords[0][0], tex_coords[0][1])
    else:
        color = (1, 1, 1)  # Color del punto si no hay textura
    return color


def wrinkledNoise(u, v):
    frequency = 20  # que tan "apretadas" son las arrugas.
    amplitude = 30.5  # cuan "profundas" son las arrugas.

    value = math.sin(u * frequency) + math.sin(v * amplitude)

    return (value + 1) * 0.5  # Esto nos da un valor entre 0 y 1.


def wrinkledNoiseShader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]
    # print(tex_coords[0])
    # print(tex_coords[1])
    noise = wrinkledNoise(tex_coords[0][0], tex_coords[0][1])

    if texture is not None:
        original_color = texture.get_color(tex_coords[0][0], tex_coords[0][1])
        color = tuple(value * noise for value in original_color)
    else:
        color = (1 * noise, 1 * noise, 1 * noise)

    return color


def gradientShader(**kwargs):
    tex_coords = kwargs["tex_coords"]

    # Definimos dos colores para el degradado: inicio y final.
    start_color = (1, 0, 0)  # Rojo en la parte superior
    end_color = (0, 0, 1)    # Azul en la parte inferior

    # Interpolamos entre los dos colores basados en la coordenada 'v' 
    # de las coordenadas de textura (esto asume un rango de 0 a 1 para 'v').
    r = start_color[0] * (1 - tex_coords[0][1]) + end_color[0] * tex_coords[0][1]
    g = start_color[1] * (1 - tex_coords[0][1]) + end_color[1] * tex_coords[0][1]
    b = start_color[2] * (1 - tex_coords[0][1]) + end_color[2] * tex_coords[0][1]

    return (r, g, b)


def phong_shader(**kwargs):
    # Extracting values from kwargs
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    nA, nB, nC = kwargs["normals"]
    directional_light = kwargs["directional_light"]
    u, v, w = kwargs["barycentric_coords"]
    cam_matrix = kwargs["cam_matrix"]
    
    ambient_strength = 0.05
    specular_strength = 0.01
    shininess = 55

    cam_forward = formatVector(
        [cam_matrix.matx[0][2], cam_matrix.matx[1][2], cam_matrix.matx[2][2]])

    # Calculate interpolated texture coordinates and normal
    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        texture_color = texture.get_color(tU, tV)
    else:
        texture_color = (1, 1, 1)

    normal = formatVector([
        u * nA[0] + v * nB[0] + w * nC[0],
        u * nA[1] + v * nB[1] + w * nC[1],
        u * nA[2] + v * nB[2] + w * nC[2]
    ])

    # Ambient
    ambient = tuple(i * ambient_strength for i in texture_color)

    # Diffuse
    light_dir = formatVector(directional_light)
    diff = max(normal.dot(light_dir), 0)
    diffuse = tuple(i * diff for i in texture_color)

    # Specular
    reflect = 2 * normal.dot(light_dir) * normal - light_dir
    spec = pow(max(reflect.dot(cam_forward), 0), shininess)
    specular = tuple(specular_strength * spec for _ in texture_color)

    # Combine results to get final color
    final_color = tuple(
        min(1, max(0, a + d + s)) for a, d, s in zip(ambient, diffuse, specular)
    )
    return final_color
