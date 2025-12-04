import os
import time
import shutil
import xml.etree.ElementTree as ET


# -------------------------------------------------------
# Función para limpiar la pantalla
# -------------------------------------------------------
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


# -------------------------------------------------------
# Cargar XML
# -------------------------------------------------------
def cargar_xml(ruta):
    try:
        tree = ET.parse(ruta)
        return tree
    except FileNotFoundError:
        print(f"ERROR El archivo '{ruta}' no existe.")
        return None
    except ET.ParseError:
        print(f"ERROR El archivo '{ruta}' tiene un formato XML inválido.")
        return None


# -------------------------------------------------------
# Guardar XML
# -------------------------------------------------------
def guardar_xml(tree, ruta):
    tree.write(ruta, encoding="utf-8", xml_declaration=True)


# -------------------------------------------------------
# FUNCIÓN mostrar_datos
# -------------------------------------------------------
def mostrar_datos(root):
    usuarios = root.findall("usuario")

    print("\n--- Contenido Actual del XML ---")

    if not usuarios:
        print("ERROR No hay usuarios en el archivo XML.")
        print("--- Fin del Contenido ---\n")
        return

    for u in usuarios:
        id_val = u.find("id").text
        nombre_val = u.find("nombre").text
        edad_val = u.find("edad").text
        print(f"ID: {id_val}, Nombre: {nombre_val}, Edad: {edad_val}")

    print("--- Fin del Contenido ---\n")


# -------------------------------------------------------
# FUNCIÓN inicializar_datos
# -------------------------------------------------------
def inicializar_datos(archivo_origen, archivo_destino):
    if not os.path.exists(archivo_origen):
        print(f"ERROR El archivo origen '{archivo_origen}' no existe. No se realizó la copia.")
        return False

    try:
        ET.parse(archivo_origen)
    except ET.ParseError:
        print(f"ERROR El archivo origen '{archivo_origen}' tiene un formato XML inválido.")
        return False

    shutil.copyfile(archivo_origen, archivo_destino)
    print(f"Datos inicializados desde '{archivo_origen}' a '{archivo_destino}'.")
    return True


# -------------------------------------------------------
# FUNCIÓN crear_arbol
# -------------------------------------------------------
def crear_arbol(nombre_raiz):
    root = ET.Element(nombre_raiz)
    tree = ET.ElementTree(root)
    return tree


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

    origen = "src/datos_usuarios_orig.xml"
    destino = "src/datos_usuarios.xml"

    # Inicializar datos
    inicializar_datos(origen, destino)

    # Cargar XML
    tree = cargar_xml(destino)

    # Si no se pudo cargar → crear uno nuevo
    if tree is None:
        print("Creando archivo XML nuevo...")
        tree = crear_arbol("usuarios")

    root = tree.getroot()

    # Mostrar contenido inicial
    mostrar_datos(root)
    pausa()

    # ---------------------------------------------------
    # Actualizar edad de usuario con ID 1
    # ---------------------------------------------------
    for u in root.findall("usuario"):
        if u.find("id").text == "1":
            u.find("edad").text = "31"
            print("Usuario con ID 1 actualizado.")
            break

    mostrar_datos(root)
    pausa()

    # ---------------------------------------------------
    # Insertar nuevo usuario (ID 3 - Pedro)
    # ---------------------------------------------------
    nuevo = ET.Element("usuario")
    ET.SubElement(nuevo, "id").text = "3"
    ET.SubElement(nuevo, "nombre").text = "Pedro"
    ET.SubElement(nuevo, "edad").text = "40"

    root.append(nuevo)

    print("Usuario Pedro añadido con éxito.")
    mostrar_datos(root)
    pausa()

    # ---------------------------------------------------
    # Eliminar usuario con ID 2
    # ---------------------------------------------------
    for u in root.findall("usuario"):
        if u.find("id").text == "2":
            root.remove(u)
            print("Usuario con ID 2 eliminado.")
            break

    mostrar_datos(root)
    pausa()

    # Guardar archivo final
    guardar_xml(tree, destino)
    print("Operaciones completadas. Archivo actualizado.")


# -------------------------------------------------------
# EJECUCIÓN DEL PROGRAMA
# -------------------------------------------------------
if __name__ == "__main__":
    main()

