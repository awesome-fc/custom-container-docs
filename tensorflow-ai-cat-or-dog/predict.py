import time, os
import tensorflow as tf
from skimage import io, transform
from scipy.misc import imresize
import numpy as np
from keras import backend as K


def predict(file_path, model_dir):
    K.clear_session()
    start = time.time()
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    from keras.models import model_from_json
    print("import keras time = ", time.time() - start)

    model = None
    # Getting model
    
    with open("%s/model.json" % model_dir, 'r') as f:
        model_content = f.read()
        model = model_from_json(model_content)
        # Getting weights
        model.load_weights("%s/weights.h5" % model_dir)
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    start = time.time()
    img_size = 64
    image = io.imread(file_path)

    if image.shape[2] == 4:  #ARGB
        tmp = transform.resize(image, (img_size, img_size, 3))
        img = imresize(tmp, (img_size, img_size, 3))
    else:
        img = imresize(image, (img_size, img_size, 3))

    X = np.zeros((1, 64, 64, 3), dtype='float64')
    X[0] = img
    Y = model.predict(X)
    return float(Y[0][0])
