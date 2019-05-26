import os
import pandas as pd
import librosa
import librosa.display
import numpy as np
import keras
from sklearn.preprocessing import LabelEncoder

from config import settings

def extract_emotion(file_name):
    #print("voice_test 경로", os.path.dirname( os.path.abspath( __file__ ) ))

    WAV_FILE_PATH = os.path.join(settings.MEDIA_ROOT , file_name)

    # mfcc로 특징 추출
    X, sample_rate = librosa.load(WAV_FILE_PATH, res_type='kaiser_fast', duration=2.5, sr=22050*2, offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
    featurelive = mfccs
    livedf2 = featurelive


    # shape (216,0)으로 맞추기
    array_len = len(livedf2)
    count = array_len%216

    if int(array_len/216) > 0:
        for i in range(count):
            livedf2 = np.delete(livedf2, [len(livedf2)-1])
    else:
        for i in range(216 - count):
            livedf2 = np.append(livedf2, 0)

    array_len = len(livedf2)

    # DataFrame 객체 생성
    livedf2 = pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T

    # 모델 불러오기
    from keras.models import model_from_json
    json_file = open(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ),'saved_models/model.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(os.path.join(os.path.dirname( os.path.abspath( __file__ ) ),'saved_models/Emotion_Voice_Detection_Model.h5'))

    # evaluate loaded model on test data
    opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)
    loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    # 배열의 차원 확장하기
    twodim = np.expand_dims(livedf2, axis=2)

    # 테스트 데이터 예측
    livepreds = loaded_model.predict(twodim, batch_size=32, verbose=1)

    livepreds1=livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()

    # 라벨 리스트
    labels = ['female_angry', 'female_calm', 'female_fearful', 'female_happy', 'female_sad', 'male_angry', 'male_calm', 'male_fearful', 'male_happy', 'male_sad']

    lb = LabelEncoder()
    lb.fit(labels)
    livepredictions = (lb.inverse_transform(liveabc))

    print('livepredictions: ',livepredictions)

    emotion_prediction = livepredictions[0].split('_')[1]
    return emotion_prediction

if __name__ == '__main__':
    print(extract_emotion('../.media_root/001.wav'))