# Simulador de Optimización de Rutas (Proyecto Escolar)

Un script de Python que determina el itinerario de viaje óptimo para un viaje de 3 días, visitando 6 destinos más el Aeropuerto y el Hotel. El objetivo es **minimizar la distancia total recorrida** respetando una restricción de tiempo de **12 horas por día**.

Este proyecto fue desarrollado como parte de un proyecto académico, aplicando conceptos de optimización y algoritmos.

## 🚀 Contexto del Problema

El simulador debe planificar un itinerario de 3 días con las siguientes características:
* **Destinos a visitar:** Daikin Park, Museo de la Salud, NRG Stadium, NASA, Toyota Center, USS Texas Museum.
* **Puntos fijos:** Se inicia en el "Aeropuerto" (Día 1) y se duerme en el "Hotel" (Días 1 y 2). El viaje termina en el "Aeropuerto" (Día 3).
* **Restricción Fija:** La visita a la "NASA" debe ocurrir obligatoriamente en el Día 2, debido a su larga duración (8 horas).
* **Restricción de Tiempo:** Cada día, el tiempo total (viaje + visita) no puede exceder las 12 horas.

## ✨ Características Principales

* **Optimización de Distancia:** El script utiliza `itertools.permutations` para probar todas las combinaciones posibles de rutas para los días 1 y 3.
* **Validación de Tiempo:** Calcula el tiempo de viaje (asumiendo 60 km/h) más el tiempo de estancia en cada lugar, asegurando que no se exceda el límite diario.
* **Lógica de Itinerario Fijo:** Aísla la visita a la NASA en el Día 2 para reducir la complejidad de la búsqueda.
* **Reporte Detallado:** Imprime en consola un itinerario completo, desglosando los tiempos de viaje, tiempos de visita, distancia por día y el gran total.

## 🛠️ Tecnologías Utilizadas

* **Python 3**
* **NumPy:** Para almacenar y acceder eficientemente a la matriz de distancias.
* **itertools:** Para generar las permutaciones de las rutas.

## ⚙️ Cómo Usarlo

1.  Asegúrate de tener Python 3 instalado.
2.  Clona este repositorio:
    ```bash
    git clone [https://github.com/TU-USUARIO/simulador-optimizacion-rutas.git](https://github.com/TU-USUARIO/simulador-optimizacion-rutas.git)
    cd simulador-optimizacion-rutas
    ```
3.  (Recomendado) Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa: venv\Scripts\activate
    ```
4.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
5.  Ejecuta el script:
    ```bash
    python PiaCodigo EQ 11.py
    ```

## 📈 Posibles Mejoras a Futuro

Este proyecto utiliza un enfoque de permutación (fuerza bruta) que funciona para un número pequeño de destinos. Para escalar la solución, se podrían implementar:
* **Algoritmos Heurísticos:** Como un Algoritmo de Barrido (Sweep Algorithm) o un Algoritmo Genético para encontrar una solución "suficientemente buena" en menos tiempo.
* **Entrada de Datos Dinámica:** Cargar las ubicaciones, distancias y tiempos desde archivos externos (CSV, JSON) en lugar de tenerlos hardcodeados.
* **Interfaz Gráfica:** Usar una librería como `Tkinter` o `Streamlit` para visualizar las rutas y los resultados.