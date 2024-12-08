import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Step 1: Load the trained model
model = load_model(r".")
print("Model loaded successfully!")

# Step 2: Define the test dataset path
test_dir = r"."
if not os.path.exists(test_dir):
    raise FileNotFoundError(f"Test data not found at: {test_dir}")

# Step 3: Prepare the test data
test_datagen = ImageDataGenerator(rescale=1.0/255)  # Normalize pixel values

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(150, 150),  # Same as the input size used during training
    batch_size=32,
    class_mode='binary',
    shuffle=False  # Ensure no shuffling for consistent evaluation
)

# Step 4: Evaluate the model on the test data
loss, accuracy = model.evaluate(test_generator)
print(f"Test Accuracy: {accuracy:.2f}")
print(f"Test Loss: {loss:.2f}")

# Optional: Display predictions and filenames for the test data
predictions = model.predict(test_generator)
predicted_classes = ["Clean" if pred > 0.5 else "Dirty" for pred in predictions]

# Display filenames and corresponding predictions
for filename, pred_class in zip(test_generator.filenames, predicted_classes):
    print(f"Filename: {filename}, Predicted: {pred_class}")

