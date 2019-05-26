import tensorflow as tf
import numpy as np
from .models import Stainless, Tag, TensileStrength, YieldStrength, ThermodynamicProperty, Composition
import matplotlib.pyplot as plt


def make_compound_dict():
    stains=Stainless.objects.all()
    compound_dict={}
    for s in stains:
        compositions=s.composition_set.all()
        for c in compositions:
            # print(c.compound)
            if c.compound in compound_dict.keys():
                compound_dict[c.compound]+=1
            else:
                compound_dict[c.compound]=1
    # print(compound_dict.keys())

def train_ts():
    Y_TRAIN_TS=np.array([]) #Tensile strength
    # Y_TRAIN_YS=[] #Yield strength
    # Y_TRAIN_TC=[] #k
    X_TRAIN=np.array([]) #compounds' ratio
    
    stains=Stainless.objects.all()
    for i,s in enumerate(stains):
        comp=stainless_composition_to_array(s)
        tss=s.tensilestrength_set.all()
        for ts in tss:
            X_TRAIN=np.append(X_TRAIN,comp,axis=0)
            # print(np.shape(ts.strength),np.shape(Y_TRAIN_TS))
            Y_TRAIN_TS=np.append(Y_TRAIN_TS,[ts.strength],axis=0)
        
    
    X_TRAIN=X_TRAIN.reshape(-1,19)
    y=Y_TRAIN_TS
    # allAtoms = ['C', 'Cr', 'Fe', 'Mn', 'Ni', 'N', 'P', 'Si', 'S', 'Cu', 'Mo', 'Se', 'Nb', 'Ti', 'Zr', 'W', 'V', 'Ta', 'B']
    # for i in range(0,19): #TS
    #     x=X_TRAIN[:,i]
    #     # print(len(x),len(y))

    #     fig = plt.figure()
    #     plt.plot(x,y,'o')
    #     plt.title('%s - TS'%(allAtoms[i]))
    #     plt.xlabel('composition(%)')
    #     plt.ylabel('strength')
    #     # plt.axis([0,100,0,2100])
    #     # plt.title("Test plot")
    #     plt.close() # and this one

    #     fig.savefig('plots/%s-TS.png'%(allAtoms[i]))

    # x_data = [[73.,80.,75.],[93.,88.,93.],[89.,91.,90.],[96.,98.,100],[73.,66.,70]]
    x_data=X_TRAIN
    y_data = [[ys] for ys in y]

    #shape 형태를 주목하자.
    X = tf.placeholder(tf.float32,shape=[None,19])
    Y = tf.placeholder(tf.float32,shape=[None,1])

    W = tf.Variable(tf.random_normal([19,1]))
    b = tf.Variable(tf.random_normal([1]))

    # 행렬 곱을 실시한다.
    # [None,3]*[3,1] -> [None,1] 의 형태이다.
    hypothesis = tf.matmul(X,W)+b

    cost = tf.reduce_mean(tf.square(hypothesis-Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate = 1.4e-4)
    train = optimizer.minimize(cost)

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    for step in range(2000001):
        cost_val, hy_val, _ = sess.run([cost,hypothesis,train],
                                    feed_dict={X:x_data,Y:y_data})
        
        if step%1000==0:
            print(step,cost_val)
    print(sess.run([W,b]))
    # print(X_TRAIN)
    # print(sess.run([W,b]))

def stainless_composition_to_array(stainless):
    allAtoms = ['C', 'Cr', 'Fe', 'Mn', 'Ni', 'N', 'P', 'Si', 'S', 'Cu', 'Mo', 'Se', 'Nb', 'Ti', 'Zr', 'W', 'V', 'Ta', 'B']
    res=np.array([])
    compositions = stainless.composition_set.all()
    for i,atom in enumerate(allAtoms):
        try:
            res=np.append(res,compositions.get(compound=atom).ratio)
            # res.append(compositions.get(compound=atom).ratio)
        except Exception as e:
            res=np.append(res,0)
    return res