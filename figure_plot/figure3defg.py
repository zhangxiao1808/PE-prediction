#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import auc,roc_curve
import sys
import pandas as pd
import joblib
import matplotlib.pyplot as plt

#feature
metabolite=['IGFBP1.PLGF']
clinic=['Parity','RPL','IVF','PMH','Age','MAP','BMI']

# data input
f1_PE=pd.read_csv("matrix/train_EPE.matrix",index_col = 0,sep='\t')
f1_con=pd.read_csv("matrix/train_control.matrix",index_col = 0,sep='\t')
f1=pd.concat([f1_PE,f1_con],axis=1)
f11=f1.T
df1=pd.concat([f11[metabolite],f11[clinic]],axis=1)
x_train=pd.DataFrame(df1).values
y_train=np.append(np.ones([len(f1_PE.columns.values)]),np.zeros([len(f1_con.columns.values)]))

f2_PE=pd.read_csv("matrix/validation_EPE.matrix",index_col = 0,sep='\t')
f2_con=pd.read_csv("matrix/validation_control.matrix",index_col = 0,sep='\t')
f2=pd.concat([f2_PE,f2_con],axis=1)
f22=f2.T
df2=pd.concat([f22[metabolite],f22[clinic]],axis=1)
x_test=pd.DataFrame(df2).values
y_test=np.append(np.ones([len(f2_PE.columns.values)]),np.zeros([len(f2_con.columns.values)]))

f3_PE=pd.read_csv("matrix/bigtest_EPE.matrix",index_col = 0,sep='\t')
f3_con=pd.read_csv("matrix/bigtest_control.matrix",index_col = 0,sep='\t')
f3=pd.concat([f3_PE,f3_con],axis=1)
f33=f3.T
df3=pd.concat([f33[metabolite],f33[clinic]],axis=1)
x_vali=pd.DataFrame(df3).values
y_vali=np.append(np.ones([len(f3_PE.columns.values)]),np.zeros([len(f3_con.columns.values)]))

# load model
model=joblib.load("model/fixed/EPE_IGFBP1.PLGF.pkl")


#calculate AUC

y_train_new = model.predict_proba(x_train)
y_test_new = model.predict_proba(x_test)
y_vali_new = model.predict_proba(x_vali)


fpr_train,tpr_train,_=roc_curve(y_train,y_train_new[:,1])
roc_auc_train=auc(fpr_train,tpr_train)
        
fpr_test,tpr_test,_=roc_curve(y_test,y_test_new[:,1])
roc_auc_test=auc(fpr_test,tpr_test)
        
fpr_vali,tpr_vali,_=roc_curve(y_vali,y_vali_new[:,1])
roc_auc_vali=auc(fpr_vali,tpr_vali)


#plot ROC
plt.figure(figsize=(5, 4))
plt.plot(fpr_train,tpr_train,label='train (AUC= {0:.2f})'.format(roc_auc_train),lw=2,c="blue",linestyle='-')
plt.plot(fpr_test,tpr_test,label='validation (AUC= {0:.2f})'.format(roc_auc_test),lw=2,c="green",linestyle='-')
plt.plot(fpr_vali,tpr_vali,label='bigtest (AUC= {0:.2f})'.format(roc_auc_vali),lw=2,c="purple",linestyle='-')
plt.plot([0,1],[0,1],color='black',lw=2,linestyle='-')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.rcParams['svg.fonttype'] = 'none'
#plt.show()
plt.savefig('EPE_best_ROC.svg', bbox_inches='tight',dpi=600)


#plot feature importance
df1.columns =['IGFBP1.PLGF','Parity','RPL','IVF','PMH','Age','MAP','BMI']
importances = model.feature_importances_
sorted_indices = np.argsort(importances)[::1]

plt.figure(figsize=(2.5, 4))
plt.title('Feature Importance')
plt.barh(range(x_train.shape[1]), importances[sorted_indices], align='center')
plt.yticks(range(x_train.shape[1]),df1.columns[sorted_indices])
plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none'
#plt.show()
#print(importances)
plt.savefig('EPE_feature_importance.svg', bbox_inches='tight',dpi=600)
