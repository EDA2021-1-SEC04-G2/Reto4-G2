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
import model
from DISClib.ADT import map as m
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

def print_results_req1(ans):
    print('---RESULTADOS REQ. 1---')
    print('El número de componentes conectados es: ' + str(ans[0]))
    if ans[1]:
        x='SI'
    else:
        x='NO'
    print('Los dos landing points',x,'están en el mismo cluster')


def print_results_req2(ans):
    print('---RESULTADOS REQ. 2---')
    print('Los landing points que más cables conectan son: ')
    print('\n')
    i=1
    while i<=10:
        entry=lt.getElement(ans,i)
        print('Nombre:',entry[0],', País:',entry[1],', Identificador:',entry[2],' conecta',entry[3],'cables')
        i+=1

def print_results_req3(ans,pais1,pais2):
    print('---RESULTADOS REQ. 3---')
    if ans[0] is None:
        print('No hay camino entre',pais1,'y',pais2)
    else:
        print('El camino más corto entre',pais1,'y',pais2,'tiene una distancia total de',
               round(ans[1],2),'km','y es el siguiente: ')
        for entry in lt.iterator(ans[0]):
            print(entry[0],'-',entry[1],'con distancia',round(entry[2],2),'km')

def print_results_req4(ans):
    print('---RESULTADOS REQ. 4---')
    print('En el MST hay un total de',ans[0],'vertices')
    print('La longitud total del MST es',ans[1],'km')
    print('La conexión más corta en el MST es',ans[2][0],'-',ans[2][1],'con longitud',ans[2][2],'km')
    print('La conexión más larga en el MST es',ans[3][0],'-',ans[3][1],'con longitud',ans[3][2],'km')

def print_results_req5(ans,landing):
    print('---RESULTADOS REQ. 5---')
    print('Si fallara el landing point',landing,'se verían afectados',ans[0],'paises (incluyendo el local)')
    print('Los países afectados son: ')
    for entry in lt.iterator(ans[1]):
        print('El país',entry[0],'y está a una distancia de',entry[1],'km del landing point de',landing)



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
        landing1=input('Landing point 1: ')
        landing2=input('Landing point 2: ')
        ans=controller.connected_components(analyzer,landing1,landing2)
        print_results_req1(ans[0])
        print(ans[1],'[ms]',ans[2],'[kb]')
    elif int(inputs[0]) == 3:
        ans=controller.critical_landing_points(analyzer)
        print_results_req2(ans[0])
        print(ans[1],'[ms]',ans[2],'[kb]')
    elif int(inputs[0]) == 4:
        pais1=input('País de origen: ' )
        pais2=input('País destino: ' )
        ans=controller.minimum_path(analyzer,pais1,pais2)
        print_results_req3(ans[0],pais1,pais2)
        print(ans[1],'[ms]',ans[2],'[kb]')
    elif int(inputs[0]) == 5:
        ans=controller.MST(analyzer)
        print_results_req4(ans[0])
        print(ans[1],'[ms]',ans[2],'[kb]')
    elif int(inputs[0]) == 6:
        landing_name=input('Landing point: ')
        ans=controller.countries_to_landing_point(analyzer,landing_name)
        print_results_req5(ans[0],landing_name)
        print(ans[1],'[ms]',ans[2],'[kb]')
    else:
        sys.exit(0)
sys.exit(0)

