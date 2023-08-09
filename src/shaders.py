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


def fragmentShader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]

    if texture is not None:
        color = texture.get_color(tex_coords[0], tex_coords[1])
    else:
        color = (1, 1, 1)

    return color