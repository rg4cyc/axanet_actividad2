"""Pruebas unitarias para Cliente y GestorClientes."""
import json

import pytest

from src.cliente import Cliente
from src.gestor import GestorClientes


def test_crear_cliente_valido():
    cliente = Cliente("Ana Maria Lopez", "ana@example.com", "5512345678", "Calle 123", "LOAA900101ABC")
    assert cliente.nombre == "Ana Maria Lopez"
    assert cliente.correo == "ana@example.com"
    assert cliente.telefono == "5512345678"
    assert cliente.rfc == "LOAA900101ABC"


def test_cliente_falla_con_correo_invalido():
    with pytest.raises(ValueError):
        Cliente("Ana Maria Lopez", "correo-invalido", "5512345678", "Calle 123", "LOAA900101ABC")


def test_cliente_falla_con_telefono_invalido():
    with pytest.raises(ValueError):
        Cliente("Ana Maria Lopez", "ana@example.com", "55ABC", "Calle 123", "LOAA900101ABC")


def test_cliente_falla_con_rfc_invalido():
    with pytest.raises(ValueError):
        Cliente("Ana Maria Lopez", "ana@example.com", "5512345678", "Calle 123", "RFC-MAL")


def test_gestor_crea_consulta_actualiza_y_elimina_cliente(tmp_path):
    ruta = tmp_path / "clientes.json"
    gestor = GestorClientes(str(ruta))
    cliente = Cliente("Carlos Perez", "carlos@example.com", "5598765432", "Avenida 456", "PECC880202DEF")
    gestor.crear_cliente(cliente)
    assert gestor.obtener_por_id(cliente.id_cliente) == cliente
    assert gestor.buscar_por_nombre("carlos")[0] == cliente
    gestor.actualizar_cliente(cliente.id_cliente, correo="nuevo@example.com", telefono="5511112222")
    actualizado = gestor.obtener_por_id(cliente.id_cliente)
    assert actualizado is not None
    assert actualizado.correo == "nuevo@example.com"
    assert actualizado.telefono == "5511112222"
    gestor.agregar_servicio(cliente.id_cliente, "Soldadura de piezas")
    actualizado = gestor.obtener_por_id(cliente.id_cliente)
    assert actualizado is not None
    assert len(actualizado.servicios) == 1
    assert gestor.eliminar_cliente(cliente.id_cliente) is True
    assert gestor.obtener_por_id(cliente.id_cliente) is None


def test_persistencia_json(tmp_path):
    ruta = tmp_path / "clientes.json"
    gestor = GestorClientes(str(ruta))
    cliente = Cliente("Luisa Gomez", "luisa@example.com", "5588887777", "Calle Norte 99", "GOLU850303GHI")
    gestor.crear_cliente(cliente)
    with ruta.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    assert "clientes" in datos
    assert datos["clientes"][0]["nombre"] == "Luisa Gomez"
    nuevo_gestor = GestorClientes(str(ruta))
    assert nuevo_gestor.obtener_por_id(cliente.id_cliente) is not None
