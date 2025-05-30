# Use Metal Performance Shaders
import tensorflow as tf
tf.config.experimental.enable_tensor_float_32_execution(False)

# Optimize memory usage
tf.config.experimental.set_memory_growth(gpu, True)

# Use efficient data loading
tf.data.Dataset.from_tensor_slices().batch(32).prefetch(tf.data.AUTOTUNE)

print("TensorFlow version:", tf.__version__)
print("GPUs:", tf.config.list_physical_devices('GPU'))