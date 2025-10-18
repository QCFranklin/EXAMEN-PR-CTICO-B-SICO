import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_weather_data(lat, lon):
    #Obtiene datos horarios de temperatura de los últimos 30 días desde Open-Meteo.
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "past_days": 30,        # Incluye datos históricos de los últimos 30 días
        "timezone": "auto"     # Ajusta la zona horaria local automáticamente
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None


def normalize_data(data):
    # Convierte el JSON de Open-Meteo en un DataFrame plano.
    if not data or "hourly" not in data:
        print("Datos inválidos o incompletos.")
        return pd.DataFrame()

    hourly = data["hourly"]
    df = pd.DataFrame({
        "time": hourly.get("time", []),
        "temperature_2m": hourly.get("temperature_2m", [])
    })

    # Convertir columna de tiempo a datetime
    df["time"] = pd.to_datetime(df["time"])
    return df


def save_to_csv(df, filename="01.1_puno_weather.csv"):
    #Guarda el DataFrame en CSV.
    df.to_csv(filename, index=False)
    print(f"Datos guardados en {filename}")


def plot_temperature(df, filename="01.2_puno_temperature.png"):
    #Genera y guarda un gráfico de temperatura horaria.
    if df.empty:
        print("No hay datos para graficar.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df["time"], df["temperature_2m"], color="#1f77b4", linewidth=1.2)
    plt.title("Temperatura horaria en Puno, Perú (últimos 30 días)", fontsize=14, pad=20)
    plt.xlabel("Fecha y hora")
    plt.ylabel("Temperatura (°C)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Gráfico guardado como {filename}")


def main():
    LAT = -15.8397
    LON = -70.0217

    print("Obteniendo datos climáticos de Puno desde Open-Meteo...")
    raw_data = fetch_weather_data(LAT, LON)

    if raw_data is None:
        return

    df = normalize_data(raw_data)
    if df.empty:
        return

    print(f"Se obtuvieron {len(df)} registros horarios.")
    save_to_csv(df)
    plot_temperature(df)


if __name__ == "__main__":
    main()