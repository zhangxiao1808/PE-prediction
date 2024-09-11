library(dplyr)

epe_features=c("AS/AL","UA","HDL-C","GGT")
lpe_features=c("WBC","PLT","MO#","AS/AL","HDL-C")
all_features=c("WBC","PLT","NE#","MO#","ALT","AS/AL","GGT","HDL-C","UA")

f<-read.csv("10-15+6w/train_AUC.csv",header=T,row.names = 1,check.names = F)
f<-f[all_features,]

f<-data.frame(features=row.names(f),f)

pdf("10-15+6w/LPE_features_AUC_barplot.pdf",width=2.5,height=6)
p<-ggplot(f,aes(x=factor(features,rev(all_features)),y=LPE_auc)) + 
  geom_bar(stat = "identity",position = position_dodge(0.9),width = 0.6,fill="#7489E1",color="black")+
  geom_text(aes(label=round(LPE_auc,5)),y=0.2)+
  theme_classic()+
  theme(axis.text.x=element_text(colour = "black",angle=30,size=10,hjust = 1,vjust = 1),
        axis.text.y=element_text(colour = "black",size=10),
        axis.title=element_text(size=15),
        plot.title = element_text(hjust = 0.5,size = 15),
        plot.margin = margin(15,9,9,30),
        legend.text = element_text(size = 15),
        legend.title = element_text(size = 15),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  xlab("")+
  ylab("")+
  ggtitle("LPE features AUC")+
  scale_y_continuous(expand = c(0,0))+
  coord_flip()

print(p)
dev.off()
