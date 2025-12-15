sarapita <- read.csv("error_sarapita.csv", header = TRUE)
sarapita$time <- as.POSIXct(sarapita$time, format="%Y-%m-%d %H:%M:%S")

dosrius <- read.csv("error_dosrius.csv", header = TRUE)
dosrius$time <- as.POSIXct(dosrius$time, format="%Y-%m-%d %H:%M:%S")


par(mfrow = c(2, 1), mar = c(4, 4, 3, 1))

# ############################################################
# GRÀFIC 1: Temperatura a SA RÀPITA (PUNTS)
# ############################################################

ylim_sarapita <- range(sarapita$temp, na.rm = TRUE)

plot(x = sarapita$time, 
     y = sarapita$temp, 
     type = "p",          # 'p' = Punts
     pch = 19,            # Forma del punt (Cercle sòlid)
     col = "darkorange",  
     cex = 1,             # Mida del punt (1 = normal)
     ylim = c(0, 30),
     main = "Temperatura Sa Ràpita",
     xlab = "",           
     ylab = "Temperatura (ºC)")

# Afegim línia de mitjana
abline(h = mean(sarapita$temp, na.rm=TRUE), col="gray", lty=2)
grid()

# ############################################################
# GRÀFIC 2: Temperatura a DOSRIUS (PUNTS)
# ############################################################

ylim_dosrius <- range(dosrius$temp, na.rm = TRUE)

plot(x = dosrius$time, 
     y = dosrius$temp, 
     type = "p",          # 'p' = Punts
     pch = 19,            # Forma del punt (Cercle sòlid)
     col = "firebrick",   
     cex = 1,
     ylim = c(0, 30),
     main = "Temperatura Dosrius",
     xlab = "Data i Hora",
     ylab = "Temperatura (ºC)")

# Afegim línia de mitjana
abline(h = mean(dosrius$temp, na.rm=TRUE), col="gray", lty=2)
grid()
