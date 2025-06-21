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
    input_path = "files/input/solicitudes_de_credito.csv"
    output_path = "files/output/solicitudes_de_credito.csv"

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Cargar el archivo
    df = pd.read_csv(input_path, sep=",", encoding="utf-8")

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Eliminar columnas completamente vacías (si existen)
    df = df.dropna(axis=1, how="all")

    # Eliminar filas completamente vacías
    df = df.dropna(axis=0, how="all")

    # Opcional: Eliminar filas con valores faltantes en columnas clave
    # (si conoces qué columnas son críticas, puedes especificarlas)
    df = df.dropna(
        subset=[
            "sexo",
            "tipo_de_emprendimiento",
            "idea_negocio",
            "barrio",
            "línea_crédito",
        ],
        how="any",
    )

    # Normalización de texto (opcional pero común)
    df["idea_negocio"] = df["idea_negocio"].str.lower().str.strip()
    df["barrio"] = df["barrio"].str.lower().str.strip()
    df["línea_crédito"] = df["línea_crédito"].str.lower().str.strip()

    # Guardar archivo limpio
    df.to_csv(output_path, index=False)
