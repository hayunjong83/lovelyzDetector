import joblib
import os
import numpy as np
from embeddings import extract_face, get_embedding
from tensorflow import keras
from PIL import Image, ImageDraw, ImageFont
from mtcnn import mtcnn
from sklearn import preprocessing

model = keras.models.load_model('facenet_keras.h5')
classifier = joblib.load('lovelyz_classifier.pkl')
out_encoder = joblib.load('lovelyz_labeler.pkl')

def predict(path):
    face = extract_face(path)
    embedding = get_embedding(model, face)
    embedding = np.expand_dims(embedding, axis=0)

    in_encoder = preprocessing.Normalizer(norm='l2')
    embedding = in_encoder.transform(embedding)

    yhat = classifier.predict(embedding)
    prob = classifier.predict_proba(embedding)
    label = out_encoder.inverse_transform(yhat)

    print("%s \n >Predicted: %s (%.3f)" % 
            (path.split(os.sep)[-1], label[0], prob[0][yhat]*100))
    
    # draw results on image
    img = Image.open(path)
    det = mtcnn.MTCNN()
    results = det.detect_faces(np.asarray(img))
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((x1,y1), (x1+width, y1+height)), outline=(255,0,0), width=3)
    draw.rectangle(((x1,y1-height//10),(x1+width//2, y1)), fill=(255,0,0))
    font = ImageFont.truetype('arial.ttf', height//10)
    draw.text((x1, y1-height//10), label[0], fill=(255,255,255), font=font)
    img.save(path.split(os.sep)[-1].split('.')[0]+'_result.jpg')

def main():
    test1_path = '..\\data\\lovelyz\\test1.jpg'
    predict(test1_path)

    test2_path = '..\\data\\lovelyz\\test2.jpg'
    predict(test2_path)

if __name__ == '__main__':
    main()