# graphics_hw08
Graphics Homework 08: mdl-animation

# Members
| **Member** | **GitHub** |
|:----------:|:----------:|
| Ariel Levy | [`@askyel`] (https://github.com/askyel) |
| Dillon Zhang | [`@dillzhang`] (https://github.com/dillzhang) |

# How it Works
To run any `.mdl` file, simple enter `$ make file=<FILENAME>`

# Features
- All features submitted within [`Homework #8`](https://github.com/dillzhang/graphics_hw08)
- Scanline Conversion
- Z-buffering
- Flat Shading: Although the code can calculate flat shading, this does not work with `.mdl` files
  - Default values
    - Ambient reflection: 0.3
    - Diffuse reflection: 0.5
    - Specular reflection: 0.2
    - Ambient Red: 128
    - Ambient Green: 0
    - Ambient Blue: 0
    - Point Light Souces
      - Located at (0, 0, -250) with color value [255, 0, 0]
  - These can be changed either by supplying another parameter to `draw_flat_polygons()` in `draw.py` or changing the default values