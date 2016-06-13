def calculate_normal( ax, ay, az, bx, by, bz ):
    normal = [0,0,0]
    normal[0] = ay * bz - az * by
    normal[1] = az * bx - ax * bz
    normal[2] = ax * by - ay * bx
    return normal


def calculate_dot(points, i, vector=[0, 0, -1], normalize=False):
    #get as and bs to calculate the normal
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )

    #set up the view vector values
    vx = vector[0]
    vy = vector[1]
    vz = vector[2]
    
    #calculate the dot product
    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz

    if normalize:
        dot = dot / (magnitude(normal) * magnitude(vector))
    return dot


def magnitude(vector):
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**(.5)


def dot_poduct(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]


def normalize(vector):
    vectorprime = vector[:]
    for i in range(len(vectorprime)):
        vectorprime[i] /= magnitude(vectorprime)
    return vectorprime
        

def get_normal(points, i=0):
    ax = points[i + 1][0] - points[i][0]
    ay = points[i + 1][1] - points[i][1]
    az = points[i + 1][2] - points[i][2]
    bx = points[i + 2][0] - points[i][0]
    by = points[i + 2][1] - points[i][1]
    bz = points[i + 2][2] - points[i][2]
    normal = calculate_normal(ax, ay, az, bx, by, bz)
    return normal


def sub_vector(v1, v2):
    vR = [0, 0, 0]
    for i in range(3):
        vR[i] = v1[i] - v2[i]
    return vR


def scalar_mult(v1, scalar):
    vR = [0, 0, 0]
    for i in range(3):
        vR[i] = v1[i] * scalar
    return vR
