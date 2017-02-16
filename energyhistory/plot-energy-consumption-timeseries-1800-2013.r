# Use GNU R and ggplot2 to plot the crude oil price per litre in inflation-corrected 2015 US dollars

library(ggplot2)
library(reshape2)

kwhpppd <- read.delim("timeseries-energy-use-per-capita.dat", header = TRUE, as.is=TRUE)
twhpd <- read.delim("timeseries-energy-use-TWh-per-day.dat", header = TRUE, as.is=TRUE)

vars <- c("year", "oil", "coal", "gas", "nuclear", "renewables")

dfepc <- melt(kwhpppd[vars], id.vars = "year")

pal <- c("#000000", "#E69F00", "#56B4E9", "#F0E442", "#009E73", "#0072B2", "#D55E00", "#CC79A7")
ggplot(dfepc, aes(x=year, y=value, fill=variable)) + geom_area() + ylab("energy consumption (kWh per person per day)") + scale_fill_manual(values=pal)

vars <- c("year", "renewables", "coal", "oil", "gas", "nuclear")
pal <- c("#009E73", "#E69F00", "#000000", "#56B4E9", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

dfepy <- melt(twhpd[vars], id.vars = "year")

ggplot(dfepy, aes(x=year, y=value, fill=variable)) + geom_area() + ylab("energy consumption (TWh per day)") + scale_fill_manual(values=pal)

