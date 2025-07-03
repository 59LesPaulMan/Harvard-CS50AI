# Traffic Sign Classifier

This project used a German traffic signs. The data was located within the /gtsrb folder with 43 folders category folders each containing 150 images for a total of 6,450 images.  Within the python program, cv2 was used to read and resize images.  Also, numpy was used to handle image data as arrages.  The os was used to help file system manipulation of data folders and files to keep the program portable, testable and easier to read.  The sys was used to accept arguments.  Tensorflow and scikit-learn were also used to build and train a CNN neural network and scikit-learn for the splitting of data into testing groups.

In essence, the code follows:

1. Load and process data
2. Splint into training and test sets
3. Build a CNN model
4. Train the model on training data
5. Evaluate the unseen test data
6. Save the trained model (option)

Global settings:
Ephoch = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

The Convolutional Neural Network (CNN) was setup following the handwriting experiment during the class lecture and study.

32 Filters of 3x3 size were used to scan over images:
    tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(30, 30, 3)),

Sequential with Conv2D, Maxpooling, Flattening as follows:

    TENSORFLOW SEQUENTIAL CNN
    model = tf.keras.models.Sequential([
    
    2D CONV
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(30, 30, 3)),

    MAX POOLING
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    FLATTEN
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),

    DROPOUT - 50%
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(43, activation="softmax")
    ])
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

This is not yied very successful results.  The results were as follows:
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 6ms/step - accuracy: 0.0508 - loss: 8.1013     
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 3s 6ms/step - accuracy: 0.0524 - loss: 3.6055 
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.0569 - loss: 3.5469 
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0554 - loss: 3.5238 
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.0555 - loss: 3.5096  
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.0591 - loss: 3.5005 
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.0572 - loss: 3.4935 
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 8ms/step - accuracy: 0.0551 - loss: 3.4930 
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0576 - loss: 3.4935 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 7ms/step - accuracy: 0.0538 - loss: 3.4992  
333/333 - 1s - 2ms/step - accuracy: 0.0569 - loss: 3.5023
Model saved to model.keras.

As you can observe, the model only achieved 57% accuracey bouncing back and forth from 50% to as high as 59%.

Suggest - add layers to the CNN.

Adding layers to the CNN was coded with:

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(30, 30, 3)),

    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    tf.keras.layers.Dense(43, activation="softmax")
])

This resulting in an increase to 97% accuracy:

kevinvia@MacBookAir traffic % python traffic.py gtsrb model.keras
Epoch 1/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 8ms/step - accuracy: 0.1753 - loss: 4.3651         
Epoch 2/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.6171 - loss: 1.3260  
Epoch 3/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.8014 - loss: 0.6750
Epoch 4/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.8782 - loss: 0.4104  
Epoch 5/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 4s 9ms/step - accuracy: 0.9079 - loss: 0.3296 
Epoch 6/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.9165 - loss: 0.2978 
Epoch 7/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 10ms/step - accuracy: 0.9355 - loss: 0.2229 
Epoch 8/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.9409 - loss: 0.2098 
Epoch 9/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.9465 - loss: 0.1837 
Epoch 10/10
500/500 ━━━━━━━━━━━━━━━━━━━━ 5s 9ms/step - accuracy: 0.9535 - loss: 0.1632  
333/333 - 1s - 4ms/step - accuracy: 0.9714 - loss: 0.1240
Model saved to model.keras.
kevinvia@MacBookAir traffic % 



