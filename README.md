# Sistema de ingeniería de datos (ETL Dropbox → MySQL)

Proyecto en Python que descarga archivos CSV desde Dropbox, normaliza datos de clientes y tarjetas, y los inserta en una base de datos MySQL evitando duplicados.

**Qué hace**
- Busca en la raíz de Dropbox archivos con nombre `Clientes-YYYY-MM-DD.csv` y `Tarjetas-YYYY-MM-DD.csv`.
- Descarga los CSV a `downloadedFiles/` y elimina CSV antiguos de esa carpeta.
- Normaliza campos (capitalización, email válido, teléfono, anonimización de DNI y CVV, hash de tarjeta).
- Inserta en MySQL evitando duplicados por `cod_cliente` y por número de tarjeta (verificación con hash).

**Requisitos**
- Python 3.9+ (recomendado).
- MySQL accesible desde el entorno local.
- Credenciales de una app de Dropbox.

**Instalación**
1. Instala dependencias:
```bash
pip install -r requirements.txt
```
2. Crea el archivo `.env` a partir de `.env.example` y completa los valores.
3. Genera el `DROPBOX_REFRESH_TOKEN` (ver sección siguiente).
4. Asegura que la base de datos y tablas existan (ver esquema sugerido).

**Generar `DROPBOX_REFRESH_TOKEN`**
1. Completa `DROPBOX_APP_KEY` y `DROPBOX_APP_SECRET` en `.env`.
2. Ejecuta:
```bash
python3 dropboxRefreshTokenRequest.py
```
3. Abre el enlace, autoriza la app, pega el código y copia el token que se imprime como `REFRESH TOKEN:`.
4. Pégalo en `DROPBOX_REFRESH_TOKEN` dentro de `.env`.

**Esquema sugerido de base de datos**
Si aún no tienes tablas, este esquema es compatible con el código actual:
```sql
CREATE TABLE clients (
  cod_cliente VARCHAR(50) PRIMARY KEY,
  nombre VARCHAR(100),
  apellido1 VARCHAR(100),
  apellido2 VARCHAR(100),
  dni VARCHAR(20),
  correo VARCHAR(150),
  telefono VARCHAR(30)
);

CREATE TABLE tarjetas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cod_cliente_tarjeta VARCHAR(50),
  numero_tarjeta VARCHAR(255),
  fecha_exp VARCHAR(20),
  cvv VARCHAR(10)
);
```

**Uso**
1. Asegúrate de tener en la raíz de Dropbox **solo un archivo** que coincida con cada patrón:
- `Clientes-YYYY-MM-DD.csv`
- `Tarjetas-YYYY-MM-DD.csv`

Si hay varios, Dropbox no garantiza el orden y el script podría tomar uno inesperado.

2. Ejecuta:
```bash
python3 main.py
```

**Normalizaciones aplicadas**
- `nombre`, `apellido1`, `apellido2`, `cod_cliente`: `Title Case` y trim.
- `dni`: se anonimiza en formato `******XYZ`.
- `correo`: se valida con regex; si es inválido se guarda `n/a`.
- `telefono`: se eliminan espacios, guiones y paréntesis.
- `numero_tarjeta`: se hashea con Argon2 y se usa para detectar duplicados.
- `cvv`: se anonimiza en formato `**X`.
- Se descartan filas de clientes cuyo `nombre` contiene dígitos.

**Tests**
```bash
pytest
```

**Estructura del proyecto**
- `main.py`: orquesta descarga, lectura, normalización e inserción.
- `normalizers.py`: funciones de normalización.
- `db.py`: conexión e inserciones a MySQL + validación de duplicados.
- `dropboxAuth.py`: descarga de archivos desde Dropbox.
- `dropboxRefreshTokenRequest.py`: genera `refresh_token`.
- `testing/test_normalizers.py`: tests unitarios de normalizadores.

**Problemas comunes**
- `No cards in DB.`: es informativo cuando la tabla está vacía.
- Error de conexión MySQL: valida `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
- Error de Dropbox: valida credenciales en `.env` y permisos de la app.

