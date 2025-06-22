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
    raw_data = pd.read_csv(input_path, sep=";")

    # Remove unnecessary column
    raw_data.drop(columns=["Unnamed: 0"], inplace=True)

    # Remove rows with missing data and duplicates
    raw_data.dropna(inplace=True)
    raw_data.drop_duplicates(inplace=True)

    # Fix date format
    raw_data[["day", "month", "year"]] = raw_data["fecha_de_beneficio"].str.split(
        "/", expand=True
    )
    short_year_condition = raw_data["year"].str.len() < 4
    raw_data.loc[short_year_condition, ["day", "year"]] = raw_data.loc[
        short_year_condition, ["year", "day"]
    ].values
    raw_data["fecha_de_beneficio"] = (
        raw_data["year"] + "-" + raw_data["month"] + "-" + raw_data["day"]
    )
    raw_data.drop(columns=["day", "month", "year"], inplace=True)

    # Normalize text in categorical columns
    text_columns = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]
    raw_data[text_columns] = raw_data[text_columns].apply(
        lambda col: col.str.lower().replace(["-", "_"], " ", regex=True).str.strip()
    )
    raw_data["barrio"] = (
        raw_data["barrio"].str.lower().replace(["-", "_"], " ", regex=True)
    )

    # Clean and convert credit amount
    raw_data["monto_del_credito"] = (
        raw_data["monto_del_credito"].str.replace("[$, ]", "", regex=True).str.strip()
    )
    raw_data["monto_del_credito"] = (
        pd.to_numeric(raw_data["monto_del_credito"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
    raw_data["monto_del_credito"] = (
        raw_data["monto_del_credito"].astype(str).str.replace(".00", "")
    )

    # Remove duplicates again
    raw_data.drop_duplicates(inplace=True)

    # Create output folder if it doesn't exist
    output_path = "files/output"
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, "solicitudes_de_credito.csv")
    raw_data.to_csv(output_file, sep=";", index=False)

    return raw_data.head()
