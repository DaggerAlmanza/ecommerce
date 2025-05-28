
# E-Commerce

## Descripción del Proyecto:
Este proyecto tiene como objetivo principal diseñar e implementar la arquitectura backend para una plataforma de e-commerce.  La aplicación permitirá a empresas y usuarios individuales (admin) vender sus productos, mientras que los compradores (user) podrán explorar, adquirir y gestionar sus pedidos.

## Requisitos Técnicos Cubiertos
Este proyecto cumple con los siguientes requisitos técnicos clave:

- Lenguaje de Programación y Framework: Utiliza Python y FastAPI, un framework de desarrollo web recomendado.
- Mecanismo de Autenticación: Implementa un mecanismo de autenticación para asegurar las llamadas a la API.
- Sistema de Colas: Integra Celery y Redis para el procesamiento asíncrono de órdenes, mejorando la escalabilidad y la experiencia del usuario.
- Despliegue Local con Docker Compose: Todos los servicios utilizados (PostgreSQL, Redis, FastAPI, Celery) pueden desplegarse localmente utilizando Docker Compose (opcionalmente se pueden usar soluciones en la nube).
- Diagrama UML de Base de Datos: Incluye un Diagrama Entidad-Relación para visualizar el diseño de la base de datos.
- API Documentada con Swagger: La API está completamente documentada y es accesible a través de Swagger UI.
- No se Requiere Frontend: El enfoque del proyecto es puramente el backend, por lo que no se incluye una interfaz de usuario.

# **Tecnologías y lenguajes**
En este proyecto, utilizaremos Python como lenguaje de programación, para la parte del servidor HTTP, emplearemos el frameworks (fastapi), la base de datos será PostgreSQL, las pruebas unitarias se llevarán a cabo utilizando pytest, la cola de tareas se llevarán a cabo utilizando Celery, el broker de colas será Redis, y por ultimo el estilo del código será pythonic, respetando el Zen de Python y siguiendo las convenciones de estilo definidas por PEP 8.

### Construido
* Lenguaje: Python 3.12.3
* Base de dato:  PostgreSQL
* Pruebas: Pytest
* Frameworks:  FastAPI
* Cola: Celery
* Persistencia de la cola: redis

### Entorno de trabajo y dependencias

1. Clona el repositorio:
```sh
git clone https://github.com/DaggerAlmanza/ecommerce
```

2. Instalar virtualEnv e instalarlo
Linux
```sh
$ virtualenv -p python3 venv
o
$ python3 -m venv venv
```
```sh
$ source venv/bin/activate
o
$ . venv/bin/activate
```
Windows
```sh
$ python -m venv venv
```
```sh
$ venv/Scripts/activate
```
3. Instalar requirements.txt
```sh
$ pip3 install -r requirements.txt
```

## Configuración

1. Se debe configurar el archivo .env con las credenciales de acceso a la base de datos.
```sh
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
```
2. Ejecuta las pruebas:

```sh
pytest
```

3. Ejecuta el servidor:
```sh
$ uvicorn config:app --host=localhost --port=8000
```

4. Inicia el worker de Celery (en una terminal separada):
```sh
celery -A app.config.celery:celery_app worker --loglevel=info --queues=orders_queue --concurrency=1
```

5. Crea una red Docker para que los contenedores puedan comunicarse:
```sh
docker network create ecommerce
```

6. Inicia el contenedor de Redis:
```sh
docker run --name redis -p 6377:6379 -d redis redis-server --network ecommerce --port 6379
```

7. Inicia el contenedor de PostgreSQL:
```sh
docker run --name postgres-db -e POSTGRES_DB=ecommerce -e POSTGRES_USER=dagger -e POSTGRES_PASSWORD=dager9123 -p 5432:5432 -v postgres_data:/var/lib/postgresql/data --network ecommerce -d postgres:16-alpine
```

## Arquictetura del proyecto
La arquitectura del proyecto está diseñada utilizando el modelo C4 para proporcionar una visión clara y concisa de los diferentes niveles del sistema.

