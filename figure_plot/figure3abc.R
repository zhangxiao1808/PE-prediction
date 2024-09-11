library(ggplot2)
library(ggpubr)
library(Rmisc)
library(dplyr)


f1<-read.csv("PLGF/all_PLGF_raw_selected.csv",header=T,check.names = F)
f1$gestation<-floor(f1$gestation)
#f1=f1[f1$hospital=="BaoAn" | f1$hospital=="Changsha" | f1$hospital=="GFY"| f1$hospital=="HFZ"| f1$hospital=="JiangMen"| f1$hospital=="LG"| f1$hospital=="ZhuHai",]
names(f1)<-c("ID","group","gestation","Raw")
f2<-read.csv("PLGF/all_PLGF_gestation_mom.csv",header=T,check.names = F)
names(f2)<-c("ID","group","gestation","MoM")
f2$gestation<-floor(f2$gestation)
f<-merge(f1,f2,all.x = T)
f<-na.omit(f)

pdf("PLGF_ELISA_boxplot_12-17+6.pdf",width=3,height=3)
for (i in c(4:dim(f)[2])){
  data <- f[,c(2,i)]
  protein_name=colnames(data)[2]
  data[,2]<-as.numeric(data[,2])
  data <-na.omit(data)
  #t<-data.frame(test=protein_name,table(data$group))
  names(data)<-c("group","value")  
  
  p<-ggplot(data, aes(y=value,x=group,fill=group))+
    geom_boxplot() +
    theme_set(theme_bw())+
    stat_compare_means(vjust=0.5,comparisons = list(c("control","EPE"),c("control","LPE")),method = "wilcox",label = "p.signif",facet.by = "dose", 
                       aes(group=group))+
    theme(axis.text.x=element_text(colour = "black",angle=45,size=12,hjust = 1,vjust = 1),
          axis.text.y=element_text(colour = "black",size=12),
          axis.title=element_text(size=12),
          plot.title = element_text(hjust = 0.5,size = 15),
          plot.margin = margin(15,9,9,30))+
    scale_fill_manual(values=c("blue4","red4","red"))+
    guides(fill = guide_legend(title = ''))+
    ggtitle(protein_name)+
    labs(x="",y ="")+
    #facet_wrap(.~hospital,nrow=1)+
    scale_y_log10()
  #coord_cartesian(ylim = c(0,15))+
  print(p)
}
dev.off()
