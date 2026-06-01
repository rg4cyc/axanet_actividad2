"""Interfaz de línea de comandos para AXANET."""
from __future__ import annotations

from .cliente import Cliente
from .gestor import GestorClientes


def mostrar_menu() -> None:
    """Muestra las opciones disponibles."""
    print("\n=== Sistema de Gestión de Clientes AXANET ===")
    print("1. Crear nuevo cliente")
    print("2. Listar todos los clientes")
    print("3. Buscar cliente por nombre")
    print("4. Visualizar cliente por ID")
    print("5. Actualizar cliente")
    print("6. Agregar servicio a cliente recurrente")
    print("7. Eliminar cliente")
    print("8. Salir")


def pedir_cliente() -> Cliente:
    """Solicita datos por terminal y crea una instancia de Cliente."""
    nombre = input("Nombre completo: ")
    correo = input("Correo electrónico: ")
    telefono = input("Teléfono (10 dígitos): ")
    direccion = input("Dirección: ")
    rfc = input("RFC: ")
    servicio = input("Descripción del primer servicio solicitado: ")
    cliente = Cliente(nombre=nombre, correo=correo, telefono=telefono, direccion=direccion, rfc=rfc)
    cliente.agregar_servicio(servicio)
    return cliente


def crear_cliente(gestor: GestorClientes) -> None:
    """Crea un cliente nuevo desde la interfaz."""
    try:
        cliente = pedir_cliente()
        gestor.crear_cliente(cliente)
        print(f"Cliente creado correctamente. ID: {cliente.id_cliente}")
    except ValueError as error:
        print(f"Error: {error}")


def listar_clientes(gestor: GestorClientes) -> None:
    """Lista todos los clientes registrados."""
    clientes = gestor.listar_todos()
    if not clientes:
        print("No hay clientes registrados.")
        return
    print("\nClientes registrados:")
    for cliente in clientes:
        print(cliente)


def buscar_cliente(gestor: GestorClientes) -> None:
    """Busca clientes por nombre."""
    nombre = input("Nombre o parte del nombre: ")
    resultados = gestor.buscar_por_nombre(nombre)
    if not resultados:
        print("No se encontraron clientes.")
        return
    print("\nResultados:")
    for cliente in resultados:
        print(cliente)


def visualizar_cliente(gestor: GestorClientes) -> None:
    """Muestra toda la información de un cliente por ID."""
    id_cliente = input("ID del cliente: ")
    cliente = gestor.obtener_por_id(id_cliente)
    if cliente is None:
        print("Cliente no encontrado.")
        return
    print("\nInformación del cliente:")
    for clave, valor in cliente.a_diccionario().items():
        print(f"{clave}: {valor}")


def actualizar_cliente(gestor: GestorClientes) -> None:
    """Actualiza parcialmente los datos de un cliente."""
    id_cliente = input("ID del cliente a actualizar: ")
    cliente = gestor.obtener_por_id(id_cliente)
    if cliente is None:
        print("Cliente no encontrado.")
        return
    print("Deja el campo vacío para conservar el valor actual.")
    nombre = input(f"Nombre [{cliente.nombre}]: ") or None
    correo = input(f"Correo [{cliente.correo}]: ") or None
    telefono = input(f"Teléfono [{cliente.telefono}]: ") or None
    direccion = input(f"Dirección [{cliente.direccion}]: ") or None
    rfc = input(f"RFC [{cliente.rfc}]: ") or None
    try:
        cliente_actualizado = gestor.actualizar_cliente(id_cliente, nombre, correo, telefono, direccion, rfc)
        print(f"Cliente actualizado: {cliente_actualizado}")
    except ValueError as error:
        print(f"Error: {error}")


def agregar_servicio(gestor: GestorClientes) -> None:
    """Agrega un servicio a un cliente existente."""
    id_cliente = input("ID del cliente recurrente: ")
    descripcion = input("Descripción del nuevo servicio: ")
    try:
        cliente = gestor.agregar_servicio(id_cliente, descripcion)
        print(f"Servicio agregado correctamente a {cliente.nombre}.")
    except ValueError as error:
        print(f"Error: {error}")


def eliminar_cliente(gestor: GestorClientes) -> None:
    """Elimina un cliente por ID."""
    id_cliente = input("ID del cliente a eliminar: ")
    eliminado = gestor.eliminar_cliente(id_cliente)
    print("Cliente eliminado correctamente." if eliminado else "Cliente no encontrado.")


def main() -> None:
    """Ejecuta el ciclo principal del menú."""
    gestor = GestorClientes()
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción [1-8]: ").strip()
        if opcion == "1":
            crear_cliente(gestor)
        elif opcion == "2":
            listar_clientes(gestor)
        elif opcion == "3":
            buscar_cliente(gestor)
        elif opcion == "4":
            visualizar_cliente(gestor)
        elif opcion == "5":
            actualizar_cliente(gestor)
        elif opcion == "6":
            agregar_servicio(gestor)
        elif opcion == "7":
            eliminar_cliente(gestor)
        elif opcion == "8":
            print("Saliendo del sistema. Hasta luego.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
