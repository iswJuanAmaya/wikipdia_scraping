Prueba de Automatización: Extracción de Datos de Wikipedia usando Python y Selenium
------------------------------------------------------------------------------------
Juan Cristobal Garcia amaya (JC)
06/03/2024
prueba para: AI27


El script pipeline.py es un "orquestador" que dada una url de wikipedia va
y extrae sus tablas(especificadas por titulo de parrafo) y las guarda como
un archivo excel(.xlsx), adicionalmente se puede ir visitando cada uno
de los anexos(links) que la tabla presente en una sola de sus columnas.


para correr el proyecto actualmente solo se ocupa tener instaladas las dependencias
listadas abajo y ejecutar el script pipeline, eg.
    .\venv\Scripts\activate           #Enciende el entorno virtual
    python pipeline.py                #correo el robot

nota: el script corre con chrome por defecto, si se quiere utilizar Firefox
se le debe pasar False a la funcion set_driver() que se llama desde el metodo 
main()


dependencias:
------------
    -este proyecto fue contruido con python3.9
    -las librerías necesarias están en requirements.txt
        se sugiere crear un entorno virtual y utilizar el comando 
        python -r requirements.txt
        para instalar recursivamente todas las librerias/dependencias 
        necesarias para que el robot funcione
    -Tener el navegador chrome o Firefox instalados


Deuda Técnica:
--------------

Lo primero que hice fue analizar el proyecto, los requerimientos funcionales y no funcionales,
planear la lógica así como los pasos, dado la limitancia del tiempo y/o de mis capacidades
opté por un modelo de desarrollo evolutivo o en espiral, dónde se creará un MVP según el nivel
de priorización y según fuera avanzando el desarrollo ir iterando para madurar este MVP,
dadas estás limitaciones y habiendo prorizado algunos requerimientos estas son algunas de las deudas 
técnicas.

1) - Automatizar la creación de una cuenta en Wikipedia (Opcional, pero con valor adicional).*1
2) - Estructura de Clases*2

*1 Por temas de tiempo decidí dejar la automatización de creación como último desarrollo dado que 
   solicita captcha y sabía que me podía tomar bastante tiempo, y al ser opcional lo segregué como
   la última de las prioridades.

*2 Aunque puse un fuerte enfoque en la modularidad y reusabilidad, por temas de tiempo y de que
   honestamente mis habilidades entorno al paradigma de programación orientada a objetos están 
   muy "oxidadas"*3 no alcancé a dedicarle tiempo a crear modulos ni clases, sin embargo si dediqué 
   tiempo a crear funciones y tratar de que fueran lo más reutilizables posible dados
   diferentes contextos.

*3 Yo aprendí a programar en python en una clase dedicada a este paradigma, sin embargo no se me
   ha dado la oportunidad de trabajar con el PPO desde hace ya mucho.

*4 Si tuviera más tiempo se lo dedicaría a generar más abstracciones lógicas para mejorar
   la escalabilidad, la modularidad y reusabilidad de mi código. 

    
