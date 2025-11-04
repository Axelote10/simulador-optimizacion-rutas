"""
Simulador de Optimización de Rutas para un Itinerario de 3 Días

Este script calcula la ruta óptima para un viaje de 3 días visitando 6 destinos
en Houston, TX, minimizando la distancia total recorrida y respetando un
límite de tiempo diario de 12 horas.

El itinerario tiene puntos fijos:
- Día 1: Aeropuerto -> Lugares -> Hotel
- Día 2: Hotel -> NASA -> Hotel (NASA es fija por su duración)
- Día 3: Hotel -> Lugares -> Aeropuerto
"""

import numpy as np
from itertools import permutations

# --- DATOS GLOBALES ---

# Matriz de distancias (km)
DISTANCES_KM = np.array([
    [0, 30, 25, 35, 40, 32, 45, 35],
    [30, 0, 12, 18, 45, 15, 35, 5],
    [25, 12, 0, 8, 42, 5, 38, 2],
    [35, 18, 8, 0, 40, 3, 39, 5],
    [40, 45, 42, 40, 0, 38, 20, 35],
    [32, 15, 5, 3, 38, 0, 36, 1],
    [45, 35, 38, 39, 20, 36, 0, 30],
    [35, 5, 2, 5, 35, 1, 30, 0]
])

# Tiempo de visita en cada lugar (horas)
TIMES_AT_LOCATION = np.array([2, 3, 3, 5, 8, 2, 3, 1])  # horas

# Nombres de las ubicaciones (corresponden a los índices de las matrices)
LOCATIONS = ["Aeropuerto", "Daikin Park", "Museo de la Salud", "NRG Stadium",
             "NASA", "Toyota Center", "USS Texas Museum", "Hotel"]

# --- CONSTANTES DE CONFIGURACIÓN ---
MAX_TIME_PER_DAY = 12  # Horas
VELOCIDAD_PROMEDIO_KMH = 60  # Asumimos 60 km/h para convertir distancia a tiempo

# --- FUNCIONES AUXILIARES ---

def get_location_index(loc_name):
    """Obtiene el índice de una ubicación a partir de su nombre."""
    return LOCATIONS.index(loc_name)

def calculate_route_time(route):
    """
    Calcula el tiempo total de una ruta (viaje + visita).
    
    Argumentos:
        route (list[int]): Una lista de índices de ubicación en orden.
        
    Devuelve:
        float: El tiempo total en horas.
    """
    total_time = 0
    for i in range(len(route) - 1):
        idx_from = route[i]
        idx_to = route[i+1]
        
        # Tiempo de viaje (distancia / velocidad)
        travel_time = DISTANCES_KM[idx_from, idx_to] / VELOCIDAD_PROMEDIO_KMH
        total_time += travel_time
        
        # Tiempo en el destino (se suma el tiempo del siguiente punto)
        total_time += TIMES_AT_LOCATION[idx_to]
        
    return total_time

