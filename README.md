# Edu-IA 360 | Asesor Cesim Hospitality — Nivel 3

Aplicación de referencia que combina:
- Nivel 1: registro de rondas, tablero, bitácora de decisiones y reflexión.
- Nivel 2: importación de reportes CSV/Excel, vista de datos importados y exportación de respaldo.
- Nivel 3: asesor estratégico con IA generativa OpenAI, usando datos del equipo, resultados históricos, decisiones, Outlook y pregunta del alumno.

## Requisitos
- Windows 10/11
- Python 3.11 o posterior
- Conexión a internet para consultar OpenAI
- Una clave de Google AI Studio para activar la asesoría generativa

## Instalación en Windows (PowerShell)
1. Descomprime el ZIP en una carpeta.
2. Abre PowerShell dentro de esa carpeta.
3. Ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

4. En `.env`, sustituye `PEGA_AQUI_TU_CLAVE` por tu clave privada de Google AI Studio.
   No compartas la clave ni la publiques en el HTML.
5. Inicia la aplicación:

```powershell
uvicorn server:app --reload
```

6. Abre en Chrome o Edge: http://127.0.0.1:8000

Si PowerShell bloquea la activación del entorno virtual, puedes ejecutar directamente:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn server:app --reload
```

## Uso recomendado
1. Carga datos de ejemplo para conocer la interfaz.
2. Registra rondas reales o importa CSV/Excel.
3. Selecciona el equipo y confirma la ronda actual.
4. Agrega las decisiones que el equipo tomó y, si se dispone, el Outlook del mercado.
5. En “Asesor experto con IA”, plantea una pregunta concreta.
6. Contrasta las recomendaciones con los reportes oficiales y con las reglas de la ronda.
7. Registra qué recomendación se adoptó y mide su resultado en la ronda posterior.

## Seguridad y límites
- La clave de OpenAI vive en el backend (`.env`), no en el navegador.
- Los datos capturados en esta demo se guardan en el navegador del dispositivo (localStorage).
- Al solicitar asesoría generativa, el resumen de la ronda, el historial seleccionado, las decisiones y el texto del Outlook se envían a OpenAI mediante el backend. No incluyas nombres completos, correos, calificaciones sensibles ni datos personales innecesarios.
- La aplicación no se conecta directamente a la cuenta Cesim. Importa archivos que el usuario tenga autorización para utilizar.
- El lector de CSV/Excel muestra los datos y permite enviarlos como contexto al asesor; no puede asumir automáticamente que cualquier columna tiene un significado correcto. Verifica etiquetas, moneda, unidades y periodo.
- El asesor no garantiza decisiones ganadoras. Trata las sugerencias como hipótesis que deben contrastarse con el manual, las condiciones del mercado y los resultados.
- Antes de desplegar para una clase, añadir autenticación, base de datos central, control de roles, copias de seguridad y política institucional de privacidad.

## Contexto del manual compartido
El manual describe un simulador hotelero y de restaurante con áreas de ventas/recepción, restaurante, limpieza, mantenimiento, recursos humanos y compras. Señala que las decisiones pueden tener efectos inmediatos, efectos de largo plazo y consecuencias sobre competidores. La meta general es crecimiento rentable y sostenible medido por utilidades acumuladas, salvo criterio alternativo del docente.


## Configuración con OpenAI en Windows (Escritorio)

1. Descarga el ZIP y extráelo en el Escritorio. Abre PowerShell dentro de la carpeta `EduIA360_Cesim_Hospitality_Nivel3`.
2. Crea el entorno e instala dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Crea tu archivo privado de configuración y ábrelo:

```powershell
Copy-Item .env.example .env
notepad .env
```

4. En `.env`, sustituye `PEGA_AQUI_TU_CLAVE` por tu clave real de OpenAI, guarda y cierra el Bloc de notas. No pongas comillas y no compartas el archivo `.env`.
5. Inicia la aplicación:

```powershell
.\.venv\Scripts\python.exe -m uvicorn server:app --reload
```

6. Abre `http://127.0.0.1:8000` en el navegador. Deja abierta la ventana de PowerShell mientras usas la aplicación. Para detenerla, presiona `Ctrl+C`.

Modelo predeterminado: `gpt-4.1-mini`. Puedes cambiar `OPENAI_MODEL` en `.env` por otro modelo habilitado en tu cuenta de API. La API de OpenAI se cobra por separado de ChatGPT y necesita que la cuenta tenga acceso y facturación configurados.
