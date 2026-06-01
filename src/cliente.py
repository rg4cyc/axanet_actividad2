"""
Modelo Cliente para el sistema AXANET.

Este módulo define la clase Cliente y sus reglas básicas de validación.
La intención es migrar la lógica de la Actividad I desde Bash hacia Python
con una estructura más ordenada y orientada a objetos.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class Cliente:
    """Representa a un cliente de AXANET."""

    nombre: str
    correo: str
    telefono: str
    direccion: str
    rfc: str = "XAXX010101000"
    servicios: List[str] = field(default_factory=list)
    id_cliente: str = field(default_factory=lambda: f"CLI-{uuid4().hex[:8].upper()}")
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def __post_init__(self) -> None:
        """Ejecuta validaciones después de construir el objeto."""
        self.nombre = self.nombre.strip()
        self.correo = self.correo.strip()
        self.telefono = self.telefono.strip()
        self.direccion = self.direccion.strip()
        self.rfc = self.rfc.strip().upper()
        self.servicios = [servicio.strip() for servicio in self.servicios if servicio.strip()]
        self.validar()

    def validar(self) -> None:
        """Valida los datos mínimos del cliente."""
        if len(self.nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$", self.correo):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        if not re.match(r"^\d{10}$", self.telefono):
            raise ValueError("El teléfono debe contener exactamente 10 dígitos.")
        if len(self.direccion) < 5:
            raise ValueError("La dirección debe tener al menos 5 caracteres.")
        if not re.match(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$", self.rfc):
            raise ValueError("El RFC no tiene un formato válido.")

    def agregar_servicio(self, descripcion: str) -> None:
        """Agrega una descripción de servicio al historial del cliente."""
        descripcion = descripcion.strip()
        if len(descripcion) < 3:
            raise ValueError("La descripción del servicio debe tener al menos 3 caracteres.")
        fecha = datetime.now().strftime("%Y-%m-%d")
        self.servicios.append(f"{fecha}: {descripcion}")

    def actualizar(self, nombre: str | None = None, correo: str | None = None,
                   telefono: str | None = None, direccion: str | None = None,
                   rfc: str | None = None) -> None:
        """Actualiza datos del cliente ignorando campos vacíos."""
        if nombre:
            self.nombre = nombre.strip()
        if correo:
            self.correo = correo.strip()
        if telefono:
            self.telefono = telefono.strip()
        if direccion:
            self.direccion = direccion.strip()
        if rfc:
            self.rfc = rfc.strip().upper()
        self.validar()

    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte el cliente a diccionario para persistirlo como JSON."""
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "rfc": self.rfc,
            "servicios": self.servicios,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Cliente":
        """Reconstruye un Cliente desde un diccionario leído de JSON."""
        return cls(
            id_cliente=datos["id_cliente"],
            nombre=datos["nombre"],
            correo=datos["correo"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            rfc=datos.get("rfc", "XAXX010101000"),
            servicios=datos.get("servicios", []),
            fecha_creacion=datos.get("fecha_creacion", datetime.now().isoformat(timespec="seconds")),
        )

    def __str__(self) -> str:
        """Representación legible para la terminal."""
        return f"{self.id_cliente} | {self.nombre} | {self.correo} | {self.telefono}"

    def __eq__(self, other: object) -> bool:
        """Compara clientes por ID."""
        if not isinstance(other, Cliente):
            return False
        return self.id_cliente == other.id_cliente

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return f"Cliente(id_cliente={self.id_cliente!r}, nombre={self.nombre!r})"