def calculate_route_distance(route):
    """
    Calcula la distancia total de una ruta.
    
    Argumentos:
        route (list[int]): Una lista de índices de ubicación en orden.
        
    Devuelve:
        float: La distancia total en km.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        idx_from = route[i]
        idx_to = route[i+1]
        total_distance += DISTANCES_KM[idx_from, idx_to]
    return total_distance

# --- LÓGICA PRINCIPAL DE OPTIMIZACIÓN ---

def find_best_routes():
    """
    Encuentra la mejor distribución de rutas para los 3 días.
    
    Este es el núcleo del optimizador. Fija la NASA al Día 2 y luego
    prueba todas las permutaciones posibles de los lugares restantes
    entre el Día 1 y el Día 3, buscando la combinación que minimiza
    la distancia total sin exceder las 12 horas diarias.
    
    Devuelve:
        list[list[int]]: Una lista de 3 rutas (una por día), o None si no se
                         encuentra una solución válida.
    """
    idx_aeropuerto = get_location_index('Aeropuerto')
    idx_hotel = get_location_index('Hotel')
    idx_nasa = get_location_index('NASA')
    
    # Lugares a visitar (excluyendo inicio, fin y NASA)
    places_to_visit = [i for i in range(len(LOCATIONS)) if i not in 
                      {idx_aeropuerto, idx_hotel, idx_nasa}]
    
    best_routes_combination = None
    best_total_distance = float('inf')
    
    # Probar todas las divisiones posibles de lugares entre Día 1 y Día 3
    for day1_size in range(1, len(places_to_visit)):
        
        # Probar todas las permutaciones (órdenes) para el Día 1
        for day1_places in permutations(places_to_visit, day1_size):
            
            # Los lugares restantes van al Día 3
            day3_places_set = set(places_to_visit) - set(day1_places)
            
            # Probar todas las permutaciones (órdenes) para el Día 3
            for day3_places in permutations(list(day3_places_set)):
                
                # --- Construir y Validar Rutas ---
                
                # Día 1: Aeropuerto -> lugares -> Hotel
                day1_route = [idx_aeropuerto] + list(day1_places) + [idx_hotel]
                day1_time = calculate_route_time(day1_route)
                
                if day1_time > MAX_TIME_PER_DAY:
                    continue  # Esta combinación no es válida
                
                # Día 2: Hotel -> NASA -> Hotel
                day2_route = [idx_hotel, idx_nasa, idx_hotel]
                day2_time = calculate_route_time(day2_route)
                
                if day2_time > MAX_TIME_PER_DAY:
                    # Si el día 2 falla, ninguna combinación funcionará (es fijo)
                    print("Error: El día 2 (NASA) excede el tiempo máximo.")
                    return None
                
                # Día 3: Hotel -> lugares -> Aeropuerto
                day3_route = [idx_hotel] + list(day3_places) + [idx_aeropuerto]
                day3_time = calculate_route_time(day3_route)
                
                if day3_time > MAX_TIME_PER_DAY:
                    continue  # Esta combinación no es válida
                
                # --- Calcular Distancia Total ---
                current_distance = (calculate_route_distance(day1_route) + 
                                  calculate_route_distance(day2_route) + 
                                  calculate_route_distance(day3_route))
                
                # --- Actualizar Mejor Resultado ---
                if current_distance < best_total_distance:
                    best_total_distance = current_distance
                    best_routes_combination = [day1_route, day2_route, day3_route]

    return best_routes_combination

# --- FUNCIÓN DE IMPRESIÓN ---

def print_detailed_itinerary(routes):
    """
    Imprime en consola un itinerario formateado y detallado.
    
    Argumentos:
        routes (list[list[int]]): Las 3 rutas óptimas encontradas.
    """
    total_distance_global = 0
    total_time_global = 0
    
    for day, route in enumerate(routes, 1):
        print(f"\n{'='*10} Día {day} {'='*10}")
        
        route_names = [LOCATIONS[i] for i in route]
        print(f"Ruta: {' → '.join(route_names)}")
        
        day_distance = calculate_route_distance(route)
        day_time = calculate_route_time(route)
        
        print("\nDetalle por segmento:")
        current_time_accumulator = 0
        
        # Detalle de la ruta
        for i in range(len(route) - 1):
            from_idx, to_idx = route[i], route[i+1]
            from_loc, to_loc = LOCATIONS[from_idx], LOCATIONS[to_idx]
            
            travel_time_h = DISTANCES_KM[from_idx, to_idx] / VELOCIDAD_PROMEDIO_KMH
            visit_time_h = TIMES_AT_LOCATION[to_idx]
            
            print(f"  {from_loc} → {to_loc}:")
            print(f"    - Tiempo de viaje: {travel_time_h:.2f} horas")
            current_time_accumulator += travel_time_h
            
            # No se suma tiempo de visita en el destino final del día
            if to_loc in ('Hotel', 'Aeropuerto') and i == len(route) - 2:
                 pass
            else:
                print(f"    - Tiempo en {to_loc}: {visit_time_h:.2f} horas")
                current_time_accumulator += visit_time_h

        print(f"\nResumen día {day}:")
        print(f"  - Distancia recorrida: {day_distance} km")
        print(f"  - Tiempo total (viaje + visita): {day_time:.2f} horas")
        
        total_distance_global += day_distance
        total_time_global += day_time
    
    print(f"\n{'='*10} RESUMEN FINAL {'='*10}")
    print(f"Distancia total recorrida: {total_distance_global} km")
    print(f"Tiempo total del viaje: {total_time_global:.2f} horas")
    
    print("\nLugares visitados por día:")
    for day, route in enumerate(routes, 1):
        day_locations = [LOCATIONS[i] for i in route[1:-1]] # Excluir inicio y fin
        if day_locations:
            print(f"Día {day}: {', '.join(day_locations)}")
        else:
            print(f"Día {day}: (Día de traslado o visita única)")

# --- PUNTO DE ENTRADA PRINCIPAL ---

if __name__ == "__main__":
    print("Calculando el itinerario óptimo...")
    
    best_routes = find_best_routes()
    
    if best_routes:
        print("¡Se encontró el mejor itinerario!")
        print_detailed_itinerary(best_routes)
    else:
        print("No se encontró una solución que cumpla con todas las restricciones de tiempo.")