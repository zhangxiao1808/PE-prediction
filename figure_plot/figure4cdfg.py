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
features_1=['BMI','Parity','RPL','IVF','PMH','Age','MAP']
features_2=["IGFBP1.PLGF",'Parity','RPL','IVF','PMH','Age','MAP','BMI']
features_3=["HDL-C",'Parity','RPL','IVF','PMH','Age','MAP','BMI',"IGFBP1.PLGF"]
features_4=["GGT",'Parity','RPL','IVF','PMH','Age','MAP','BMI',"IGFBP1.PLGF"]
features_5=["AS/AL","UA","HDL-C",'Parity','RPL','IVF','PMH','Age','MAP','BMI',"IGFBP1.PLGF"]


# data input

#train
f1_PE=pd.read_csv("matrix/train_imputed_EPE.matrix",index_col = 0,sep='\t')
f1_con=pd.read_csv("matrix/train_imputed_control.matrix",index_col = 0,sep='\t')
f1=pd.concat([f1_PE,f1_con],axis=1)
f11=f1.T
y_train=np.append(np.ones([len(f1_PE.columns.values)]),np.zeros([len(f1_con.columns.values)]))

x_train_1=pd.DataFrame(f11[features_1]).values
x_train_2=pd.DataFrame(f11[features_2]).values
x_train_3=pd.DataFrame(f11[features_3]).values
x_train_4=pd.DataFrame(f11[features_4]).values
x_train_5=pd.DataFrame(f11[features_5]).values


# validation
f2_PE=pd.read_csv("matrix/validation_imputed_EPE.matrix",index_col = 0,sep='\t')
f2_con=pd.read_csv("matrix/validation_imputed_control.matrix",index_col = 0,sep='\t')
f2=pd.concat([f2_PE,f2_con],axis=1)
f22=f2.T
y_vali=np.append(np.ones([len(f2_PE.columns.values)]),np.zeros([len(f2_con.columns.values)]))

#vali
x_vali_1=pd.DataFrame(f22[features_1]).values
x_vali_2=pd.DataFrame(f22[features_2]).values
x_vali_3=pd.DataFrame(f22[features_3]).values
x_vali_4=pd.DataFrame(f22[features_4]).values
x_vali_5=pd.DataFrame(f22[features_5]).values


#bigtest
f3_PE=pd.read_csv("matrix/bigtest_imputed_EPE.matrix",index_col = 0,sep='\t')
f3_con=pd.read_csv("matrix/bigtest_imputed_control.matrix",index_col = 0,sep='\t')
f3=pd.concat([f3_PE,f3_con],axis=1)
f33=f3.T
y_bigtest=np.append(np.ones([len(f3_PE.columns.values)]),np.zeros([len(f3_con.columns.values)]))

# model predict
x_bigtest_1=pd.DataFrame(f33[features_1]).values
x_bigtest_2=pd.DataFrame(f33[features_2]).values
x_bigtest_3=pd.DataFrame(f33[features_3]).values
x_bigtest_4=pd.DataFrame(f33[features_4]).values
x_bigtest_5=pd.DataFrame(f33[features_5]).values


#load trained model
model_1=joblib.load("model/fixed/EPE_MF.pkl")
model_2=joblib.load("model/fixed/EPE_IGFBP1.PLGF.pkl")
model_3=joblib.load("model/fixed/EPE_protein+HDL-C.pkl")
model_4=joblib.load("model/fixed/EPE_protein+GGT.pkl")
model_5=joblib.load("model/fixed/EPE_protein+AS_AL+UA+HDL-C.pkl")


#validation
y_vali_new_1 = model_1.predict_proba(x_vali_1)
y_vali_new_2 = model_2.predict_proba(x_vali_2)
y_vali_new_3 = model_3.predict_proba(x_vali_3)
y_vali_new_4 = model_4.predict_proba(x_vali_4)
y_vali_new_5 = model_5.predict_proba(x_vali_5)

