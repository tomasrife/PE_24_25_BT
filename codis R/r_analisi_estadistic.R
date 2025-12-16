setwd("C:\\1 UNI LOCAL\\projectepe")

# ============================================================
# 1) Leer los dos CSV
# ============================================================
dosrius <- read.csv("error_dosrius.csv", header = TRUE)
sarapita <- read.csv("error_sarapita.csv", header = TRUE)

# ============================================================
# 2) Transformaciones log(error + 1) por modelo y por localidad
# ============================================================
# DOSRIUS
log_gfs_dosrius   <- log(dosrius$dgfs+1)
log_icon7_dosrius <- log(dosrius$dicon7+1)
log_arome_dosrius <- log(dosrius$darome+1)

# SA RÀPITA
log_gfs_sarapita   <- log(sarapita$dgfs+1)
log_icon7_sarapita <- log(sarapita$dicon7+1)
log_arome_sarapita <- log(sarapita$darome+1)

## 1) Longituds (per controlar bé el times)
n_gfs_d   <- length(log_gfs_dosrius)
n_icon7_d <- length(log_icon7_dosrius)
n_arome_d <- length(log_arome_dosrius)

n_gfs_s   <- length(log_gfs_sarapita)
n_icon7_s <- length(log_icon7_sarapita)
n_arome_s <- length(log_arome_sarapita)

## 2) Resposta (Y) en un sol vector
y <- c(
  log_gfs_dosrius, log_icon7_dosrius, log_arome_dosrius,
  log_gfs_sarapita, log_icon7_sarapita, log_arome_sarapita
)

## 3) Factor MODEL (times amb 6 enters: un per cada bloc concatenat)
model <- factor(rep(
  x = c("gfs", "icon7", "arome", "gfs", "icon7", "arome"),
  times = c(n_gfs_d, n_icon7_d, n_arome_d, n_gfs_s, n_icon7_s, n_arome_s)
))

## 4) Factor LOCALITZACIÓ (times amb 6 enters, alineat amb els mateixos blocs)
localitzacio <- factor(rep(
  x = c("Dosrius", "Dosrius", "Dosrius", "SaRapita", "SaRapita", "SaRapita"),
  times = c(n_gfs_d, n_icon7_d, n_arome_d, n_gfs_s, n_icon7_s, n_arome_s)
))

## 5) Data frame per a lm()
df <- data.frame(
  y = y,
  model = model,
  localitzacio = localitzacio
)

## 6) Ajust del model lineal múltiple i resum
fit <- lm(y ~ model + localitzacio, data = df)
summary(fit)

### IC's dels parametres del model ###
conf <- confint(fit)
print(conf)

### IC's desfets dels parametres del model ###
conf_desfet<- exp(conf)-1
print(conf_desfet)

##### ============================================================ #
##### 7) ESTUDI de les diferencies en la variabilitat dels  models
##### ============================================================ #

# vectors en funcio dels models
gfs <- c(dosrius$dgfs, sarapita$dgfs)
icon7 <- c(dosrius$dicon7, sarapita$dicon7)
arome <- c(dosrius$darome, sarapita$darome)

# IC del 95% per a la desviació estàndard (sigma) de cada model
# Assumint normalitat de la resposta (log(error+1))

alpha <- 0.05

## --- GFS ---
x <- gfs
x <- x[!is.na(x)]
n <- length(x)
s2 <- var(x)        # variància mostral (denominador n-1)
df <- n - 1

var_low  <- (df * s2) / qchisq(1 - alpha/2, df)
var_high <- (df * s2) / qchisq(alpha/2, df)

ic_sigma_gfs <- c(sigma_low = sqrt(var_low),
                  sigma_hat = sqrt(s2),
                  sigma_high = sqrt(var_high))
print(ic_sigma_gfs)

## --- ICON7 ---
x <- icon7
x <- x[!is.na(x)]
n <- length(x)
s2 <- var(x)
df <- n - 1

var_low  <- (df * s2) / qchisq(1 - alpha/2, df)
var_high <- (df * s2) / qchisq(alpha/2, df)

ic_sigma_icon7 <- c(sigma_low = sqrt(var_low),
                    sigma_hat = sqrt(s2),
                    sigma_high = sqrt(var_high))
print(ic_sigma_icon7)

## --- AROME ---
x <- arome
x <- x[!is.na(x)]
n <- length(x)
s2 <- var(x)
df <- n - 1

