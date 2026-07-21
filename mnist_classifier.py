import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('mnist.xls')
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=50
)

X_train = X_train.reshape(-1, 784).astype('float32') / 255
X_test = X_test.reshape(-1, 784).astype('float32') / 255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

model = keras.Sequential([
    keras.Input(shape=(784,)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32
)

loss, accuracy = model.evaluate(X_test, y_test, verbose=1)

print(f"Accuracy: {accuracy:.4f}")
print(f"Loss: {loss:.4f}")

num = 10
indices = np.random.choice(len(X_test), num)
vis = X_test[indices].reshape(-1, 28, 28)

predictions = model.predict(X_test[indices], verbose=0)
predicted_labels = np.argmax(predictions, axis=1)

actual_labels = np.argmax(y_test[indices], axis=1)

fig, axes = plt.subplots(1, 10, figsize=(12, 5))

for i, ax in enumerate(axes):
    ax.imshow(vis[i], cmap='gray')
    ax.set_title(
    f"Actual: {actual_labels[i]}\nPredicted: {predicted_labels[i]}",
    fontsize=9)
    ax.axis("off")

plt.show()