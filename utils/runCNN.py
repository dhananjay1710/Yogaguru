from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16
import numpy as np

def extract_features(directory, sample_count, datagen, conv_base, batch_size):
    features = np.zeros(shape = (sample_count, 4, 4, 512))
    labels = np.zeros(shape = (sample_count, 1))
    #labels = np.zeros(shape = (sample_count, 2)) edited to two as my custom image directory has only two classes.
    generator = datagen.flow_from_directory(directory, target_size = (150, 150), batch_size = batch_size, class_mode="categorical",subset = "training")
    i = 0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size: (i+1) * batch_size] = features_batch
        labels[i * batch_size: (i+1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:
            break
    return features, labels


def run_cnn():
    conv_base = VGG16(weights = 'imagenet', include_top = False, input_shape = (150, 150, 3))
    model = load_model('models/YogaPoseClassifierRegularCustomDB.h5')
    datagen = ImageDataGenerator(rescale = 1./255)
    batch_size = 20
    test_dir = 'static/UserUpload'
    test_features, test_labels = extract_features(test_dir, 1, datagen, conv_base, batch_size)
    test_features = np.reshape(test_features, (1, 4 * 4 * 512))
    output_class = model.predict(test_features)
    poses = ['Goddess', 'Half Moon', 'Tree', 'Triangle', 'Warrior2']
    output_idx = np.argmax(output_class[0])
    input_pose = poses[output_idx]
    return input_pose