var_low  <- (df * s2) / qchisq(1 - alpha/2, df)
var_high <- (df * s2) / qchisq(alpha/2, df)

ic_sigma_arome <- c(sigma_low = sqrt(var_low),
                    sigma_hat = sqrt(s2),
                    sigma_high = sqrt(var_high))
print(ic_sigma_arome)

##### ============================================================ #
##### 7) ESTUDI de residus: ei = Yi - Ŷi
##### ============================================================ #

#vector de residus
residus <- c(resid(fit))

#vector temps
time_vec <- c(
  dosrius$time, dosrius$time, dosrius$time,
  sarapita$time, sarapita$time, sarapita$time
)

#convertim unitats temps
if (!inherits(time_vec, c("Date", "POSIXct", "POSIXt"))) {
  time_vec <- as.POSIXct(time_vec, tz = "Europe/Madrid", tryFormats = c(
    "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"
  ))
}

### COMPROVEM INDEPENDENCIA ### -> no hi ha patró clar -> hi ha independència
#Gràfic residu vs temps 
plot(time_vec, residus,
     xlab = "Temps (time)",
     ylab = "Residu (Yi - Ŷi)",
     main = "Residus del model vs temps",
     pch = 16)

abline(h = 0, lty = 2)

### COMPROVEM HOMOSCEDESTICITAT ENTRE RESIDUS ### -> residus centrats al voltant de zero (u = 0) i dispersió
#similar -> homoscedesticitat
# Gràfic residus vs fitted
plot(fitted(fit), residus,
     xlab = "Fitted values (Ŷi)",
     ylab = "Residu (Yi - Ŷi)",
     main = "Residus vs Fitted values (homoscedasticitat)",
     pch = 16)

abline(h = 0, lty = 2)

# (Opcional) línia suau per veure tendències (idealment ~ plana)
lines(lowess(fitted(fit), residus))

### COMPROVEM NORMALITAT DELS RESIDUS ### -> segueixen distribucio normal

# Normal Q-Q plot dels residus
qqnorm(residus,
       main = "Normal Q-Q plot dels residus",
       pch = 16)

qqline(residus, lty = 2)


#########
#BOXPLOTS
#########

### MITJANES DELS ERRORS ###
# Detransformació a escala original
gfs_dosrius_orig   <- exp(log_gfs_dosrius) - 1
icon7_dosrius_orig <- exp(log_icon7_dosrius) - 1
arome_dosrius_orig <- exp(log_arome_dosrius) - 1

gfs_sarapita_orig   <- exp(log_gfs_sarapita) - 1
icon7_sarapita_orig <- exp(log_icon7_sarapita) - 1
arome_sarapita_orig <- exp(log_arome_sarapita) - 1

# Mostra 2 gràfics en una sola finestra (1 fila, 2 columnes)
par(mfrow = c(1, 2))

boxplot(gfs_dosrius_orig, icon7_dosrius_orig, arome_dosrius_orig,
        names = c("GFS", "ICON7", "AROME"),
        main  = "DOSRIUS - Error per model",
        xlab  = "Model predicció",
        ylab  = "Error")

boxplot(gfs_sarapita_orig, icon7_sarapita_orig, arome_sarapita_orig,
        names = c("GFS", "ICON7", "AROME"),
        main  = "SA RÀPITA - Error per model",
        xlab  = "Model predicció",
        ylab  = "Error")

# (Opcional) torna al mode d'un sol gràfic per finestra
par(mfrow = c(1, 1))

### DESVIACIONS ###
sigma_hat <- c(
  sd(gfs),
  sd(icon7),
  sd(arome)
)

sigma_low <- c(
  ic_sigma_gfs["sigma_low"],
  ic_sigma_icon7["sigma_low"],
  ic_sigma_arome["sigma_low"]
)

sigma_high <- c(
  ic_sigma_gfs["sigma_high"],
  ic_sigma_icon7["sigma_high"],
  ic_sigma_arome["sigma_high"]
)

models <- c("GFS", "ICON7", "AROME")

plot(1:3, sigma_hat,
     ylim = range(c(sigma_low, sigma_high)),
     xaxt = "n",
     xlab = "Model",
     ylab = "Desviació estàndard (log(error+1))",
     main = "IC del 95% de la desviació estàndard per model",
     pch = 16)

axis(1, at = 1:3, labels = models)

arrows(1:3, sigma_low, 1:3, sigma_high,
       angle = 90, code = 3, length = 0.05)