#calculate AUC
fpr_vali_1,tpr_vali_1,thr_vali_1=roc_curve(y_vali,y_vali_new_1[:,1],drop_intermediate=False)
roc_auc_vali_1=auc(fpr_vali_1,tpr_vali_1)
fpr_vali_2,tpr_vali_2,thr_vali_2=roc_curve(y_vali,y_vali_new_2[:,1],drop_intermediate=False)
roc_auc_vali_2=auc(fpr_vali_2,tpr_vali_2)
fpr_vali_3,tpr_vali_3,thr_vali_3=roc_curve(y_vali,y_vali_new_3[:,1],drop_intermediate=False)
roc_auc_vali_3=auc(fpr_vali_3,tpr_vali_3)
fpr_vali_4,tpr_vali_4,thr_vali_4=roc_curve(y_vali,y_vali_new_4[:,1],drop_intermediate=False)
roc_auc_vali_4=auc(fpr_vali_4,tpr_vali_4)
fpr_vali_5,tpr_vali_5,thr_vali_5=roc_curve(y_vali,y_vali_new_5[:,1],drop_intermediate=False)
roc_auc_vali_5=auc(fpr_vali_5,tpr_vali_5)

print(roc_auc_vali_1,roc_auc_vali_2,roc_auc_vali_3,roc_auc_vali_4,roc_auc_vali_5,sep="\t")

#compare auc by delong's test
sys.path.append("/Users/zhangxiao/Desktop/华大基因资料/孕期疾病预测项目/文章/蛋白/ELISA/")
import compare_auc_delong_xu 

