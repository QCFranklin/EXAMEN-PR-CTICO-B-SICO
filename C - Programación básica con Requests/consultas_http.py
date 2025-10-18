import requests

def get_status(url):
    # Devuelve el código de estado HTTP de la URL.
    try:
        respuesta = requests.get(url, timeout=10)
        return respuesta.status_code
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_headers(url):
    # Devuelve un diccionario con los headers de respuesta.
    
    try:
        respuesta = requests.get(url, timeout=10)
        return dict(respuesta.headers)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_keyword_count(url, palabra):
    # Cuenta cuántas veces aparece una palabra en el texto HTML (case-insensitive).
    try:
        respuesta = requests.get(url, timeout=10)
        html_text = respuesta.text.lower()
        palabra_lower = palabra.lower()
        return html_text.count(palabra_lower)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# --- PRUEBAS ---
if __name__ == "__main__":
    url = "https://example.com"

    # Ejecutar funciones y capturar resultados
    status = get_status(url)
    headers = get_headers(url)
    keyword_count = get_keyword_count(url, "example")

    # Formatear salida
    salida = (
        f"=== RESULTADOS ===\n"
        f"Código de estado HTTP: {status}\n"
        f"\nHeaders de respuesta:\n{headers}\n"
        f"\nApariciones de 'example' en el HTML: {keyword_count}\n"
    )

    # Imprimir en consola
    print(salida)

    # Guardar en archivo salida.txt
    with open("salida.txt", "w", encoding="utf-8") as f:
        f.write(salida)

    print("\n Resultados guardados en salida.txt")