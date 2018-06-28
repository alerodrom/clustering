**_Resumen Automático de Vídeos mediante Clasificación_**

**Inteligencia Artificial 2017/18**

Desarrollado por **Alejandro Rodríguez Romero** y **José Manuel Lázaro Domínguez**.

Este proyecto esta desarollado en `Python3`. Para un buen funcionamiento del proyecto es necesario que se instalen los requisitos para ello pondremos en el terminal:

    pip3 install -r requirements.txt

Tras configurar el entorno pasaremos a configurar el proyecto para poderlo ejecutar. Accederemos al fichero `start.py` e indicamos los pámetros necesarios para ejutar el proyecto. Por defecto dejaremos un ejemplo: 

    my_clustering.start('media/video.mp4', 'input', 'output', 'frames_videos', 30, 15, [0, 256])

Explicación de los parámetros:

    Primer parámetro: Ruta del vídeo
    Segundo parámetro: Ruta donde se generarán los fotogramas del video
    Tercer parámetro: Ruta donde se añadirán los fotogramas clave del video
    Cuarto parámetro: Ruta donde se añadirán los fotogramas para generar el video resumen
    Quinto parámetro: T, Número de fotogramas a saltar
    Sexto parámetro: K, Número de grupos para k-means
    Séptimo parámetro: H, Tamaño del histográma generado
    
Para ejecutar el programa pondriamos lo siguiente:

    python3 start.py

Tras ejecutar el programa obtendríamos lo siguiente. En la `carpeta raiz` tendríamos el video resumen, en la carpeta `input` tendríamos los fotogramas del video, en `output` los fotogramas clave y en `frames_videos` estarán los fotogramas que se han usado para generar el vídeo.

Nota: Para volver a ejecutar las pruebas se deben de eliminar los fotogramas de las carpetas `input`, `output` y `frames_videos`.