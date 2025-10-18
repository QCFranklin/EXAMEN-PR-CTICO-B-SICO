# <center>UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO</center>
## <center>FINESI</center>
Docente: Aleman Gonzales Leonid <br> Estudiante: Queccara Condori Franklin - 222147

# Informe: Consumo de la API pública Open-Meteo para datos climáticos en Puno, Perú

Esta práctica describe el proceso de consumo de la API pública **Open-Meteo** (https://open-meteo.com/), una plataforma de datos meteorológicos abierta, sin autenticación ni clave de API. Se utilizó para obtener datos horarios de temperatura en **Puno, Perú**, durante los últimos **30 días**, con el objetivo de normalizar la respuesta, exportarla a CSV y generar una visualización básica.

## Endpoint y parámetros utilizados

### Endpoint principal
```
GET https://api.open-meteo.com/v1/forecast
```

### Parámetros de la solicitud
| Parámetro        | Valor               | Descripción |
|------------------|---------------------|-------------|
| `latitude`       | `-15.8397`          | Latitud de Puno (15°50′23″S) |
| `longitude`      | `-70.0217`          | Longitud de Puno (70°01′18″O) |
| `hourly`         | `temperature_2m`    | Variable meteorológica solicitada (temperatura a 2 m del suelo) |
| `past_days`      | `30`                | Incluye datos históricos de los últimos 30 días |
| `timezone`       | `auto`              | Ajusta automáticamente la zona horaria local (UTC-5 para Puno) |

Este conjunto de parámetros permite obtener una serie temporal horaria de temperatura, con fechas en formato ISO 8601 y valores en grados Celsius.

## Estructura de la respuesta

La API devuelve un objeto JSON con esta estructura simplificada:

```json
{
  "latitude": -15.8397,
  "longitude": -70.0217,
  "hourly": {
    "time": ["2024-05-02T00:00", "2024-05-02T01:00", ..., "2024-06-01T23:00"],
    "temperature_2m": [8.2, 7.9, 7.1, ..., 12.4]
  }
}
```

Los datos están organizados en **listas paralelas**: el índice `i` en `time` corresponde al mismo índice en `temperature_2m`. Esta estructura requiere **normalización** para su uso en análisis tabular.

## Normalización y exportación

El script convierte las listas en un **DataFrame plano** con dos columnas:
- `time`: marca de tiempo (tipo `datetime`)
- `temperature_2m`: valor numérico de temperatura (°C)

Este DataFrame se exporta a `01.1_puno_weather.csv` sin índice, generando aproximadamente **720 filas** (24 horas × 30 días). El archivo resultante es compatible con Excel, Google Sheets, pandas y otras herramientas de análisis.

## Manejo de errores

El script incluye manejo básico pero robusto de errores comunes:

- **Fallo de conexión**: captura `requests.exceptions.RequestException` (timeout, DNS error, etc.).
- **Respuesta HTTP no exitosa**: usa `response.raise_for_status()` para detectar códigos 4xx/5xx.
- **JSON inválido o incompleto**: verifica la presencia de la clave `"hourly"` antes de procesar.
- **Datos vacíos**: evita graficar o guardar si no hay registros.

Esto garantiza que el script no falle silenciosamente y proporcione retroalimentación clara al usuario.

## Límites de la API

Open-Meteo impone ciertos límites técnicos y de uso:

- **Rate limiting**: ~10–20 solicitudes por segundo por IP (útil para esta práctica encargada).
- **Rango temporal**:  
  - Datos históricos: hasta **92 días** hacia atrás, según web.  
  - Pronóstico: hasta **16 días** hacia adelante.  
  → El uso de `past_days=30` está bien dentro de estos límites.
- **Sin autenticación**, pero **prohibido el scraping masivo o comercial** sin autorización.
- **Precisión**: los datos provienen de modelos meteorológicos (ECMWF, GFS), no de estaciones locales, por lo que pueden tener ligeras desviaciones respecto a mediciones reales en Puno.

## Conclusión

La API de Open-Meteo resultó ideal para esta tarea: es **pública, ética, sin barreras técnicas** y proporciona datos estructurados de alta utilidad. El flujo implementado (consumo → normalización → CSV → gráfico) demuestra un pipeline completo de integración de APIs públicas, cumpliendo con todos los entregables solicitados.

> **Archivos generados**:  
> - `openMeteoPuno.py` (script funcional)  
> - `01.1_puno_weather.csv` (≥720 registros)  
> - `01.2_puno_temperature.png` (gráfico de línea)
 
    