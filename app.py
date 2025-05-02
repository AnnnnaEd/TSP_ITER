import math
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # Cierra el ciclo
    return total

def i_hill_climbing(coord):
    ruta = list(coord.keys())
    mejor_ruta = ruta[:]
    max_iteraciones = 10

    while max_iteraciones > 0:
        mejora = True
        random.shuffle(ruta)

        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta, coord)

            for i in range(len(ruta)):
                if mejora:
                    break
                for j in range(len(ruta)):
                    if i != j:
                        ruta_tmp = ruta[:]
                        ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]

                        dist = evalua_ruta(ruta_tmp, coord)
                        if dist < dist_actual:
                            mejora = True
                            ruta = ruta_tmp[:]
                            break
        
        max_iteraciones -= 1

        if evalua_ruta(ruta, coord) < evalua_ruta(mejor_ruta, coord):
            mejor_ruta = ruta[:]

    return mejor_ruta, evalua_ruta(mejor_ruta, coord)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ruta')
def obtener_ruta():
    coord = {
        'Jiloyork': (19.916012, -99.580580),
        'Toluca': (19.289165, -99.655697),
        'Atlacomulco': (19.799520, -99.873844),
        'Guadalajara': (20.677754, -103.346253),
        'Monterrey': (25.691611, -100.321838),
        'QuintanaRoo': (21.163111, -86.802315),
        'Michoacan': (19.701400, -101.208296),
        'Aguascalientes': (21.876410, -102.264386),
        'CDMX': (19.432713, -99.133183),
        'QRO': (20.597194, -100.386670)
    }
    
    mejor_ruta, distancia_total = i_hill_climbing(coord)
    
    return jsonify({
        "mejor_ruta": mejor_ruta,
        "distancia_total": distancia_total
    })

if __name__ == '__main__':
    app.run(debug=True)
