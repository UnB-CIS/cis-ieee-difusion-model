import os
import tensorflow as tf
import tensorflow_datasets as tfds
from typing import Tuple

class DataTransformer:
    def __init__(self, img_size: int, resize_method: tf.image.ResizeMethod = tf.image.ResizeMethod.BILINEAR):
        self.img_size = img_size
        self.resize_method = resize_method

    def resize_image(self, image: tf.Tensor) -> tf.Tensor:
        return tf.image.resize(image, [self.img_size, self.img_size], method=self.resize_method)

    def load_and_preprocess_image(self, image: tf.Tensor, label: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        image = self.resize_image(image)
        image = tf.cast(image, tf.float32) / 255.0
        return image, label

    @staticmethod
    def split_dataset(dataset: tf.data.Dataset, train_split: float, val_split: float) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
        total_examples = dataset.cardinality().numpy()
        train_size = int(total_examples * train_split)
        val_size = int(total_examples * val_split)

        train_ds = dataset.take(train_size)
        remaining_ds = dataset.skip(train_size)
        val_ds = remaining_ds.take(val_size)

        return train_ds, val_ds

    def prepare_dataset(self, dataset: tf.data.Dataset, batch_size: int, train_split: float, val_split: float) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
        dataset = dataset.map(
            lambda image, label: self.load_and_preprocess_image(image, label),
            num_parallel_calls=tf.data.AUTOTUNE
        )
        train_ds, val_ds = self.split_dataset(dataset, train_split, val_split)
        train_ds = train_ds.shuffle(1000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
        val_ds = val_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
        return train_ds, val_ds