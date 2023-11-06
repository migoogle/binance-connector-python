import requests
import pandas as pd
import numpy as np
import spacy

# Carga el modelo de lenguaje de spaCy
nlp = spacy.load("es_core_news_sm")

# URLs de las APIs para obtener el valor del USDT, dólar blue y dólar MEP en ARS
usdt_url = "https://criptoya.com/api/usdt/ars/0.1"
blue_url = "https://dolarapi.com/v1/dolares/blue"
mep_url = "https://dolarapi.com/v1/dolares/bolsa"

def obtener_datos_mercados():
    try:
        # Realiza una solicitud GET para obtener el valor del USDT en ARS
        usdt_response = requests.get(usdt_url)

        # Realiza una solicitud GET para obtener el valor del dólar blue en ARS
        blue_response = requests.get(blue_url)

        # Realiza una solicitud GET para obtener el valor del dólar MEP en ARS
        mep_response = requests.get(mep_url)

        # Verifica si todas las solicitudes fueron exitosas (código de respuesta 200)
        if (
            usdt_response.status_code == 200
            and blue_response.status_code == 200
            and mep_response.status_code == 200
        ):
            # Analiza las respuestas JSON
            usdt_data = usdt_response.json()
            blue_data = blue_response.json()
            mep_data = mep_response.json()

            # Agrega el mercado "lemoncash" al DataFrame
            data = {
                "Mercado": ["USDT", "Blue", "MEP", "BinanceP2P", "Lemoncash"],
                "Compra": [
                    usdt_data["binance"]["bid"],
                    blue_data["compra"],
                    mep_data["compra"],
                    usdt_data["binancep2p"]["bid"],
                    usdt_data["lemoncash"]["bid"],
                ],
                "Venta": [
                    usdt_data["binance"]["ask"],
                    blue_data["venta"],
                    mep_data["venta"],
                    usdt_data["binancep2p"]["ask"],
                    usdt_data["lemoncash"]["ask"],
                ],
            }
            df = pd.DataFrame(data)
            return df
        else:
            print(
                f"Error en una de las solicitudes: Código de respuesta {usdt_response.status_code}/{blue_response.status_code}/{mep_response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

def obtener_recomendacion(df):
    if df is not None:
        # Buscar el mejor mercado para comprar y el mejor mercado para vender
        min_compra = df["Venta"].min()
        max_venta = df["Compra"].max()

        mejores_compra = df[df["Venta"] == min_compra]
        mejores_venta = df[df["Compra"] == max_venta]

        # Encontrar combinaciones óptimas de compra y venta
        ganancias = []
        for _, compra_row in mejores_compra.iterrows():
            for _, venta_row in mejores_venta.iterrows():
                ganancia = venta_row["Compra"] - compra_row["Venta"]
                ganancias.append((compra_row["Mercado"], venta_row["Mercado"], ganancia))

        # Encontrar la combinación con la máxima ganancia
        mejor_combinacion = max(ganancias, key=lambda x: x[2])
        return f"Comprar {mejor_combinacion[0]} y vender {mejor_combinacion[1]} para obtener una ganancia de {mejor_combinacion[2]:.2f} ARS por cada USD"
    else:
        return "No se pudieron obtener los datos de los mercados."

def responder_pregunta(texto_pregunta, df):
    doc = nlp(texto_pregunta)

    for token in doc:
        # Buscar palabras clave en la pregunta para determinar la acción del usuario
        if token.text.lower() == "recomendación":
            return obtener_recomendacion(df)
        elif token.text.lower() == "valores":
            return df.to_string()
        elif token.text.lower() == "ayuda":
            return "Puedes preguntar sobre recomendaciones o valores de compra y venta."

    return "No entiendo la pregunta. Puedes preguntar sobre recomendaciones o valores de compra y venta."

if __name__ == "__main__":
    df = obtener_datos_mercados()
    if df is not None:
        print("¡Hola! Soy tu asistente financiero. Puedes preguntarme sobre recomendaciones o valores de compra y venta.")
        while True:
            pregunta = input("Tu pregunta: ")
            respuesta = responder_pregunta(pregunta, df)
            print("Respuesta:", respuesta)
