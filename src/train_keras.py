import numpy as np
from numpy.lib.npyio import load
import tensorflow as tf
from tensorflow import keras
from embeddings import load_dataset, get_embedding
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import svm
import joblib
import pickle

def get_data(model, train_path, val_path):
    trainX, trainy = load_dataset(train_path)
    testX, testy = load_dataset(val_path)

    newTrainX = []
    for face_pixels in trainX:
        embedding = get_embedding(model, face_pixels)
        newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)
    
    newTestX = []
    for face_pixels in testX:
        embedding = get_embedding(model, face_pixels)
        newTestX.append(embedding)
    newTestX = np.asarray(newTestX)
    
    return newTrainX, trainy, newTestX, testy
    
def main():
    model = keras.models.load_model('facenet_keras.h5')
    trainX, trainy, testX, testy = get_data(model, 
                                    '..\\data\\lovelyz\\train',
                                    '..\\data\\lovelyz\\val')
    in_encoder = preprocessing.Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)

    out_encoder = preprocessing.LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
    out_encoder_file = open('lovelyz_labeler.pkl', 'wb')
    pickle.dump(out_encoder, out_encoder_file)
    out_encoder_file.close()

    # fit model
    classifier = svm.SVC(kernel='linear', probability=True)
    classifier.fit(trainX, trainy)

    # predict
    yhat_train = classifier.predict(trainX)
    score_train = accuracy_score(trainy, yhat_train)
    
    yhat_test = classifier.predict(testX)
    score_test = accuracy_score(testy, yhat_test)

    print("Accuracy: train=%.3f, test=%.3f" % (score_train*100, score_test*100))
    joblib.dump(classifier, 'lovelyz_classifier.pkl')

if __name__ == '__main__':
    main()