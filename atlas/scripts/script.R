# scripts/script.R
library(ggpplot2)
data <- data.frame(x = c(1, 2, 3, 4), y = c(5, 6, 7, 8))
ppng("plot.png")
ggplot(data, aes(x=x, y=y)) + geom_line()
dev.off()