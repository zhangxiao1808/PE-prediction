library(ggplot2)

f<-read.csv("all_IGFBP1_PLGF_10-17+6W.csv",header=T,check.names = F)
#f<-f[f$experiment.x=="BGI",]
#f<-f[f$gestation>=70,]
#f<-f[f$gestation<114,]
#f<-na.omit(f)
#f<-f[!duplicated(f$ID),]
#f<-f[f$group=="control",]

pdf("IGFBP1_concentration_compare_10-17+6w.pdf",width=8,height=4)
p<-ggplot(f, aes(y=IGFBP1,color=group.x, x=gestation.x))+
  geom_smooth()+
  theme_classic()+
  theme(axis.text.x=element_text(colour = "black",size=15,hjust = 1,vjust = 1),
        axis.text.y=element_text(colour = "black",size=11),
        axis.title=element_text(size=15),
        plot.title = element_text(hjust = 0.5,size = 15),
        plot.margin = margin(15,9,9,30),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank())+
  ggtitle("IGFBP1")+
  labs(x="Gestational Age (days)",y = c("Concentration (pg/ml)"))+
  scale_color_manual(values = c("RoyalBlue", "Brown1", "Brown4"))

print(p)
dev.off()
