# Actividad II: Migración AXANET de Bash a Python

## Descripción

Este proyecto migra el sistema de gestión de clientes de AXANET desde un script Bash hacia una aplicación Python con programación orientada a objetos. La aplicación permite crear, consultar, actualizar y eliminar clientes mediante una interfaz de línea de comandos, usando archivos JSON como mecanismo de persistencia.

## Estructura

```text
proyecto/
├── src/
│   ├── __init__.py
│   ├── cliente.py
│   ├── gestor.py
│   └── app.py
├── data/
│   └── clientes.json
├── tests/
│   └── test_cliente.py
├── .github/
│   └── workflows/
│       ├── testing.yml
│       ├── lint.yml
│       └── deploy.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Funcionalidades

- Crear cliente nuevo.
- Listar clientes registrados.
- Buscar cliente por nombre.
- Visualizar cliente por ID.
- Actualizar datos de cliente.
- Agregar servicio a cliente recurrente.
- Eliminar cliente.
- Guardar información en JSON.
- Validar nombre, correo, teléfono, dirección y RFC.

## Instalación local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python -m src.app
```

## Pruebas y lint

```bash
pytest
flake8 src tests
```

## Docker

```bash
docker build -t axanet-clientes:1.0 .
docker run -it --rm axanet-clientes:1.0
```

## GitFlow propuesto

- `main`: versión estable.
- `develop`: rama de integración.
- `feature/crud-operations`: implementación CRUD.
- `feature/validation`: validaciones de datos y pruebas.

## GitHub Actions

- `testing.yml`: ejecuta pruebas con pytest.
- `lint.yml`: valida estilo con flake8.
- `deploy.yml`: simula despliegue y genera artifact.

## Operaciones CRUD implementadas

La aplicación implementa las operaciones básicas de gestión de clientes:

- CREATE: permite crear un nuevo cliente con nombre, RFC, correo, teléfono, dirección y servicio inicial.
- READ: permite listar todos los clientes, buscar por nombre y visualizar un cliente por ID.
- UPDATE: permite actualizar datos de un cliente existente y agregar servicios recurrentes.
- DELETE: permite eliminar un cliente del archivo JSON de persistencia.

Estas operaciones se concentran en `src/gestor.py`, mientras que `src/app.py` funciona como interfaz de línea de comandos.
