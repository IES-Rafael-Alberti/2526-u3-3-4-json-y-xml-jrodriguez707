import json
import os
import time

# -------------------------------------------------------
# Función para limpiar la pantalla
# -------------------------------------------------------
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


# -------------------------------------------------------
# Función cargar_json
# -------------------------------------------------------
def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Validación de existencia del nodo usuarios
        if "usuarios" not in datos or not isinstance(datos["usuarios"], list):
            print("ERROR El archivo JSON no contiene usuarios!")
            return {"usuarios": []}

        return datos

    except FileNotFoundError:
        print(f"ERROR El archivo '{ruta}' no existe.")
        return {"usuarios": []}
    except json.JSONDecodeError:
        print(f"ERROR El archivo '{ruta}' tiene un formato JSON inválido.")
        return {"usuarios": []}


# -------------------------------------------------------
# Función guardar_json
# -------------------------------------------------------
def guardar_json(ruta, datos):
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR al guardar el archivo: {e}")


# -------------------------------------------------------
# FUNCIÓN mostrar_datos
# -------------------------------------------------------
def mostrar_datos(datos):
    usuarios = datos.get("usuarios", [])

    print("\n--- Contenido Actual del JSON ---")
    if not usuarios:
        print("ERROR El archivo JSON no contiene usuarios!")
        print("--- Fin del Contenido ---\n")
        return

    for u in usuarios:
        print(f"ID: {u['id']}, Nombre: {u['nombre']}, Edad: {u['edad']}")

    print("--- Fin del Contenido ---\n")


# -------------------------------------------------------
# FUNCIÓN inicializar_datos
# -------------------------------------------------------
def inicializar_datos(archivo_origen, archivo_destino):
    if not os.path.exists(archivo_origen):
        print(f"ERROR El archivo origen '{archivo_origen}' no existe. No se realizó la copia.")
        return False

    try:
        with open(archivo_origen, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR El archivo origen '{archivo_origen}' tiene un formato JSON inválido.")
        return False

    # Guardar copia
    with open(archivo_destino, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print(f"Datos inicializados desde '{archivo_origen}' a '{archivo_destino}'.")
    return True


# -------------------------------------------------------
# Función pausa
# -------------------------------------------------------
def pausa():
    input("Presione una tecla para continuar . . . ")


# -------------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------------
def main():
    limpiar_consola()

    origen = "src/datos_usuarios_orig.json"
    destino = "src/datos_usuarios.json"

    # Inicializar datos
    inicializar_datos(origen, destino)

    # Cargar JSON
    datos = cargar_json(destino)

    # Mostrar contenido inicial
    mostrar_datos(datos)
    pausa()

    # ---------------------------------------------------
    # Actualizar edad de un usuario (ID 1 → edad 31)
    # ---------------------------------------------------
    for u in datos["usuarios"]:
        if u["id"] == 1:
            u["edad"] = 31
            print("Usuario con ID 1 actualizado.")
            break

    mostrar_datos(datos)
    pausa()

    # ---------------------------------------------------
    # Insertar nuevo usuario (Pedro)
    # ---------------------------------------------------
    datos["usuarios"].append({"id": 3, "nombre": "Pedro", "edad": 40})
    print("Usuario Pedro añadido con éxito.")

    mostrar_datos(datos)
    pausa()

    # ---------------------------------------------------
    # Eliminar usuario con ID 2
    # ---------------------------------------------------
    datos["usuarios"] = [u for u in datos["usuarios"] if u["id"] != 2]
    print("Usuario con ID 2 eliminado.")

    mostrar_datos(datos)
    pausa()

    # Guardar cambios finales
    guardar_json(destino, datos)

    print("Operaciones completadas. Archivo actualizado.")


# -------------------------------------------------------
# EJECUCIÓN DEL PROGRAMA
# -------------------------------------------------------
if __name__ == "__main__":
    main()
