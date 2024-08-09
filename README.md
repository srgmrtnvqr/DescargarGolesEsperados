<h1 align="center">Descargar los tiros realizados en un partido</h1>
<p align="center"><img src="https://raw.githubusercontent.com/srgmrtnvqr/DescargarGolesEsperados/main/xg_partido.jpg"/></p> 

- Lenguaje utilizado: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

## Índice:
---

- [Descripción](#descripción)
- [Guía de usuario](#guía-de-usuario)
- [Dependencias](#dependencias)
- [Autor/es](#autores)


## Descripción
---
Este repositorio contiene el código para descargar los tiros de cualquier partido en la página www.understat.com 

Las ligas incluidas en esta web son: Premier League, La Liga, Bundesliga, Serie A, League 1 y Premier League Rusa.
Los datos descargados son copiados en un Excel para su posterior análisis.

## Guía de usuario
---
Pasos a seguir para descargar los goles esperados de un partido.

- Primero tienes que ejecutar la primera celda de código, que sirve para la descarga del partido, el tratamiento de los datos y la representación en un gráfico.
  ```
  import descarga_tratamiento
  import pandas as pd
  import matplotlib.pyplot as plt
  ```
  
- Después, tienes que ejecutar la primera celda de código de `` # Selección del partido para descargar ``.
  
- Al ejecutar la siguiente celda, tendrás que escribir con el teclado la liga, la temporada y la jornada que corresponden al partido que quieres descargar.
  ```
  # Para descargar un partido de La Liga 
  while True:
      liga = str(input('¿Qué Liga es?: ')).upper()    #ESP
      if liga in dicc_ligas:
          break
      else:
          print('Introduce una liga disponible')
  temporada = str(input('¿Qué temporada es?: '))  #23-24
  jornada = str(input('¿Qué jornada es?: '))  #37
  ```

  Este es un ejemplo para descargar el Almería - Getafe de la jornada 33 de la temporada 23-24.
  ``
    - Cuando ejecutes la celda de código aparecerá la primera pregunta: ¿Qué Liga es?
      La respuesta es ESP
    - La pregunta que aparecerá después es: ¿Qué temporada es?
      La respuesta es 23-24
    - Para finalizar aparecerá la última pregunta: ¿Qué jornada es?
      La respuesta es 33
      
- La última celda de código de este apartado sirve para introducir el id correspondiente al partido. Este id aparece en la página web " https://understat.com/match/' + partido ", donde partido es el id correspondiente.
``` partido = str(input('¿Cuál es el ID del partido que quieres descargar: '))
  enlace = 'https://understat.com/match/' + partido
```
`` Para el partido del ejemplo anterior el id que hay que introducir es el siguiente: 23005 ``

## Dependencias
---
Las librerías necesarias para la ejecución del código son: 
- requests
- BeautifulSoup
- json
- pandas

## Autor/es
---
Sergio Martín Vaquero
