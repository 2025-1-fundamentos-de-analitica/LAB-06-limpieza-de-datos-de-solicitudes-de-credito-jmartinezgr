"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    ruta_entrada = "files/input/solicitudes_de_credito.csv"
    datos_raw = pd.read_csv(ruta_entrada, sep=";")

    # Eliminar columna innecesaria si existe
    if "Unnamed: 0" in datos_raw.columns:
        datos_raw.drop(columns=["Unnamed: 0"], inplace=True)

    # Eliminar filas con datos faltantes y duplicados
    datos_raw.dropna(inplace=True)
    datos_raw.drop_duplicates(inplace=True)

    # Corregir formato de fecha
    datos_raw[["dia", "mes", "anio"]] = datos_raw["fecha_de_beneficio"].str.split(
        "/", expand=True
    )

    # Ajustar fechas con año de 2 dígitos
    condicion_anio_corto = datos_raw["anio"].str.len() < 4
    datos_raw.loc[condicion_anio_corto, ["dia", "anio"]] = datos_raw.loc[
        condicion_anio_corto, ["anio", "dia"]
    ].values

    # Formatear la fecha a YYYY-MM-DD
    datos_raw["fecha_de_beneficio"] = (
        datos_raw["anio"] + "-" + datos_raw["mes"] + "-" + datos_raw["dia"]
    )
    datos_raw.drop(columns=["dia", "mes", "anio"], inplace=True)

    # Normalizar texto en columnas categóricas
    columnas_texto = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]
    datos_raw[columnas_texto] = datos_raw[columnas_texto].apply(
        lambda col: col.str.lower().replace(["-", "_"], " ", regex=True).str.strip()
    )
    datos_raw["barrio"] = (
        datos_raw["barrio"].str.lower().replace(["-", "_"], " ", regex=True).str.strip()
    )

    # Limpiar y convertir monto de crédito
    datos_raw["monto_del_credito"] = (
        datos_raw["monto_del_credito"].str.replace(r"[$, ]", "", regex=True).str.strip()
    )
    datos_raw["monto_del_credito"] = (
        pd.to_numeric(datos_raw["monto_del_credito"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    # Eliminar duplicados nuevamente por seguridad
    datos_raw.drop_duplicates(inplace=True)

    # Crear carpeta de salida si no existe
    ruta_salida = "files/output"
    os.makedirs(ruta_salida, exist_ok=True)

    # Guardar el archivo limpio
    archivo_salida = os.path.join(ruta_salida, "solicitudes_de_credito.csv")
    datos_raw.to_csv(archivo_salida, sep=";", index=False)
