# Makefile pour le projet de détection de couleurs et d'objets

.PHONY: all install run_controller clean help

# Cible par défaut
all: run_controller

# Installation des dépendances
install:
	pip install opencv-python numpy

# Exécution du contrôleur
run_controller:
	python controller.py

# Nettoyage (aucune action spécifique à faire pour l'instant)
clean:
	@echo "Rien à nettoyer."

# Cible d'aide pour afficher les cibles disponibles
help:
	@echo "Cibles disponibles:"
	@echo "  install          - Installe les dépendances requises"
	@echo "  run_controller   - Exécute le script controller.py"
	@echo "  clean            - Nettoie les fichiers générés (aucune action pour l'instant)"
	@echo "  help             - Affiche cette aide"
