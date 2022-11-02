import string
import random 
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer 
import tensorflow as tensorF
from tensorflow import keras
from keras import Sequential 
from keras.layers import Dense, Dropout
lm = WordNetLemmatizer() 
import json#for getting wordshi
# lists
ourClasses = []
newWords = []
documentX = []
documentY = []
# Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
with open('E:/python codes/speech recognition projects/sppechrcognition/words.json') as f:
  ourData = json.load(f)
for intent in ourData["intents"]:
    for pattern in intent["patterns"]:
        ourTokens = nltk.word_tokenize(pattern)
        newWords.extend(ourTokens)
        documentX.append(pattern)
        documentY.append(intent["tag"])
    
    
    if intent["tag"] not in ourClasses:# add unexisting tags to their respective classes
        ourClasses.append(intent["tag"])

newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in string.punctuation] # set words to lowercase if not in punctuation
newWords = sorted(set(newWords))# sorting words
ourClasses = sorted(set(ourClasses))
trainingData = [] # training list array
outEmpty = [0] * len(ourClasses)
# BOW model
for idx, doc in enumerate(documentX):
    bagOfwords = []
    text = lm.lemmatize(doc.lower())
    for word in newWords:
        bagOfwords.append(1) if word in text else bagOfwords.append(0)
    
    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bagOfwords, outputRow])

random.shuffle(trainingData)
trainingData = num.array(trainingData, dtype=object)# coverting our data into an array afterv shuffling

x = num.array(list(trainingData[:, 0]))# first trainig phase
y = num.array(list(trainingData[:, 1]))# second training phase
iShape = (len(x[0]),)
oShape = len(y[0])

# the deep learning model
ourNewModel = Sequential()
ourNewModel.add(Dense(128, input_shape=iShape, activation="relu"))
ourNewModel.add(Dropout(0.5))
ourNewModel.add(Dense(64, activation="relu"))
ourNewModel.add(Dropout(0.3))
ourNewModel.add(Dense(oShape, activation = "softmax"))
md = tensorF.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
ourNewModel.compile(loss='categorical_crossentropy',
              optimizer=md,
              metrics=["accuracy"])
print(ourNewModel.summary())
ourNewModel.fit(x, y, epochs=500, verbose=1)
ourNewModel.save('model.tflearn')


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