### Diagrama de contexto del sistema
[![system-context-diagram.png](https://i.postimg.cc/nM89Xg5s/system-context-diagram.png)](https://postimg.cc/ctmLj9dZ)

### Diagrama de contenedores

[![container-diagram.png](https://i.postimg.cc/KzvPFXSx/container-diagram.png)](https://postimg.cc/d7pkmxVx)

### Diagrama de componentes

[![component-diagram.png](https://i.postimg.cc/RhhL7kXX/component-diagram.png)](https://postimg.cc/gL9hdT9Z)

## Diagrama Entidad-Relación (DER)
Este diagrama muestra la estructura de la base de datos y las relaciones entre las entidades.
[![entity-relationship-diagram.png](https://i.postimg.cc/0rRpRT25/entity-relationship-diagram.png)](https://postimg.cc/sGmB50hb)

## Rutas de la API
La API expone los siguientes endpoints para interactuar con el sistema. Puedes acceder a la documentación interactiva de la API con Swagger UI en http://127.0.0.1:8000/docs.

1. http://127.0.0.1:8000/api/v1/users

GET: Obtener todos los usuarios (solo disponible para admin).
POST: Crear un nuevo usuario (admin o user).

2. http://127.0.0.1:8000/api/v1/users/{id}

- PUT: Editar el propio usuario (no se pueden editar otros usuarios).
- GET: Obtener el propio usuario por ID (user), o cualquier usuario por ID (admin).
- DELETE: "Eliminar" un usuario del sistema (desactivación lógica para conservar el historial).

3. http://127.0.0.1:8000/api/v1/users/admin

- GET: Obtener todos los usuarios eliminados (solo disponible para admin).

4. http://127.0.0.1:8000/api/v1/cart_items/admin

- GET: Obtener todos los artículos de carritos creados (solo disponible para admin).

5. http://127.0.0.1:8000/api/v1/products/admin

- GET: Obtener todos los productos eliminados (solo disponible para admin).

6. http://127.0.0.1:8000/api/v1/carts

- GET: Obtener todos los carritos de compra (solo disponible para admin).
- POST: Crear un carrito de compra (solo lo puede realizar el usuario actual).

7. http://127.0.0.1:8000/api/v1/carts/{id}

- GET: Ver el propio carrito o consultar cualquier carrito si eres admin.

8. http://127.0.0.1:8000/api/v1/products

- GET: Obtener todos los productos disponibles.
- POST: Crear un nuevo producto (solo disponible para admin).

9. http://127.0.0.1:8000/api/v1/products/upload_file

- POST: Subir una imagen (simulando un servicio de almacenamiento como S3, pero almacenado localmente).

10. http://127.0.0.1:8000/api/v1/products/{id} (disponible para admin salvo indicación contraria)

- PUT: Editar un producto.
- DELETE: Eliminar un producto del sistema (desactivación lógica).
- GET: Obtener un producto por ID (disponible para todos).

11. http://127.0.0.1:8000/api/v1/cart_items (disponible solo para usuario)

- GET: Obtener todos los artículos del carrito del usuario.
- POST: Crear un artículo en el carrito, validando la disponibilidad del producto.

12. http://127.0.0.1:8000/api/v1/cart_items/{id}

- PUT: Editar un artículo del carrito.
- GET: Obtener un artículo del carrito por ID.
- DELETE: Borrar un artículo del carrito.

13. http://127.0.0.1:8000/api/v1/order_items

- GET: Obtener todos los artículos de las órdenes disponibles en la base de datos (solo admin).

14. http://127.0.0.1:8000/api/v1/order_items/{id}

- GET: Obtener un artículo de orden por ID (solo admin).

15. http://127.0.0.1:8000/api/v1/order_items/user

- GET: Obtener todos los artículos de las órdenes disponibles para el usuario actual.

16. http://127.0.0.1:8000/api/v1/orders

- GET: Obtener todas las órdenes (solo admin).
- POST: Crear una orden (disponible para user). Este proceso se encola (FIFO) y ejecuta una transacción que:
    * Toma todos los artículos del carrito del usuario.
    * Crea la orden y sus artículos asociados.
    * Verifica la existencia y disponibilidad de los productos.
    * Descuenta el stock de los productos.
    * Elimina los artículos del carrito.

17. http://127.0.0.1:8000/api/v1/orders/{task_id} (o similar, para verificar el estado de la tarea encolada)

- GET: Verificar el estado de la tarea de creación de orden.

18. http://127.0.0.1:8000/api/v1/orders/tasks/{task_id} (si tienes una ruta específica para el estado de tareas)

- GET: Verificar el estado de la tarea.

19. http://127.0.0.1:8000/api/v1/orders/{id}

- GET: Obtener una orden por ID.
- PUT: Editar el estado de una orden (solo por parte de admin).

20. http://127.0.0.1:8000/token

- GET: Obtener el token de autenticación actual del usuario.
- POST: Iniciar sesión para obtener un nuevo token.

21. http://127.0.0.1:8000/

- GET: Verificar que el servicio está operativo (up).
