import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def preprocess(raw_data_path, output_path):
    # Leer datos
    df = pd.read_csv(os.path.join(raw_data_path, "titanic.csv"))

    # Limpieza de datos
    df = df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1)
    df["Age"].fillna(df["Age"].median(), inplace=True)
    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    # Codificación de variables categóricas
    le = LabelEncoder()
    df["Sex"] = le.fit_transform(df["Sex"])
    df["Embarked"] = le.fit_transform(df["Embarked"])

    # Dividir en train y test
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    # Guardar datos procesados
    os.makedirs(os.path.join(output_path, "train"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "test"), exist_ok=True)

    train.to_csv(os.path.join(output_path, "train/train.csv"), index=False)
    test.to_csv(os.path.join(output_path, "test/test.csv"), index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, dest="raw_data_path")
    parser.add_argument("--output-data", type=str, dest="output_path")
    args = parser.parse_args()

    preprocess(args.raw_data_path, args.output_path)
