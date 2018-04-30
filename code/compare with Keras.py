# -*- coding: utf-8 -*-  
from keras.models import Sequential
from keras.layers import Dense
import random, re, json, os
import numpy
old = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = old[:,0:9]
Y = old[:,9]
for a in old:
    p = a[1]
    mati = str(p)
    o = ot = list(mati)
    k = int((len(o)+1)/2)
    jj=[]
    for j in range(0,len(o)):
        jj.append(j)
    d = random.sample(jj,k)
    for i in d:
        o[i] = "0"
    r = ""
    for w in o:
        r = r + w
    a[1] = float(r)
X1 = old[:,0:9]
Y1 = old[:,9]
# create model
model = Sequential()
model.add(Dense(12, input_dim=9, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X1, Y1, epochs=130, batch_size=10,  verbose=2)
# calculate predictions
predictions = model.predict(X1)
# ro6und predictions
rounded = [round(x[0]) for x in predictions]



dataset1 = numpy.loadtxt("pima-indians-diabetes2.csv", delimiter=",")
# split into input (X) and output (Y) variables
j = dataset1[:,0:8]
i = dataset1[:,8]
# create model
model1 = Sequential()
model1.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model1.add(Dense(8, init='uniform', activation='relu'))
model1.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model1.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model1.fit(j, i, epochs=130, batch_size=10,  verbose=2)
# calculate predictions
predictions1 = model1.predict(j)
# round predictions
rounded1 = [round(x[0]) for x in predictions1]
print(rounded)
print(rounded1)

same = 0
differ = 0
for n in range(766):
    if rounded[n] == rounded1[n]:
        same = same+1
    elif rounded[n] != rounded1[n]:
        differ = differ+1
print(same)
print(differ)


from matplotlib import pyplot as plt 

plt.figure(figsize=(6,9))
labels = [u'same',u'differ']
sizes = [same,differ]
colors = ['yellowgreen','lightskyblue']
explode = (0.05,0.0)
patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
                                labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                startangle = 90,pctdistance = 0.6)

for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)

plt.axis('equal')
plt.legend()
plt.show()
