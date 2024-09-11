library(Rmisc)
library(dplyr)
library(corrplot)

f<-read.csv("12-17+6w/all_clinic_data_12-17+6w.csv",header=T,row.names = 1,check.names = F)
f=f[f$hospital!="LG",]
f=f[f$group=="control",]
f=select(f,as.vector(c("WBC","PLT","NE#","MO#","ALT","AS/AL","GGT","HDL-C","UA")))

cor.mat<-cor(f,use = "pairwise.complete.obs")

#correlation plot
pdf("12-17+6w/9_features_correlation_plot.pdf",width=6,height=8)
corrplot(cor.mat,is.corr = T,cl.pos = "n",addgrid.col = "black", tl.col = "black",)
corrplot(cor.mat,is.corr = T,method = "number",type = "lower",add = T,diag = F,tl.pos = "n",cl.pos = "b",addgrid.col = "black",tl.col = "black",)
dev.off()  


