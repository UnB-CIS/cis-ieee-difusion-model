import tensorflow as tf
from data_transform import DataTransformer

def test_data_transformer():
    img_size = 32
    batch_size = 64
    train_split = 0.8
    val_split = 0.2
    resize_method = tf.image.ResizeMethod.NEAREST_NEIGHBOR

    transformer = DataTransformer(img_size, resize_method)
    
    # Carrega o CIFAR-10 primeiro
    dataset = transformer.load_cifar10()
    train_ds, _ = transformer.prepare_dataset(dataset, batch_size, train_split, val_split)
    
    # Checa o tamanho e formato das imagens
    for images, labels in train_ds.take(1):
        assert images.shape == (batch_size, img_size, img_size, 3), f"Formato esperado: {(batch_size, img_size, img_size, 3)}, recebido: {images.shape}"
        assert labels.shape == (batch_size,), f"Formato esperado: {(batch_size,)}, recebido: {labels.shape}"

if __name__ == "__main__":
    test_data_transformer()