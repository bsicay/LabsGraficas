from .mathLB import formatVector


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


# def fragmentShader(**kwargs):
#     tex_coords = kwargs["tex_coords"]
#     texture = kwargs["texture"]

#     if texture is not None:
#         color = texture.get_color(tex_coords[0], tex_coords[1])
#     else:
#         color = (1, 1, 1)

#     return color


# dottedShader: 
def fragmentShader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]

    dot_size = 0.05  # Determina el tamaño de los puntos
    space_size = 0.01  # Determina el espacio entre los puntos

    # Calcula si estamos en un punto o en un espacio
    if (tex_coords[0] % (dot_size + space_size) < dot_size) and (tex_coords[1] % (dot_size + space_size) < dot_size):
        # Estamos en un punto
        if texture is not None:
            color = texture.get_color(tex_coords[0], tex_coords[1])
        else:
            color = (0, 0, 0)  # Color del punto si no hay textura
    else:
        color = (63/255,64/255,53/255)  # Color del espacio entre puntos

    return color
