library(pheatmap)

f<-read.csv("12-17+6w/all_clinic_DE_foldchange.csv",row.names = 2,header = TRUE)
f<-f[c("WBC","PLT","NE#","MO#","ALT","AS/AL","UA","HDL-C","GGT"),]
data<-log(f[,-1])

df<-read.csv("12-17+6w/all_clinic_DE_pvalue.csv",row.names = 2,header = TRUE)
df<-df[,-1]
df<-df[c("WBC","PLT","NE#","MO#","ALT","AS/AL","UA","HDL-C","GGT"),]

sample_annotation <- data.frame(Hospital = c("ZH","ZH","JM","JM","BA","BA"))
rownames(sample_annotation) <- colnames(data)

feature_annotation <- data.frame(TestType = f$type)
rownames(feature_annotation) <- rownames(data)


#breaks
bk <- c(seq(-0.5,-0.1,by=0.01),seq(0,0.5,by=0.01))

p<-pheatmap(data,
         annotation_row = feature_annotation,
         annotation_col = sample_annotation,
         cluster_rows = F,
         cluster_cols = F,
         na_col = "#ffffff",
         fontsize_row = 5.5,
         #border_color = NA, 
         display_numbers = matrix(ifelse(df<0.05,"*",""),nrow(df)),
         color = c(colorRampPalette(colors = c("RoyalBlue","white"))(length(bk)/2),colorRampPalette(colors = c("white","Brown2"))(length(bk)/2)),
         legend_breaks=seq(-0.5,0.5,0.5),
         breaks = bk,
         gaps_col = c(2,4,6))
print(p)

save_pheatmap_pdf <- function(x, filename, width=6, height=4) {
  stopifnot(!missing(x))
  stopifnot(!missing(filename))
  pdf(filename, width=width, height=height)
  grid::grid.newpage()
  grid::grid.draw(x$gtable)
  dev.off()
}

save_pheatmap_pdf(p, "12-17+6w/all_selected_indicators_heatmap.pdf")
