import tensorflow as tf
from data_transform import DataTransformer

def create_test_data(num_samples=100, img_size=32):
    images = tf.random.uniform([num_samples, img_size, img_size, 3], minval=0, maxval=255, dtype=tf.int32)
    labels = tf.random.uniform([num_samples], minval=0, maxval=10, dtype=tf.int32)
    dataset = tf.data.Dataset.from_tensor_slices((images, labels))
    return dataset

def test_resize_image():
    transformer = DataTransformer(img_size=64)
    image = tf.random.uniform([32, 32, 3], minval=0, maxval=255, dtype=tf.int32)
    resized_image = transformer.resize_image(image)
    assert resized_image.shape == (64, 64, 3), f"Formato esperado: (64, 64, 3), recebeu: {resized_image.shape}"

def test_load_and_preprocess_image():
    transformer = DataTransformer(img_size=32)
    image = tf.random.uniform([32, 32, 3], minval=0, maxval=255, dtype=tf.int32)
    label = tf.constant(1, dtype=tf.int32)
    processed_image, processed_label = transformer.load_and_preprocess_image(image, label)
    assert processed_image.shape == (32, 32, 3), f"Formato esperado: (32, 32, 3), recebeu: {processed_image.shape}"
    assert processed_image.dtype == tf.float32, f"Tipo esperado: tf.float32, recebeu: {processed_image.dtype}"
    assert processed_label == label, f"Rótulo esperado: {label}, recebeu: {processed_label}"

def test_split_dataset():
    dataset = create_test_data(num_samples=100)
    transformer = DataTransformer(img_size=32)
    train_ds, val_ds = transformer.split_dataset(dataset, train_split=0.8, val_split=0.2)
    assert train_ds.cardinality().numpy() == 80, f"Tamanho esperado do treino: 80, recebeu: {train_ds.cardinality().numpy()}"
    assert val_ds.cardinality().numpy() == 20, f"Tamanho esperado da validação: 20, recebeu: {val_ds.cardinality().numpy()}"

dataset = create_test_data()
for image, label in dataset.take(1):
    print(f"Image shape: {image.shape}, Label: {label.numpy()}")

if __name__ == "__main__":
    test_resize_image()
    test_load_and_preprocess_image()
    test_split_dataset()