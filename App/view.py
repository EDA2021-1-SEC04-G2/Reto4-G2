"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cantidad componentes conectados")
    print("3- Landing Points de interconexión")
    print("4- Ruta mínima entre dos países")
    print("5- Identificar estructura crítica")
    print("6- Impacto de un Landing Point dañado")



    
 


analyzer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer=controller.init_analyzer()
        controller.load_data(analyzer)
        numedges = controller.total_edges(analyzer)
        numvertex = controller.total_vertices(analyzer)
        numcountries=controller.total_countries(analyzer)
        numlanding=controller.total_landing_points(analyzer)
        print('Numero de vertices: ' + str(numvertex))
        print('Numero de arcos: ' + str(numedges))
        print('Numero de paises: ',numcountries)
        print('Numero de landing_points: ',numlanding)
    elif int(inputs[0]) == 2:
        verta=input('vertice a')
        vertb=input('vertice b')
        ans=controller.connected_components(analyzer,verta,vertb)
        print('El número de componentes conectados es: ' +
          str(ans[0]))
        print('Los dos vertices están conectados',ans[1])
    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        pass

    else:
        sys.exit(0)
sys.exit(0)
