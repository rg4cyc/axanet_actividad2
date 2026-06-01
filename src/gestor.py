"""
Gestor CRUD para clientes AXANET.

Este módulo administra la persistencia en JSON y centraliza las operaciones:
crear, leer, actualizar y eliminar clientes.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .cliente import Cliente


class GestorClientes:
    """Administra clientes en memoria y los guarda en un archivo JSON."""

    def __init__(self, ruta_archivo: str = "data/clientes.json") -> None:
        """Inicializa el gestor y carga datos existentes."""
        self.ruta_archivo = Path(ruta_archivo)
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        self.clientes: Dict[str, Cliente] = {}
        self.cargar()

    def cargar(self) -> None:
        """Carga clientes desde el archivo JSON hacia memoria."""
        if not self.ruta_archivo.exists():
            self.guardar()
            return
        with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.clientes = {
            item["id_cliente"]: Cliente.desde_diccionario(item)
            for item in datos.get("clientes", [])
        }

    def guardar(self) -> None:
        """Guarda los clientes actuales en el archivo JSON."""
        datos = {"clientes": [cliente.a_diccionario() for cliente in self.clientes.values()]}
        with self.ruta_archivo.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

    def crear_cliente(self, cliente: Cliente) -> Cliente:
        """Agrega un nuevo cliente y persiste el cambio."""
        if cliente.id_cliente in self.clientes:
            raise ValueError("Ya existe un cliente con ese ID.")
        self.clientes[cliente.id_cliente] = cliente
        self.guardar()
        return cliente

    def obtener_por_id(self, id_cliente: str) -> Cliente | None:
        """Busca un cliente por ID."""
        return self.clientes.get(id_cliente.strip())

    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes cuyo nombre contenga el texto indicado."""
        nombre = nombre.strip().lower()
        return [cliente for cliente in self.clientes.values() if nombre in cliente.nombre.lower()]

    def listar_todos(self) -> List[Cliente]:
        """Devuelve todos los clientes registrados."""
        return list(self.clientes.values())

    def actualizar_cliente(self, id_cliente: str, nombre: str | None = None,
                           correo: str | None = None, telefono: str | None = None,
                           direccion: str | None = None, rfc: str | None = None) -> Cliente:
        """Actualiza datos de un cliente existente."""
        cliente = self.obtener_por_id(id_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        cliente.actualizar(nombre=nombre, correo=correo, telefono=telefono, direccion=direccion, rfc=rfc)
        self.guardar()
        return cliente

    def agregar_servicio(self, id_cliente: str, descripcion: str) -> Cliente:
        """Agrega un nuevo servicio a un cliente recurrente."""
        cliente = self.obtener_por_id(id_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        cliente.agregar_servicio(descripcion)
        self.guardar()
        return cliente

    def eliminar_cliente(self, id_cliente: str) -> bool:
        """Elimina un cliente por ID."""
        if id_cliente not in self.clientes:
            return False
        del self.clientes[id_cliente]
        self.guardar()
        return True

    def indice_por_nombre(self) -> Dict[str, str]:
        """Crea una tabla hash secundaria nombre -> id_cliente."""
        return {cliente.nombre.lower(): cliente.id_cliente for cliente in self.clientes.values()}
