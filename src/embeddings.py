import PIL
import os
import numpy as np
from mtcnn import mtcnn
from silence_tensorflow import silence_tensorflow
silence_tensorflow()

def extract_face(filename, size=(160,160)):
    img = PIL.Image.open(filename).convert('RGB')
    pixels = np.asarray(img)
    det = mtcnn.MTCNN()
    results = det.detect_faces(pixels)

    x1, y1 , width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    face = pixels[y1: y1+height, x1:x1+width]
    img = PIL.Image.fromarray(face)
    img = img.resize(size)

    return np.asarray(img)

def load_faces(directory):
    faces = []
    files = os.listdir(directory)
    for filename in files:
        face = extract_face(os.path.join(directory, filename))
        faces.append(face)

    return faces

def load_dataset(directory):
    X, y = list(), list()

    for subdir in os.listdir(directory):
        faces = os.path.join(directory, subdir)
        faces = load_faces(faces)
        labels = [subdir for _ in range(len(faces))]
        X.extend(faces)
        y.extend(labels)

    return np.asarray(X), np.asarray(y)

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    
    face_pixels = (face_pixels - mean)/std
    samples = np.expand_dims(face_pixels, axis=0)

    yhat = model.predict(samples)
    return yhat[0]

if __name__ == '__main__':
    trainX, trainy = load_dataset('..\\data\\lovelyz\\train')
    print(trainX.shape, trainy.shape)

    testX, testy = load_dataset('..\\data\\lovelyz\\val')
    print(testX.shape, testy.shape)