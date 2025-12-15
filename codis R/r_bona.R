
par(mfrow = c(2, 1), mar = c(4, 4, 3, 1))

# ============================================================
# GRÀFIC 1: SA RÀPITA
# ============================================================

sarapita <- read.csv("error_sarapita.csv", header = TRUE)
sarapita$time <- as.POSIXct(sarapita$time, format="%Y-%m-%d %H:%M:%S")


lim_y_sarapita <- range(c(sarapita$dgfs, sarapita$dicon7, sarapita$darome), na.rm = TRUE)


plot(x = sarapita$time, y = sarapita$dgfs, 
     type = "p", pch = 19, col = "blue", 
     ylim = lim_y_sarapita, cex = 1.2,
     main = "Sa Ràpita: Error dels Models",
     xlab = "", ylab = "Error")

points(x = sarapita$time, y = sarapita$dicon7, col = "red", pch = 17, cex = 1.2)
points(x = sarapita$time, y = sarapita$darome, col = "darkgreen", pch = 15, cex = 1.2)

grid()
legend("topright", legend = c("GFS", "ICON7", "AROME"),
       col = c("blue", "red", "darkgreen"), pch = c(19, 17, 15), pt.cex = 1, cex=0.8)

# ============================================================
# GRÀFIC 2: DOSRIUS
# ============================================================
# 1. Llegir i preparar dades

dosrius <- read.csv("error_dosrius.csv", header = TRUE)
dosrius$time <- as.POSIXct(dosrius$time, format="%Y-%m-%d %H:%M:%S")

# 2. Calcular límits
lim_y_dosrius <- range(c(dosrius$dgfs, dosrius$dicon7, dosrius$darome), na.rm = TRUE)

# 3. Dibuixar
plot(x = dosrius$time, y = dosrius$dgfs, 
     type = "p", pch = 19, col = "blue", 
     ylim = lim_y_dosrius, cex = 1.2,
     main = "Dosrius: Error dels Models",
     xlab = "Data i Hora", ylab = "Error")

points(x = dosrius$time, y = dosrius$dicon7, col = "red", pch = 17, cex = 1.2)
points(x = dosrius$time, y = dosrius$darome, col = "darkgreen", pch = 15, cex = 1.2)

grid()

legend("topright", legend = c("GFS", "ICON7", "AROME"),
       col = c("blue", "red", "darkgreen"), pch = c(19, 17, 15), pt.cex = 1, cex=0.8)


par(mfrow = c(1, 1))