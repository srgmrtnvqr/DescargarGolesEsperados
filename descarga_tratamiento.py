import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# DESCARGA DE LOS DATOS
def obtener_datos_partido(enlace):    # Función que devuelve un diccionario con los tiros del partido
    respuesta = requests.get(enlace)    # Petición realizada a la web
    sopa = BeautifulSoup(respuesta.text, 'lxml')    # Contenido de la página
    scripts = sopa.find_all('script') 
    cadena = scripts[1].string # En el segundo script es donde se encuentran los datos que nos interesan
    codificar = cadena.encode('utf8').decode('unicode_escape') # Para ver como se disponen los datos del texto con claridad
    inicio = codificar.index("('") + 2 
    final = codificar.index("')") 
    datos = codificar[inicio:final]    # Eliminar los caracteres anteriores y posteriores a los datos
    datos = json.loads(datos)   # Convertir a json para realizar la extracción de los datos
    return datos

# TRATAMIENTO DE LOS DATOS
def datos_equipo(dicc_ligas, liga, jornada, temporada, datos, localia):  # Función que devuelve un dataframe con los tiros de un equipo
    # Para crear un ID del partido
    equipo_local = datos['h'][0]['h_team']  
    equipo_visitante = datos['a'][0]['a_team']  
    # Listas para almacenar los datos correspondientes
    minuto = []
    equipo = []
    localias = []
    xg = []
    jugador = []
    zona_contacto = []
    resultado = []
    x = []
    y = []
    situacion = []
    asistente = []
    accion_anterior = []
    for indice in range(len(localia)):
        for clave in localia[indice]:
            if clave == 'h_a': 
                if localia[indice][clave] == 'h':
                    equipo.append(localia[indice]['h_team'])
                    localias.append('local')
                else:
                    equipo.append(localia[indice]['a_team'])
                    localias.append('visitante')
            elif clave == 'minute':
                minuto.append(int(localia[indice][clave]))
            elif clave == 'xG':
                xg.append(float(localia[indice][clave]))
            elif clave == 'player':
                jugador.append(localia[indice][clave])
            elif clave == 'shotType':
                zona_contacto.append(localia[indice][clave])
            elif clave == 'result':
                resultado.append(localia[indice][clave])
            elif clave == 'X':
                x.append(localia[indice][clave])
            elif clave == 'Y':
                y.append(localia[indice][clave])
            elif clave == 'situation':
                situacion.append(localia[indice][clave])
            elif clave == 'player_assisted':
                asistente.append(localia[indice][clave])
            elif clave == 'lastAction':
                accion_anterior.append(localia[indice][clave]) 
            else: pass  # Fin del bucle FOR
    columnas = ['jugador','equipo','localia','minuto','xg','zona_contacto','resultado','x','y','situacion','asistente','accion_anterior']
    df = pd.DataFrame([jugador,equipo,localias,minuto,xg,zona_contacto,resultado,x,y,situacion,asistente,accion_anterior],index=columnas)
    df = df.T
    id = dicc_ligas[liga] + '_' + jornada + '_' + temporada + '_' + equipo_local + '-' + equipo_visitante
    df['id'] = id
    df['partido'] = equipo_local + '-' + equipo_visitante
    return df

