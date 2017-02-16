# Use GNU R and ggplot2 to plot the crude oil price per litre in inflation-corrected 2015 US dollars
library(ggplot2)
oilprice <- read.delim("crude-oil-price-inflation-corrected.csv", header = TRUE, as.is=TRUE)
ggplot(oilprice, aes(x=year, y=dollars_per_L_2015)) + geom_line() + ylab("crude oil price per Litre (2015 US dollars)") + scale_x_continuous(breaks = scales::pretty_breaks(n = 8)) + scale_y_continuous(breaks = scales::pretty_breaks(n = 8))


