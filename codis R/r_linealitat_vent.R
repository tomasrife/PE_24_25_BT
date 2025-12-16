
setwd("C:/Users/tomas/OneDrive/Escritorio/projectepe/data")

dades_errors_dr <- read.csv("error_dosrius.csv", header = TRUE)
dades_errors_sr <- read.csv("error_sarapita.csv", header = TRUE)



par(mfrow = c(1, 2)) 


ymax_dr <- max(c(dades_errors_dr$dgfs, dades_errors_dr$darome, dades_errors_dr$dicon7), na.rm=TRUE)
ymin_dr <- min(c(dades_errors_dr$dgfs, dades_errors_dr$darome, dades_errors_dr$dicon7), na.rm=TRUE)

plot(dades_errors_dr$dir, dades_errors_dr$dgfs, 
     col = "blue", pch = 16, 
     ylim = c(ymin_dr, ymax_dr), 
     xlab = "Direcció", ylab = "Error",
     main = "Dosrius")

points(dades_errors_dr$dir, dades_errors_dr$darome, col = "green", pch = 16)
points(dades_errors_dr$dir, dades_errors_dr$dicon7, col = "red", pch = 16)


legend("topright", legend=c("GFS", "AROME", "ICON7"),
       col=c("blue", "green", "red"), pch=16, cex=0.7)



ymax_sr <- max(c(dades_errors_sr$dgfs, dades_errors_sr$darome, dades_errors_sr$dicon7), na.rm=TRUE)
ymin_sr <- min(c(dades_errors_sr$dgfs, dades_errors_sr$darome, dades_errors_sr$dicon7), na.rm=TRUE)

plot(dades_errors_sr$dir, dades_errors_sr$dgfs, 
     col = "blue", pch = 16,
     ylim = c(ymin_sr, ymax_sr),
     xlab = "Direcció", ylab = "Error",
     main = "Sa Ràpita")

points(dades_errors_sr$dir, dades_errors_sr$darome, col = "green", pch = 16)
points(dades_errors_sr$dir, dades_errors_sr$dicon7, col = "red", pch = 16)

legend("topright", legend=c("GFS", "AROME", "ICON7"),
       col=c("blue", "green", "red"), pch=16, cex=0.7)