library(dplyr)
library(tidyverse)
library(ggsci)

f1<-read.table("Reactome_2022_table.txt",sep ="\t",header=T,quote = "\t",check.names = F)
f1<-f1[c(1:5),]
f1<-separate(f1,Overlap,into = c('num','back_num'),sep = '/')
f1<-data.frame(type="Reactome",f1,check.names = F)

f2<-read.table("KEGG_2021_Human_table.txt",sep ="\t",header=T,quote = "\t",check.names = F)
f2<-f2[c(1:5),]
f2<-separate(f2,Overlap,into = c('num','back_num'),sep = '/')
f2<-data.frame(type="KEGG",f2,check.names = F)

f3<-read.table("GO_Biological_Process_2023_table.txt",sep ="\t",quote = "\t",header=T,check.names = F)
f3<-f3[c(1:5),]
f3<-separate(f3,Overlap,into = c('num','back_num'),sep = '/')
f3<-data.frame(type="GO BP",f3,check.names = F)

f4<-read.table("GO_Cellular_Component_2023_table.txt",sep ="\t",quote = "\t",header=T,check.names = F)
f4<-f4[c(1:5),]
f4<-separate(f4,Overlap,into = c('num','back_num'),sep = '/')
f4<-data.frame(type="GO CC",f4,check.names = F)

f5<-read.table("GO_Molecular_Function_2023_table.txt",sep ="\t",quote = "\t",header=T,check.names = F)
f5<-f5[c(1:5),]
f5<-separate(f5,Overlap,into = c('num','back_num'),sep = '/')
f5<-data.frame(type="GO MF",f5,check.names = F)

f<-rbind(f1,f2,f3,f4,f5)
write.csv(f,file="LPE_3hospital_GO.csv",row.names=F)
f<-read.csv("LPE_3hospital_GO_clean.csv",header=T,check.names = F)
f$Term<-factor(f$Term,levels = unique(f$Term),ordered = T)

pdf("LPE_3hospital_GO_barplot.pdf",width=8,height=4)
ggplot(f,aes(x=Term,y=-log10(`Adjusted P-value`),fill=type)) + 
  geom_bar(stat = "identity",position = position_dodge(0.9),width = 0.6)+
  theme_classic()+
  theme(axis.text.x=element_text(colour = "black",angle=30,size=7,hjust = 1,vjust = 1),
        axis.text.y=element_text(colour = "black",size=7),
        axis.title=element_text(size=7),
        plot.title = element_text(hjust = 0.5,size = 15),
        plot.margin = margin(15,9,9,30),
        legend.text = element_text(size = 7),
        legend.title = element_text(size = 7),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  geom_hline(yintercept =-log10(0.05) ,linetype=2)+
  geom_text(aes(label=num),size=3,vjust=-0.5)+
  scale_fill_npg()+
  xlab("")+
  ylim(0,27)+
  ylab("-log10(Adjusted P-value)")+
  ggtitle("LPE ZH+JM+BA")
dev.off()

