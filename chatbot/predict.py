import json
import string
import random 
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer 
import tensorflow as tensorF
from tensorflow import keras
import pickle
import tflearn
import os
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense, Dropout
lm = WordNetLemmatizer()
ourNewModel.load('model.tflearn')

def ourText(text): 
  newtkns = nltk.word_tokenize(text)
  newtkns = [lm.lemmatize(word) for word in newtkns]
  return newtkns

def wordBag(text, vocab): 
  newtkns = ourText(text)
  bagOwords = [0] * len(vocab)
  for w in newtkns: 
    for idx, word in enumerate(vocab):
      if word == w: 
        bagOwords[idx] = 1
  return num.array(bagOwords)

def pred_class(text, vocab, labels): 
  bagOwords = wordBag(text, vocab)
  ourResult = ourNewModel.predict(num.array([bagOwords]))[0]
  newThresh = 0.2
  yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

  yp.sort(key=lambda x: x[1], reverse=True)
  newList = []
  for r in yp:
    newList.append(labels[r[0]])
  return newList

def getRes(firstlist, fJson): 
  tag = firstlist[0]
  listOfIntents = fJson["intents"]
  for i in listOfIntents: 
    if i["tag"] == tag:
      ourResult = random.choice(i["responses"])
      break
  return ourResult
while True:
    newMessage = input("")
    intents = pred_class(newMessage, newWords, ourClasses)
    ourResult = getRes(intents, ourData)
    print(ourResult)
