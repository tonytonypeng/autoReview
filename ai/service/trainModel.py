import sys
import random
import pandas as pd
import numpy as np
from keras.models import  Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint,ReduceLROnPlateau
from keras.utils import np_utils
from keras import optimizers
import keras
from keras import layers

class reviewModel(object):
    def __init__(self):
        """初始化数据"""
        df = pd.read_csv('data/five_star_restaurants_reviews_only.csv')
        df = df.replace({r'\+':''},regex=True)
        mask = (df['text'].str.len() < 251)
        df1 = df.loc[mask]
        short_review = df1.sample(frac=1).reset_index(drop=True)
        short_review.to_csv('data/short_reviews_shuffle.txt', header=None, index=None, sep=' ')
        self.text = open('data/short_reviews_shuffle.txt').read()
        self.chars = sorted(list(set(self.text)))
        self.char_indices = dict((char,self.chars.index(char)) for char in self.chars)
        self.maxlen = 60
        self.step = 1
        self.callbacks_list = ''

    def getDataFromChunk(self,textChunk, maxlen=60, step=1):
        """构建数据结构"""
        sentences = []
        next_chars = []
        for i in range(0, len(textChunk) - maxlen, step):
            sentences.append(textChunk[i:i + maxlen])
            next_chars.append(textChunk[i + maxlen])
        print('nb sequences:', len(sentences))
        print('矢量化。。。。')
        X = np.zeros((len(sentences), maxlen, len(self.chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                X[i, t, self.char_indices[char]] = 1
                y[i, self.char_indices[next_chars[i]]] = 1
        return [X, y]

    def generateModels(self):
        self.model = keras.models.Sequential()
        self.model.add(layers.LSTM(1024, input_shape=(self.maxlen, len(self.chars)), return_sequences=True))
        self.model.add(layers.LSTM(1024, input_shape=(self.maxlen, len(self.chars))))
        self.model.add(layers.Dense(len(self.chars), activation='softmax'))
        optimizer = keras.optimizers.Adam(lr=0.001)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
        filepath = "Jul-7-all-{epoch:02d}-{loss:.4f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=1, min_lr=0.00001)
        self.callbacks_list = [checkpoint, reduce_lr]
        return self.model

    def sample(self, preds, temperature=1.0):
        """用给定的preds生成一些随机性，它是一个数字列表，如果温度是很小的，它总是会选择具有最高pred值的索引"""
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def trainModel(self):
        model = self.generateModels()
        for iteration in range(1, 20):
            print()
            print('-' * 50)
            print('Iteration', iteration)
            with open('data/short_reviews_shuffle.txt') as f:
                for chunk in iter(lambda: f.read(9000), ""):
                    X, y = self.getDataFromChunk(chunk)
                    self.model.fit(X, y, batch_size=128, epochs=1, callbacks=self.callbacks_list)

            start_index = random.randint(0, len(self.text) - self.maxlen - 1)
            generated_text = self.text[start_index:start_index + self.maxlen]
            print('----Generating with seed:"' + generated_text + '"')
            for temperature in [0.5, 0.8, 1.0]:
                print('------temperature:', temperature)
                sys.stdout.write(generated_text)

                for i in range(300):
                    sampled = np.zeros((1, self.maxlen, len(self.chars)))
                    for t, char in enumerate(generated_text):
                        sampled[0, t, self.char_indices[char]] = 1

                    preds = model.predict(sampled, verbose=0)[0]
                    next_index = self.sample(preds, temperature)
                    next_char = self.chars[next_index]

                    generated_text += next_char
                    generated_text = generated_text[1:]

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                return generated_text

    def testModel(self):
        """在不进行/完成训练时，使用这个测试输出。"""
        model = self.generateModels()
        start_index = random.randint(0, len(self.text) - self.maxlen - 1)
        generated_text = self.text[start_index: start_index + self.maxlen]
        print('--- Generating with seed: "' + generated_text + '"')

        for temperature in [0.5, 0.8, 1.0]:
            print('------ temperature:', temperature)
            sys.stdout.write(generated_text)

            # We generate 300 characters
            for i in range(300):
                sampled = np.zeros((1, self.maxlen, len(self.chars)))
                for t, char in enumerate(generated_text):
                    sampled[0, t, self.char_indices[char]] = 1.
                preds = model.predict(sampled, verbose=0)[0]
                next_index = self.sample(preds, temperature)
                next_char = self.chars[next_index]

                generated_text += next_char
                generated_text = generated_text[1:]

                sys.stdout.write(next_char)
                sys.stdout.flush()
            return generated_text