# scripts/script.R

# Liste des packages nécessaires
packages <- c("ggplot2", "jsonlite")

# Fonction pour installer les packages manquants
install_if_missing <- function(p) {
    if (!require(p, character.only = TRUE)) {
        install.packages(p, repos = "http://cran.us.r-project.org")
        library(p, character.only = TRUE)
    }
}

# Installer les packages nécessaires
lapply(packages, install_if_missing)

# Générer les données et le graphique
args <- commandArgs(trailingOnly = TRUE)
plot_path <- args[1]

# Débogage
print(paste("Saving plot to:", plot_path))

data <- data.frame(x = c(1, 2, 3, 4), y = c(5, 6, 7, 8))
png(plot_path)
ggplot(data, aes(x=x, y=y)) + geom_line()
dev.off()

# Confirmer la fin de l'exécution
print("Plot saved successfully.")