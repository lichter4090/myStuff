from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist


def main(file_name):
    # Download the dataset and save it to local storage
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Preprocess the data
    x_train = x_train.reshape(-1, 28 * 28) / 255.0  # Flatten and normalize
    x_test = x_test.reshape(-1, 28 * 28) / 255.0
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    # Define the model
    model = Sequential([
        Flatten(input_shape=(28 * 28,)),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model offline
    model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

    model.save(file_name)


if __name__ == "__main__":
    main("model.h5")