def traducir_tiros(datos, dicc_ligas, liga, jornada, temporada):  # Función que devuelve los tiros traducidos al español
    # Se llama a la función para que nos de los dataframes de los dos equipos
    datos_local = datos['h']    
    datos_visitante = datos['a']
    df_local = datos_equipo(dicc_ligas, liga, jornada, temporada, datos, datos_local)
    df_visitante = datos_equipo(dicc_ligas, liga, jornada, temporada, datos, datos_visitante)
    # Más tratamiento de datos
    df_equipos = pd.concat([df_local, df_visitante]).reset_index(drop=True)
    # Se podrían traducir los datos al español
    df_equipos.loc[df_equipos.zona_contacto == 'RightFoot', 'zona_contacto'] = 'Pierna derecha' 
    df_equipos.loc[df_equipos.zona_contacto == 'LeftFoot', 'zona_contacto'] = 'Pierna izquierda'
    df_equipos.loc[df_equipos.zona_contacto == 'Head', 'zona_contacto'] = 'Cabeza'
    df_equipos.loc[df_equipos.zona_contacto == 'OtherBodyPart', 'zona_contacto'] = 'Otra parte del cuerpo'
    # Resultado del tiro
    df_equipos.loc[df_equipos.resultado == 'MissedShots', 'resultado'] = 'Tiro fuera' 
    df_equipos.loc[df_equipos.resultado == 'SavedShot', 'resultado'] = 'Tiro a porteria'
    df_equipos.loc[df_equipos.resultado == 'BlockedShot', 'resultado'] = 'Tiro bloqueado'
    df_equipos.loc[df_equipos.resultado == 'ShotOnPost', 'resultado'] = 'Tiro al palo'
    df_equipos.loc[df_equipos.resultado == 'Goal', 'resultado'] = 'Gol' 
    df_equipos.loc[df_equipos.resultado == 'OwnGoal', 'resultado'] = 'Gol en propia'
    # Tipo de jugada
    df_equipos.loc[df_equipos.situacion == 'OpenPlay', 'situacion'] = 'Juego abierto'
    df_equipos.loc[df_equipos.situacion == 'FromCorner', 'situacion'] = 'Remate de corner'
    df_equipos.loc[df_equipos.situacion == 'DirectFreekick', 'situacion'] = 'Falta directa'
    df_equipos.loc[df_equipos.situacion == 'SetPiece', 'situacion'] = 'Balon parado' 
    df_equipos.loc[df_equipos.situacion == 'Penalty', 'situacion'] = 'Penalti'
    df_equipos.loc[df_equipos.situacion == 'CounterAttack', 'situacion'] = 'Contraataque'
    # Acción previa al tiro
    df_equipos.loc[df_equipos.accion_anterior == 'Aerial', 'accion_anterior'] = 'Aereo' 
    df_equipos.loc[df_equipos.accion_anterior == 'Cross', 'accion_anterior'] = 'Centro'
    df_equipos.loc[df_equipos.accion_anterior == 'CornerAwarded', 'accion_anterior'] = 'Corner concedido'
    df_equipos.loc[df_equipos.accion_anterior == 'LayOff', 'accion_anterior'] = 'Dejada'
    df_equipos.loc[df_equipos.accion_anterior == 'Clearance', 'accion_anterior'] = 'Despeje'
    df_equipos.loc[df_equipos.accion_anterior == 'Challenge', 'accion_anterior'] = 'Duelo'
    df_equipos.loc[df_equipos.accion_anterior == 'Tackle', 'accion_anterior'] = 'Entrada'
    df_equipos.loc[df_equipos.accion_anterior == 'Chipped', 'accion_anterior'] = 'Pase elevado'
    df_equipos.loc[df_equipos.accion_anterior == 'Standard', 'accion_anterior'] = 'Estandar'
    df_equipos.loc[df_equipos.accion_anterior == 'Foul', 'accion_anterior'] = 'Falta'
    df_equipos.loc[df_equipos.accion_anterior == 'GoodSkill', 'accion_anterior'] = 'Filigrana'
    df_equipos.loc[df_equipos.accion_anterior == 'OffsideProvoked', 'accion_anterior'] = 'Fuera de juego provocado'
    df_equipos.loc[df_equipos.accion_anterior == 'Interception', 'accion_anterior'] = 'Interceptacion'
    df_equipos.loc[df_equipos.accion_anterior == 'BlockedPass', 'accion_anterior'] = 'Pase bloqueado'
    df_equipos.loc[df_equipos.accion_anterior == 'Pass', 'accion_anterior'] = 'Pase'
    df_equipos.loc[df_equipos.accion_anterior == 'Throughball', 'accion_anterior'] = 'Pase en profundidad'
    df_equipos.loc[df_equipos.accion_anterior == 'HeadPass', 'accion_anterior'] = 'Pase de cabeza'
    df_equipos.loc[df_equipos.accion_anterior == 'Dispossessed', 'accion_anterior'] = 'Perdida'
    df_equipos.loc[df_equipos.accion_anterior == 'Rebound', 'accion_anterior'] = 'Rechace'
    df_equipos.loc[df_equipos.accion_anterior == 'TakeOn', 'accion_anterior'] = 'Regate'
    df_equipos.loc[df_equipos.accion_anterior == 'BallRecovery', 'accion_anterior'] = 'Recuperacion'
    df_equipos.loc[df_equipos.accion_anterior == 'BallTouch', 'accion_anterior'] = 'Toque'
    df_equipos.loc[df_equipos.accion_anterior == 'None', 'accion_anterior'] = ''
    return df_equipos