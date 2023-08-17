from .mathLB import formatVector
import math

def vertexShader(vertex, **kwargs):
    model_matrix = kwargs["model_matrix"]
    view_matrix = kwargs["view_matrix"]
    projection_matrix = kwargs["projection_matrix"]
    viewport_matrix = kwargs["viewport_matrix"]

    vt = formatVector([vertex[0], vertex[1], vertex[2], 1])
    vt = viewport_matrix * projection_matrix * view_matrix * model_matrix @ vt
    vt = formatVector([vt.data[0] / vt.data[3], vt.data[1] /
                 vt.data[3], vt.data[2] / vt.data[3]])

    return vt.data[:3]


def fragmentShader(**kwargs):
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
    # print(tex_coords[0][0])
    # print('a')
    # print(tex_coords[0][1])
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
