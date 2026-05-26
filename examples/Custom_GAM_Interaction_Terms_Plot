# ============================================================
# Simulated Minke Whale GAM Example
# Reproduces a spatial tensor interaction smooth with:
#   - Simulated trackline survey data (lon/lat + count)
#   - Negative binomial GAM fitted via mgcv
#   - image.plot colour legend (fields package)
#   - Contour lines on the response scale
#   - Original data points overlaid
# ============================================================

# --- Required packages ---
library(mgcv)      # GAM fitting
# install.packages("fields")
library(fields)    # image.plot for colour legend
library(viridis)   # colour palette


# ============================================================
# 1. SIMULATE DATA
# ============================================================
# Spatial extent: Atlantic coast, roughly 40–52°N, 15–25°W
# (mimics a typical North Atlantic minke survey region)

set.seed(42)
n_segs <- 800  # number of trackline segments

lon <- runif(n_segs, min = -25, max = -15)
lat <- runif(n_segs, min = 40,  max = 52)

# Effort (segment length in km) — log-offset in the model
effort_km <- runif(n_segs, min = 1, max = 10)

# --- True spatial pattern ---
# Whales prefer:
#   1. Cooler northern waters (higher lat)
#   2. A shelf-edge hotspot around lon = -20, lat = 47
#   3. Low counts nearshore (lon > -17)

shelf_effect  <- exp(-0.5 * ((lon - (-20))^2 / 4 + (lat - 47)^2 / 4))
north_effect  <- (lat - 40) / 12           # gradient: more whales further north
nearshore_pen <- ifelse(lon > -17, -1.5, 0) # penalty near coast

log_mu <- -3 +
  1.8 * shelf_effect +
  0.8 * north_effect +
  nearshore_pen +
  log(effort_km)  # offset for effort

mu <- exp(log_mu)

# Simulate negative binomial counts (theta = 1.5, moderately overdispersed)
count <- rnbinom(n_segs, size = 1.5, mu = mu)

# Assemble data frame
dat <- data.frame(
  lon      = lon,
  lat      = lat,
  count    = count,
  effort   = effort_km
)

cat("Summary of simulated counts:\n")
print(summary(dat$count))
cat(sprintf("Proportion of zero segments: %.1f%%\n\n",
            100 * mean(dat$count == 0)))

# ============================================================
# 2. FIT GAM
# ============================================================
# Negative binomial family; tensor interaction of lon x lat;
# log(effort) as a fixed offset

nb_model <- gam(
  count ~ ti(lon, lat, k = c(5, 5)) + offset(log(effort)),
  data   = dat,
  family = nb(),
  method = "REML",
  main = "Original"
)

cat("Model summary:\n")
print(summary(nb_model))

# ============================================================
# 3. SHOW ORIGINAL PLOT AND CAPTURE PLOT DATA 
# ============================================================
par(mfrow=c(1,2))

plot_data <- plot(nb_model,
                  select = 1,     # only one smooth in this model
                  trans  = exp,
                  scale  = 0,
                  scheme = 2)

pd <- plot_data[[1]]

# ============================================================
# 4. PLOT
# ============================================================

# Retrieve EDF for the smooth (for the title)
edf_val <- round(summary(nb_model)$s.table[, "edf"], 2)

# Colour palette: viridis (yellow = high counts)
my_cols <- rev(hcl.colors(100, "YlOrRd"))
#my_cols <- viridis(100, option = "viridis")

# --- Page layout ---
par(mfrow = c(1, 2),
    mgp   = c(3, 0.8, 0),
    mar   = c(5, 4, 4, 4))

plot(nb_model,
     select = 1,     # only one smooth in this model
     trans  = exp,
     scale  = 0,
     scheme = 2,
     xlab      = "Longitude (°)",
     ylab      = "Latitude (°)")

# --- Main plot ---
image.plot(
  pd$x, pd$y,
  matrix(exp(pd$fit), length(pd$x), length(pd$y)),
  col       = my_cols,
  xlab      = "Longitude (°)",
  ylab      = "Latitude (°)",
  main      = "With legend",
  legend.lab   = "Expected minke whales per segment",
  smallplot    = c(0.84, 0.87, 0.25, 0.75)
)

# --- Contours (response scale) ---
contour(
  pd$x, pd$y,
  matrix(exp(pd$fit), length(pd$x), length(pd$y)),
  add       = TRUE,
  col       = "black",
  lwd       = 0.7,
  labcex    = 0.55
)

# --- All segment locations (effort; semi-transparent white) ---
points(dat$lon, dat$lat,
       pch = 16,
       cex = 0.25,
       col = rgb(0, 0, 0, 0.25))



# ============================================================
# 5. QUICK DIAGNOSTICS (optional)
# ============================================================
cat("\nGratia-style check (base R):\n")
cat(sprintf("  Deviance explained: %.1f%%\n",
            100 * (1 - nb_model$deviance / nb_model$null.deviance)))
cat(sprintf("  n segments with count > 0: %d / %d\n",
            sum(dat$count > 0), nrow(dat)))
