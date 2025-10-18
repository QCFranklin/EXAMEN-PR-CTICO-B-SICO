# Open-Meteo: Datos climáticos de Puno, Perú

Esta práctica del curso Ciencia de datos consume la API pública de [Open-Meteo](https://open-meteo.com/) —**sin autenticación ni clave**— para obtener datos horarios de temperatura en **Puno, Perú**, durante los **últimos 30 días**, y genera un archivo CSV + gráfico de tendencia.

## Coordenadas usadas
- **Latitud**: `-15.8397` (15°50′23″S)  
- **Longitud**: `-70.0217` (70°01′18″O)

## Requisitos
- Python 3.7+
- Paquetes: `requests`, `pandas`, `matplotlib`

Instálamos con:
```bash
pip install requests pandas matplotlib
```

## Ejecución
```bash
python 01_openMeteoPuno.py
```

## Salidas generadas
- `puno_weather.csv`: datos horarios de temperatura (720+ registros).
- `puno_temperature.png`: gráfico de línea de temperatura vs. tiempo.

## Notas
- La API **no requiere clave** y respeta el estándar ético de uso público.
- Se obtienen datos de los **últimos 30 días** (`past_days=30`).
- La zona horaria se ajusta automáticamente según la ubicación (`timezone=auto`).

---

## Explicación del script `01_openMeteoPuno.py`

### 1. **Encabezado y dependencias**
```python
import requests      # Para hacer solicitudes HTTP a la API
import pandas as pd  # Para manipular y exportar datos estructurados
import matplotlib.pyplot as plt  # Para generar gráficos
```
> Se importan las librerías esenciales para consumir la API, normalizar datos y visualizar.

---

### 2. **Función `fetch_weather_data(lat, lon)`**
```python
def fetch_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "past_days": 30,
        "timezone": "auto"
    }
    ...
```
> - Construye la URL con parámetros.
> - `past_days=30`: solicita datos históricos de los últimos **30 días** (720 horas aprox.).
> - `timezone="auto"`: devuelve las fechas en la zona horaria local de Puno (UTC-5).
> - Incluye manejo de errores (`try/except`) para fallos de red o respuestas inválidas.

---

### 3. **Función `normalize_data(data)`**
```python
def normalize_data(data):
    hourly = data["hourly"]
    df = pd.DataFrame({
        "time": hourly.get("time", []),
        "temperature_2m": hourly.get("temperature_2m", [])
    })
    df["time"] = pd.to_datetime(df["time"])
    return df
```
> - Convierte las listas paralelas (`time`, `temperature_2m`) en un **DataFrame plano**.
> - Cada fila representa una medición horaria.
> - La columna `time` se convierte a tipo `datetime` para facilitar el gráfico y análisis.

---

### 4. **Función `save_to_csv(df, filename)`**
```python
def save_to_csv(df, filename="01.1_puno_weather.csv"):
    df.to_csv(filename, index=False)
```
> - Exporta los datos normalizados a un archivo CSV sin índice.
> - Resultado: archivo listo para análisis en Excel, Google Sheets o herramientas de BI.

---

### 5. **Función `plot_temperature(df, filename)`**
```python
def plot_temperature(df, filename="01.2_puno_temperature.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["temperature_2m"], color="#1f77b4", linewidth=1.2)
    plt.title("Temperatura horaria en Puno, Perú (últimos 30 días)", fontsize=14)
    plt.xlabel("Fecha y hora")
    plt.ylabel("Temperatura (°C)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
```
> - Genera un **gráfico de línea** suave que muestra la evolución de la temperatura.
> - Incluye título centrado, etiquetas claras y cuadrícula para mejor lectura.
> - Guarda la imagen en alta resolución (`dpi=150`).

---

### 6. **Función `main()`**
```python
def main():
    LAT = -15.8397
    LON = -70.0217
    raw_data = fetch_weather_data(LAT, LON)
    df = normalize_data(raw_data)
    save_to_csv(df)
    plot_temperature(df)
```
> - Punto de entrada del script.
> - Define las coordenadas de Puno.
> - Encadena la obtención, normalización, exportación y visualización.

---

### 7. **Bloque de ejecución**
```python
if __name__ == "__main__":
    main()
```
> - Permite ejecutar el script directamente desde la terminal.

---