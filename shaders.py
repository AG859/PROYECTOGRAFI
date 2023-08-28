import ml
import random
import math
import colorsys

def matrix_transform(matrix, vector):
    """
    Multiplica una matriz 4x4 por un vector 4x1.
    """
    result = [0, 0, 0, 0]
    
    for i in range(4):
        for j in range(4):
            result[i] += matrix[i][j] * vector[j]
            
    return result
def glitter_effect(value, threshold=0.95):
    """
    Simula el efecto de brillantina.
    Si el valor es mayor que el umbral, se intensifica el color.
    """
    if value > threshold:
        return 1.3  # Aumenta el valor del color para simular el brillo
    return 1

def thermal_color_map(intensity):
    """Convierte una intensidad de brillo en un color térmico."""
    if intensity < 0.25:
        return (0, 0, intensity * 4)  # Azul para frío
    elif intensity < 0.5:
        return (0, (intensity - 0.25) * 4, 1 - (intensity - 0.25) * 4)  # Transición de azul a verde
    elif intensity < 0.75:
        return ((intensity - 0.5) * 4, 1 - (intensity - 0.5) * 4, 0)  # Transición de verde a amarillo
    else:
        return (1, (1 - intensity) * 4, 0)  # Rojo para caliente
def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    vt = [vertex[0], vertex[1], vertex[2], 1]
    vt = matrix_transform(modelMatrix, vt)
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]
    return vt

def fragmentShader1(**kwargs):
    textCoords = kwargs["textCoords"]
    texture = kwargs["texture"]
    
    pixel_size = 32  

    # Pixelar las coordenadas de textura
    u_pixel, v_pixel = pixelate(textCoords[0], textCoords[1], pixel_size)
    
    # Usar las coordenadas pixeladas para obtener el color de la textura
    if texture:
        color = texture.getColor(u_pixel, v_pixel)
    else:
        # Si no hay textura, simplemente devolver un color sólido
        color = (0.5, 0.5, 0.5)

    return color

    

def dot_product(v1, v2):
    """ Calcula el producto punto de dos vectores """
    return sum(a*b for a, b in zip(v1, v2))
def fragmentShader2(**kwargs):
    textCoords = kwargs["textCoords"]

    # Colores base
    purple = (0.5, 0.0, 0.5)
    blue = (0.0, 0.0, 1.0)
    pink = (1.0, 0.5, 0.5)

    # Gradiente entre morado y azul basado en la coordenada y de la textura
    baseColor = (
        purple[0] * (1 - textCoords[1]) + blue[0] * textCoords[1],
        purple[1] * (1 - textCoords[1]) + blue[1] * textCoords[1],
        purple[2] * (1 - textCoords[1]) + blue[2] * textCoords[1],
    )

    # Añadir puntos rosados aleatoriamente
    sparkle_chance = 0.05
    if random.random() < sparkle_chance:
        baseColor = pink

    # Añadir efecto de resplandor

    shine_strength = 0.2
    distance_to_perfect_reflection = abs(textCoords[1] - 0.5)
    shine = 1 - min(distance_to_perfect_reflection / 0.5, 1)
    
    baseColor = (
        baseColor[0] + shine_strength * shine,
        baseColor[1] + shine_strength * shine,
        baseColor[2] + shine_strength * shine
    )

    # Normalizar colores
    baseColor = (
        min(1.0, baseColor[0]),
        min(1.0, baseColor[1]),
        min(1.0, baseColor[2])
    )

    return baseColor


def fragmentShader3(**kwargs):
    textCoords = kwargs["textCoords"]
    texture = kwargs.get("texture", None)
    

    if texture:
        color = texture.getColor(textCoords[0], textCoords[1])
        
        # Convertimos el valor de brillo del color a una intensidad
        intensity = sum(color) / 3.0
    else:
        # Si no hay textura, se toma la intensidad basándonose en una variación de coordenadas
        intensity = 0.5 + (math.sin(textCoords[0] * 10) + math.cos(textCoords[1] * 10)) / 4


    thermal_color = thermal_color_map(intensity)

    return thermal_color\
    


def pixelate(u, v, pixel_size):
    u_pixel = int(u * pixel_size) / float(pixel_size)
    v_pixel = int(v * pixel_size) / float(pixel_size)
    return u_pixel, v_pixel



def fragmentShader4(**kwargs):
    textCoords = kwargs["textCoords"]
    texture = kwargs["texture"]

    # Si no hay una textura, devuelve blanco
    if not texture:
        return (1, 1, 1)

    # Definir la cantidad de desenfoque
    blur_amount = 0.01  

    # Tomar muestras alrededor de la coordenada actual para el desenfoque
    offsets = [
        (-blur_amount, -blur_amount), (0, -blur_amount), (blur_amount, -blur_amount),
        (-blur_amount, 0), (0, 0), (blur_amount, 0),
        (-blur_amount, blur_amount), (0, blur_amount), (blur_amount, blur_amount)
    ]
    
    # Calcular el promedio de los colores de las muestras
    r, g, b = 0, 0, 0
    valid_samples = 0
    for offset in offsets:
        sampled_color = texture.getColor(textCoords[0] + offset[0], textCoords[1] + offset[1])
        
        # Comprobar si el color muestreado es válido
        if sampled_color is not None:
            r += sampled_color[0]
            g += sampled_color[1]
            b += sampled_color[2]
            valid_samples += 1
    
    # Evita la división por cero
    if valid_samples == 0:
        return (1, 1, 1)  # Devuelve blanco si no hay muestras válidas

    r /= valid_samples
    g /= valid_samples
    b /= valid_samples
    
    return (r, g, b)