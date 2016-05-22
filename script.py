import mdl
import sys
from display import *
from matrix import *
from draw import *


def first_pass(commands):
    num_frames = None
    basename = None
    for command in commands:
        if command[0] == "frames":
            if num_frames is None:
                num_frames = command[1]
            else:
                print "ERROR: Too many calls of 'frames'"
                sys.exit(0)
        elif command[0] == "basename":
            if basename is None:
                basename = command[1]
            else:
                print "ERROR: Too many calls of 'basename'"
                sys.exit(0)
        elif command[0] == "vary":
            if num_frames is None:
                print "Please declare number of frames before vary"
                sys.exit(0)
            for i in range(2, 4):
                if command[i] < 0 or round(command[i]) != command[i] or command[i] > num_frames:
                    print "Invalid vary command"
                    sys.exit(0)
    if num_frames is not None and basename is None:
        basename = "base"
        print "WARNING: No basename provided. Defaulted to " + basename
    return [num_frames, basename]


def calculate_vary(x, x0, x1, y0, y1):
    m = (y1 - y0) / float(x1 - x0)
    return m * (x - x0) + y0


def second_pass(commands, num_frames):
    varies = []
    frame_values = []
    for i in range(num_frames):
        current_dict = {}
        for command in commands:
            if command[0] == 'vary' and command[2] <= i and i <= command[3]:
                variable = command[1]
                if variable not in varies:
                    varies.append(variable)
                current_dict[variable] = calculate_vary(i, command[2], command[3], command[4], command[5])
        for change in varies:
            if change not in current_dict:
                current_dict[change] = frame_values[-1][change]
        frame_values.append(current_dict)
    for change in varies:
        for i in range(num_frames)[::-1]:
            if change not in frame_values[i]:
                frame_values[i][change] = frame_values[i + 1][change]
    return frame_values


def run(filename):
    color = [255, 255, 255]
    tmp = new_matrix()
    ident(tmp)
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    
    animation_values = first_pass(commands)
    isAnimated = True
    frame_values = []
    if animation_values[0] is None:
        animation_values[0] = 1
        isAnimated = False
    else:
        frame_values = second_pass(commands, animation_values[0])
    for i in range(animation_values[0]):
        screen = new_screen()
        z_buffer = new_screen(XRES, YRES, [None])
        stack = [tmp]
        print "Frame %04d" % i
        for command in commands:
            if command[0] == "pop":
                stack.pop()
                if not stack:
                    stack = [tmp]
            if command[0] == "push":
                stack.append(stack[-1][:])
            if command[0] == "save":
                save_extension(screen, command[1])
            if command[0] == "display":
                display(screen)
            if command[0] == "sphere":
                m = []
                add_sphere(m, command[1], command[2], command[3], command[4], 5)
                matrix_mult(stack[-1], m)
                draw_polygons(m, screen, z_buffer, color)
            if command[0] == "torus":
                m = []
                add_torus(m, command[1], command[2], command[3], command[4], command[5], 5)
                matrix_mult(stack[-1], m)
                draw_polygons( m, screen, z_buffer, color )
            if command[0] == "box":
                m = []
                add_box(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_polygons( m, screen, z_buffer, color )
            if command[0] == "line":
                m = []
                add_edge(m, *command[1:])
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, z_buffer, color )
            if command[0] == "bezier":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'bezier')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, z_buffer, color )
            if command[0] == "hermite":
                m = []
                add_curve(m, command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8], .05, 'hermite')
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, z_buffer, color )
            if command[0] == "circle":
                m = []
                add_circle(m, command[1], command[2], command[3], command[4], .05)
                matrix_mult(stack[-1], m)
                draw_lines( m, screen, color )
            if command[0] in ["move", "scale", "rotate"]:
                factor = 1
                if command[-1]:
                    factor = frame_values[i][command[-1]]
                t = new_matrix()
                if command[0] == "move":                
                    xval = command[1] * factor
                    yval = command[2] * factor
                    zval = command[3] * factor
                    t = make_translate(xval, yval, zval)
                if command[0] == "scale":
                    xval = command[1] * factor
                    yval = command[2] * factor
                    zval = command[3] * factor
                    t = make_scale(xval, yval, zval)
                if command[0] == "rotate":
                    angle = command[2] * (math.pi / 180) * factor
                    if command[1] == 'x':
                        t = make_rotX( angle )
                    elif command[1] == 'y':
                        t = make_rotY( angle )
                    elif command[1] == 'z':
                        t = make_rotZ( angle )            
                matrix_mult( stack[-1], t )
                stack[-1] = t
        if isAnimated:
            save_extension(screen, "anim/" + animation_values[1] + "%04d.png" % i)
