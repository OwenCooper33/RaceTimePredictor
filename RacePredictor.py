import mysql.connector
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Connect to the database
def get_data_from_db():
    connection = mysql.connector.connect(
        host='your_host',
        user='your_username',
        password='your_password',
        database='your_database'
    )

    query = """
    SELECT distance, pace FROM AthletePerformance
    WHERE athlete_id = %s
    """
    athlete_id = 1  # Replace with the actual athlete ID

    data = pd.read_sql(query, connection, params=(athlete_id,))
    connection.close()
    return data

# Prepare the data
def prepare_data(data):
    X = data['distance'].values.reshape(-1, 1)
    y = data['pace'].values

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler

# Build the TensorFlow model
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    return model

# Train the model
def train_model(model, X_train, y_train):
    history = model.fit(X_train, y_train, epochs=100, validation_split=0.2, verbose=0)
    return model

# Predict the pace for a given distance
def predict_pace(model, distance, scaler):
    distance_array = np.array(distance).reshape(-1, 1)
    distance_scaled = scaler.transform(distance_array)
    predicted_pace = model.predict(distance_scaled)
    return predicted_pace

# Main function
def main():
    data = get_data_from_db()

    if data.empty:
        print("No data found for the specified athlete.")
        return

    X_train, X_test, y_train, y_test, scaler = prepare_data(data)

    model = build_model()
    model = train_model(model, X_train, y_train)

    # Evaluate the model
    loss = model.evaluate(X_test, y_test)
    print(f"Model test loss: {loss}")

    # Predict pace for a given distance
    distance_to_predict = 10  # e.g., predict pace for 10 km
    predicted_pace = predict_pace(model, distance_to_predict, scaler)
    print(f"Predicted pace for {distance_to_predict} km: {predicted_pace[0][0]:.2f} minutes per km")

if __name__ == "__main__":
    main()
