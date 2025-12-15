# ============================================================
# 1) PREPARACIÓ DE DADES
# ============================================================
sarapita <- read.csv("error_sarapita.csv", header = TRUE)
sarapita$time <- as.POSIXct(sarapita$time, format="%Y-%m-%d %H:%M:%S")

dosrius <- read.csv("error_dosrius.csv", header = TRUE)
dosrius$time <- as.POSIXct(dosrius$time, format="%Y-%m-%d %H:%M:%S")

# ############################################################
# 2) CONFIGURACIÓ DEL PANELL
# ############################################################
par(mfrow = c(2, 1), mar = c(4, 5, 3, 1)) # Marge esquerre (5) una mica més ample per les lletres

# ############################################################
# GRÀFIC 1: Direcció Vent SA RÀPITA
# ############################################################
plot(x = sarapita$time, 
     y = sarapita$dir, 
     type = "p",           # Punts
     pch = 19,             # Cercle sòlid
     col = "purple",       # Color lila
     cex = 1,
     ylim = c(0, 360),     # Els graus van de 0 a 360 obligatòriament
     yaxt = "n",           # "n" vol dir: "No dibuixis l'eix Y automàtic, que el faré jo"
     main = "Direcció del Vent: Sa Ràpita",
     xlab = "",           
     ylab = "Direcció")


axis(2, at = c(0, 90, 180, 270, 360), 
     labels = c("N", "E", "S", "W", "N"), las=1)


abline(h = c(90, 180, 270), col = "lightgray", lty = 3)
grid(nx = NULL, ny = NA) # Només graella vertical

# ############################################################
# GRÀFIC 2: Direcció Vent DOSRIUS
# ############################################################
plot(x = dosrius$time, 
     y = dosrius$dir, 
     type = "p", 
     pch = 19, 
     col = "darkcyan",     # Color blau-verdaci
     cex = 1,
     ylim = c(0, 360),
     yaxt = "n",           # Amaguem eix automàtic
     main = "Direcció del Vent: Dosrius",
     xlab = "Data i Hora",
     ylab = "Direcció")


axis(2, at = c(0, 90, 180, 270, 360), 
     labels = c("N", "E", "S", "W", "N"), las=1)


abline(h = c(90, 180, 270), col = "lightgray", lty = 3)
grid(nx = NULL, ny = NA)
