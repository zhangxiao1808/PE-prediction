library("ggplot2")
library("ggrepel")

data<-read.csv("LPE_BA_DE.csv",header = T)
data<-subset(data,logfoldchange!="NA") 
data<-subset(data,Pvalue!="NA")

Regulation <- as.factor(ifelse(data$Pvalue < 0.05 & abs(data$logfoldchange) >0 , ifelse(data$logfoldchange > 0 ,'Up','Down'),'Not'))

ggplot(data,aes(x=logfoldchange,y=-log10(Pvalue),colour=Regulation)) +
  xlab("log(Fold Change)")+ylab("-log10(p-value)") +
  geom_point(size = 2,alpha=1) +
  xlim(-4.5,4.5) +
  ggtitle("LPE BA")+
  scale_color_manual(values=c("blue","grey", "red"))+
  #geom_vline(xintercept = c(0), lty = 2,colour="#000000")+ 
  geom_hline(yintercept = -log10(0.05), lty = 2,colour="#000000")+
  geom_hline(yintercept = -log10(0.05), lty = 2,colour="#000000")+
  theme(axis.text=element_text(size=15),
        axis.title=element_text(size=15),
        plot.title = element_text(hjust = 0.5,size = 15),)+
  geom_text_repel(
    data = data[data$Pvalue < 0.05,],
    aes(label = features),
    size = 4.5,
    color = "black",
    segment.color = "black", show.legend = FALSE)