#log10(p-value) by delong's test
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_vali,y_vali_new_1[:,1],y_vali_new_2[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_vali,y_vali_new_1[:,1],y_vali_new_3[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_vali,y_vali_new_1[:,1],y_vali_new_4[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_vali,y_vali_new_1[:,1],y_vali_new_5[:,1])
print(10**log10_pvalue.item())


#plot ROC
plt.figure(figsize=(7, 6))
plt.rcParams['svg.fonttype'] = 'none'
plt.plot(fpr_vali_1,tpr_vali_1,label='MF (AUC= {0:.4f})'.format(roc_auc_vali_1),lw=2,c="#3574B6")
plt.plot(fpr_vali_2,tpr_vali_2,label='MF+protein (AUC= {0:.4f})'.format(roc_auc_vali_2),lw=2,c="#1A814F")
plt.plot(fpr_vali_3,tpr_vali_3,label='MF+protein+HDL-C (AUC= {0:.4f})'.format(roc_auc_vali_3),lw=2,c="#8B81A2")
plt.plot(fpr_vali_4,tpr_vali_4,label='MF+protein+GGT (AUC= {0:.4f})'.format(roc_auc_vali_4),lw=2,c="#CB8778")
plt.plot(fpr_vali_5,tpr_vali_5,label='MF+protein+AS/AL+UA+HDL-C (AUC= {0:.4f})'.format(roc_auc_vali_5),lw=2,c="#7c2102")


plt.plot([0,1],[0,1],color='black',lw=2,linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
#plt.show()
plt.savefig('EPE_vali_compare_ROC.svg', bbox_inches='tight',dpi=600)


#bigtest
y_bigtest_new_1 = model_1.predict_proba(x_bigtest_1)
y_bigtest_new_2 = model_2.predict_proba(x_bigtest_2)
y_bigtest_new_3 = model_3.predict_proba(x_bigtest_3)
y_bigtest_new_4 = model_4.predict_proba(x_bigtest_4)
y_bigtest_new_5 = model_5.predict_proba(x_bigtest_5)

#calculate AUC
fpr_bigtest_1,tpr_bigtest_1,thr_bigtest_1=roc_curve(y_bigtest,y_bigtest_new_1[:,1],drop_intermediate=False)
roc_auc_bigtest_1=auc(fpr_bigtest_1,tpr_bigtest_1)
fpr_bigtest_2,tpr_bigtest_2,thr_bigtest_2=roc_curve(y_bigtest,y_bigtest_new_2[:,1],drop_intermediate=False)
roc_auc_bigtest_2=auc(fpr_bigtest_2,tpr_bigtest_2)
fpr_bigtest_3,tpr_bigtest_3,thr_bigtest_3=roc_curve(y_bigtest,y_bigtest_new_3[:,1],drop_intermediate=False)
roc_auc_bigtest_3=auc(fpr_bigtest_3,tpr_bigtest_3)
fpr_bigtest_4,tpr_bigtest_4,thr_bigtest_4=roc_curve(y_bigtest,y_bigtest_new_4[:,1],drop_intermediate=False)
roc_auc_bigtest_4=auc(fpr_bigtest_4,tpr_bigtest_4)
fpr_bigtest_5,tpr_bigtest_5,thr_bigtest_5=roc_curve(y_bigtest,y_bigtest_new_5[:,1],drop_intermediate=False)
roc_auc_bigtest_5=auc(fpr_bigtest_5,tpr_bigtest_5)

print(roc_auc_bigtest_1,roc_auc_bigtest_2,roc_auc_bigtest_3,roc_auc_bigtest_4,roc_auc_bigtest_5,sep="\t")

#log10(p-value) by delong's test
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_bigtest,y_bigtest_new_1[:,1],y_bigtest_new_2[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_bigtest,y_bigtest_new_1[:,1],y_bigtest_new_3[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_bigtest,y_bigtest_new_1[:,1],y_bigtest_new_4[:,1])
print(10**log10_pvalue.item())
log10_pvalue=compare_auc_delong_xu.delong_roc_test(y_bigtest,y_bigtest_new_1[:,1],y_bigtest_new_5[:,1])
print(10**log10_pvalue.item())


#plot ROC
plt.figure(figsize=(7, 6))
plt.rcParams['svg.fonttype'] = 'none'
plt.plot(fpr_bigtest_1,tpr_bigtest_1,label='MF (AUC= {0:.4f})'.format(roc_auc_bigtest_1),lw=2,c="#3574B6")
plt.plot(fpr_bigtest_2,tpr_bigtest_2,label='MF+protein (AUC= {0:.4f})'.format(roc_auc_bigtest_2),lw=2,c="#1A814F")
plt.plot(fpr_bigtest_3,tpr_bigtest_3,label='MF+protein+HDL-C(AUC= {0:.4f})'.format(roc_auc_bigtest_3),lw=2,c="#8B81A2")
plt.plot(fpr_bigtest_4,tpr_bigtest_4,label='MF+protein+GGT (AUC= {0:.4f})'.format(roc_auc_bigtest_4),lw=2,c="#CB8778")
plt.plot(fpr_bigtest_5,tpr_bigtest_5,label='MF+protein+AS/AL+UA+HDL-C (AUC= {0:.4f})'.format(roc_auc_bigtest_5),lw=2,c="#7c2102")


plt.plot([0,1],[0,1],color='black',lw=2,linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
#plt.show()
plt.savefig('EPE_bigtest_compare_ROC.svg', bbox_inches='tight',dpi=600)


#plot feature importance
f11[features_4].columns =["HDL-C",'Parity','RPL','IVF','PMH','Age','MAP','BMI',"IGFBP1.PLGF"]
importances = model_4.feature_importances_
sorted_indices = np.argsort(importances)[::-1]

plt.figure(figsize=(4, 2.5))
plt.rcParams['svg.fonttype'] = 'none'
plt.title('Feature Importance')
plt.bar(range(x_train_4.shape[1]), importances[sorted_indices], align='center')
plt.xticks(range(x_train_4.shape[1]), f11[features_4].columns[sorted_indices], rotation=90)
plt.tight_layout()
#plt.show()
#print(importances)
plt.savefig('EPE_feature_importance_GGT.svg', bbox_inches='tight',dpi=600)


#plot shap beewarms
import shap 

explainer = shap.Explainer(model_4)
sv = explainer(x_train_4)
sv.feature_names=["GGT",'Parity','RPL','IVF','PMH','Age','MAP','BMI',"IGFBP1.PLGF"]

plt.figure(figsize=(3, 4))
plt.rcParams['svg.fonttype'] = 'none'
shap.plots.beeswarm(sv[:,:,1],show=False,plot_size=[4,6])
plt.savefig('EPE_shap_GGT.svg', bbox_inches='tight',dpi=600)


