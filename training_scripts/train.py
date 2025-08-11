import argparse
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train(train_path, test_path, model_path, n_estimators, min_samples_leaf, random_state):
    # Leer datos
    train_data = pd.read_csv(os.path.join(train_path, "train.csv"))
    test_data = pd.read_csv(os.path.join(test_path, "test.csv"))

    # Separar características y objetivo
    X_train = train_data.drop("Survived", axis=1)
    y_train = train_data["Survived"]
    X_test = test_data.drop("Survived", axis=1)
    y_test = test_data["Survived"]

    # Entrenar modelo
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    # Evaluar modelo
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy}")

    # Guardar modelo
    os.makedirs(model_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_path, "model.joblib"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Hyperparameters
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--min-samples-leaf", type=int, default=3)
    parser.add_argument("--random-state", type=int, default=42)

    # Paths
    parser.add_argument("--train", type=str, dest="train_path")
    parser.add_argument("--test", type=str, dest="test_path")
    parser.add_argument("--model-dir", type=str, dest="model_path", default=os.environ.get("SM_MODEL_DIR"))

    args = parser.parse_args()

    train(
        args.train_path,
        args.test_path,
        args.model_path,
        args.n_estimators,
        args.min_samples_leaf,
        args.random_state
    )
