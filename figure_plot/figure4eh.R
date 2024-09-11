SHAP_analysis <- function(data,diseasetype="EPE",features=""){
  #data$Group=ifelse(data$Group==diseasetype,1,0)
  library(caret)
  library(kernelshap)
  library(shapviz)
  library(ggplot2)
  library(ggbeeswarm)
  data=data[,colnames(data)%in%c("Group",features)]
  
  fit <- train(
    Group ~ . , 
    data = data, 
    method = "rf", 
    #tuneGrid = data.frame(intercept = TRUE),
    trControl = trainControl(method = "none")
  )
  xvars <- colnames(data[-1])
  s <- kernelshap(fit, data, predict, bg_X = data, feature_names = xvars)
  sv <- shapviz(s)
  tiff(paste("Mean_Shap_values_",diseasetype,".tiff"),width=12,height=8,units = "cm",res=300,compression = "lzw+p",pointsize=8)
  p=sv_importance(sv)+theme_bw()+theme(axis.text = element_text(color = "black"))+theme(axis.text=element_text(size=14,angle=0,hjust = 1,colour="black"),axis.title=element_text(size=14),legend.text = element_text(size = 14))+theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank(),panel.background = element_rect(fill = "white",color="black",linetype ="solid" ))
  print(p)
  dev.off()
  Rawdata=s$S
  
  shap_plot <- function(rawdata){
    d=c(rawdata)
    m=nrow(rawdata)
    n=i=k=numeric()
    for(i in colnames(rawdata)){k=c(k,rep(i,m))}
    for(i in 1:ncol(rawdata)){shap_importance = mean(abs(rawdata[,i]));n=c(n,rep(shap_importance,m))}
    DATA=data.frame(v1=d,v2=k,v3=n)
    colnames(DATA)=c("shap_value","feature","shap_importance")
    tiff(paste("Shap_values_",diseasetype,".tiff"),width=15,height=8,units = "cm",res=300,compression = "lzw+p",pointsize=8)
    p=ggplot(DATA,aes(x=shap_value,y = reorder(feature, shap_importance))) +geom_quasirandom(groupOnX = FALSE, varwidth = TRUE, size =1, alpha = 0.8, aes(color = shap_value)) +scale_color_gradient(low = "#ffcd30", high = "#6600cd")+labs(x="SHAP value",y="")+theme_bw()+theme(axis.text = element_text(color = "black"))+geom_vline(xintercept = 0,linetype="dashed",color="grey")+theme(axis.text=element_text(size=14,angle=0,hjust = 1,colour="black"),axis.title=element_text(size=14),legend.text = element_text(size = 14))+theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank(),panel.background = element_rect(fill = "white",color="black",linetype ="solid" ))
    print(p)
    dev.off()
    write.table(DATA,file=paste("Shap_values_",diseasetype,".txt"),col.names=T,row.names=F,quote=F,sep="\t")
  }
  d=shap_plot(rawdata=Rawdata)
}