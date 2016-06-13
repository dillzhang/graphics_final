from gmath import *


def return_center(triplet):
    center = [0, 0, 0]
    for x in range(3):
        for y in range(3):
            center[x] += triplet[y][x]
            center[x] = center[x] / 3
    return center


def return_ambient(ambient_light, ambient_properties):
    ambient = [0, 0, 0]
    for i in range(3):
        ambient[i] = ambient_light[i] * ambient_properties
    return ambient

    
def return_diffuse(point_lights, diffuse_properties, center, points):
    diffuse = [0, 0, 0]
    for i in range(3):
        total_light = 0
        for light in point_lights:
            view_vector = [light[0] - center[0],
                           light[1] - center[1],
                           light[2] - center[2]]
            cos = calculate_dot(points, 0, view_vector, True)
            if cos < 0:
                cos = 0
            total_light += light[3 + i] * diffuse_properties * cos
        if total_light < 0:
            total_light = 0
        diffuse[i] = total_light
    return diffuse


def return_specular(point_lights, specular_properties, center, points, v_vector=[0, 0, -1]):
    specular = [0, 0, 0]
    for i in range(3):
        total_light = 0
        for light in point_lights:
            l_vector = [light[0] - center[0],
                        light[1] - center[1],
                        light[2] - center[2]]
            l_norm = normalize(l_vector)
            n_vector = get_normal(points)
            n_norm = normalize(n_vector)
            v_norm = normalize(v_vector)
            l_dot_n = dot_poduct(l_norm, n_norm)
            r_norm = scalar_mult(n_norm, 2 * l_dot_n)
            r_minus_l = sub_vector(r_norm, l_norm)
            cos = dot_poduct(r_minus_l, v_norm)
            if cos < 0:
                cos = 0
            total_light += light[3 + i] * specular_properties * cos**2
        if total_light < 0:
            total_light = 0
        specular[i] = total_light
    return specular


def return_color(ambient, diffuse, specular):
    color = [0, 0, 0]
    #print ambient, diffuse, specular
    for i in range(3):
        color[i] = int(ambient[i] + diffuse[i] + specular[i])
        if color[i] < 0:
            color[i] = 0
        if color[i] > 255:
            color[i] = 255
    # print color
    return color
