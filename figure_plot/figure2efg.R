library(ggplot2)
library(ggpubr)
library(Rmisc)
library(dplyr)
library(reshape2)


f<-read.csv("target_proteins_PCA_filtered.csv",header=T,check.names = F)
f<-f[f$gestation<18,]

EPE_features<-c("GLRX1","HBB_EFTPPVQAAYQK","IGFBP1","PRG2","MIF")
f=select(f,as.vector(c("ID","group","hospital",EPE_features)))
names(f)<-c("ID","group","hospital","GLRX","HBB","IGFBP1","PRG2","MIF")
f=f[f$group!="LPE",]

LPE_features<-c("MIF")
f=select(f,as.vector(c("ID","group","hospital",LPE_features)))
f=f[f$group!="EPE",]

ff<-melt(f,id.vars = c("ID","group","hospital"),variable.name = "feature",value.name = "value")

pdf("target_LPE_boxplot_by_hospital.pdf",width=4,height=3)
for (i in c("ZH","JM","BA")){
  data <- ff[which(ff$hospital==i),]
  p<-ggplot(data, aes(y=log(value,10),x=feature,fill=group))+
    geom_boxplot() +
    theme_set(theme_bw())+
    stat_compare_means(vjust=1,method = "wilcox",label = "p.signif",facet.by = "dose", aes(group=group))+
    theme(axis.text.x=element_text(colour = "black",angle=90,size=14,hjust = 1,vjust = 1),
          axis.text.y=element_text(colour = "black",size=10),
          axis.title=element_text(size=14),
          plot.title = element_text(hjust = 0.5,size = 14),
          plot.margin = margin(15,9,9,30),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank())+
    scale_fill_manual(values=c("blue4","red4"))+
    guides(fill = guide_legend(title = ''))+
    ylim(0,10)+
    ggtitle(i)+
    labs(x="",y = "log10(Concentration (pg/ml))")
  print(p)
}
dev.off()

