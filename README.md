# Banco Seguro

Aplicación bancaria simple escrita en Python con Flet, utilizando POO y datos cargados desde JSON.

## Características

- Login con email o cédula y contraseña
- Dashboard con cuentas, tarjetas y movimientos
- Datos cargados desde `data/datos.json`
- Contenerización con Docker y exposición en el puerto `8555`

## Estructura

- `main.py` - App Flet principal
- `utils/data_manager.py` - Carga y administra datos del banco
- `models/` - Clases POO para usuarios, cuentas, tarjetas y transacciones
- `data/datos.json` - Datos de ejemplo para la app
- `Dockerfile` - Imagen Docker
- `docker-compose.yml` - Orquestación de contenedor

## Requisitos

- Python 3.10+
- Docker (opcional)

## Uso local

1. Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

2. Ejecuta la app:

```bash
python main.py
```

3. Abre en tu navegador:

```text
http://localhost:8555
```

## Uso con Docker

1. Construye la imagen:

```bash
docker build -t bancoseguro .
```

2. Ejecuta el contenedor:

```bash
docker run -p 8555:8555 bancoseguro
```

3. Abre en tu navegador:

```text
http://localhost:8555
```

## Uso con Docker Compose

```bash
docker-compose up --build
```

## Credenciales de prueba

- `juan.garcia@email.com` / `123456`
- `maria.lopez@email.com` / `password123`
- `carlos.martinez@email.com` / `seguridadmax`

## Nota

La app utiliza Flet para convertir la interfaz a web y carga los datos directamente desde el archivo `data/datos.json`.
