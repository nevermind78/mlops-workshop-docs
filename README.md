# mlops-workshop-docs

[![Documentation](https://img.shields.io/badge/docs-online-brightgreen)](https://nevermind78.github.io/mlops-workshop-docs/)

Prérequis pour utiliser Azure CLI avec ces commandes

## 1. Compte Azure Actif
- Un compte Azure avec un abonnement actif
- Permissions suffisantes (Contributor ou Owner sur le groupe de ressources)

## 2. Installation d'Azure CLI

### Sur Windows :
```powershell
# Via PowerShell (admin)
winget install Microsoft.AzureCLI

# Ou téléchargement manuel
# https://aka.ms/installazurecliwindows
```

### Sur macOS :
```bash
# Via Homebrew
brew update && brew install azure-cli

# Ou téléchargement manuel
# https://aka.ms/InstallAzureCliMac
```

### Sur Linux (Ubuntu/Debian) :
```bash
# Installation
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Pour autres distributions :
# https://docs.microsoft.com/fr-fr/cli/azure/install-azure-cli-linux
```

## 3. Vérification de l'installation
```bash
# Vérifier la version
az version

# Vérifier l'installation complète
az --version
```

## 4. Connexion à Azure
```bash
# Connexion interactive (ouvre un navigateur)
az login

# Vérifier la connexion
az account show

# Lister les abonnements disponibles
az account list --output table

# Définir l'abonnement par défaut (si plusieurs)
az account set --subscription "NOM_DE_VOTRE_ABONNEMENT"
```

## 5. Extensions Azure CLI Requises
```bash
# Vérifier les extensions installées
az extension list

# Installer l'extension Container Apps (OBLIGATOIRE)
az extension add --name containerapp --upgrade

# Mettre à jour toutes les extensions
az extension update --name containerapp
```

## 6. Prérequis Docker
```bash
# 1. Docker Desktop installé et en cours d'exécution
# Windows/Mac : https://www.docker.com/products/docker-desktop/
# Linux : https://docs.docker.com/engine/install/

# 2. Vérifier l'installation Docker
docker --version
docker run hello-world

# 3. Avoir construit l'image localement
docker build -t bank-churn-api:v1 .
```

## 7. Vérification des Autorisations
```bash
# Vérifier les autorisations Azure
az role assignment list --assignee $(az account show --query user.name -o tsv) --all

# Si besoin, demander à l'administrateur Azure ces rôles :
# - Contributor (sur le groupe de ressources ou abonnement)
# - AcrPush (pour push sur ACR)
# - Web Plan Contributor (pour Container Apps)
```

## 8. Quotas Azure (importants)
Vérifier que vous avez suffisamment de quotas :
```bash
# Vérifier les quotas
az vm list-usage --location westeurope --output table

# Quotas nécessaires :
# - Container Registries : ≥1
# - Container Apps Environments : ≥1
# - vCPU pour Container Apps : ≥0.5
```

## 9. Script de Vérification Complète
```bash
#!/bin/bash
echo "=== VÉRIFICATION DES PRÉREQUIS ==="

# 1. Azure CLI
echo -n "Azure CLI : "
az version > /dev/null 2>&1 && echo "✅" || echo "❌"

# 2. Connexion Azure
echo -n "Connecté à Azure : "
az account show > /dev/null 2>&1 && echo "✅" || echo "❌"

# 3. Extensions
echo -n "Extension containerapp : "
az extension show --name containerapp > /dev/null 2>&1 && echo "✅" || echo "❌"

# 4. Docker
echo -n "Docker : "
docker --version > /dev/null 2>&1 && echo "✅" || echo "❌"

# 5. Abonnement actif
echo "Abonnement actif :"
az account show --query "{Nom:name, ID:id, État:state}" -o table

# 6. Quotas
echo "Quotas Container Apps :"
az containerapp env list --query "[].{Nom:name, RG:resourceGroup}" -o table
```

## 10. Résolution des Problèmes Courants
```bash
# Problème : Extension manquante
az extension add --name containerapp

# Problème : Non connecté
az login --use-device-code  # Si terminal sans navigateur

# Problème : Mauvais abonnement
az account list --output table
az account set --subscription "SUBSCRIPTION_ID"

# Problème : Docker non démarré
# Windows/Mac : Lancer Docker Desktop
# Linux : sudo systemctl start docker

# Problème : Permissions insuffisantes
# Contacter l'administrateur Azure pour les rôles nécessaires
```

## 11. Configuration Optionnelle mais Recommandée
```bash
# Activer la complétion automatique (Linux/macOS)
az completion --bash | sudo tee /etc/bash_completion.d/azure-cli

# Configurer la sortie par défaut
az config set core.output=table

# Activer les paramètres par défaut
az config set core.collect_telemetry=no
az config set core.only_show_errors=yes
```

## 12. Coûts à Anticiper
Les ressources créées génèrent des coûts :
- ACR Basic : ~$0.17/jour
- Container Apps : ~$0.135/vCPU/jour + $0.015/Go mémoire/jour
- Réseau : Données sortantes payantes

Pour nettoyer après les tests :
```bash
# Supprimer toutes les ressources
az group delete --name rg-mlops-workshop --yes --no-wait

# Ou supprimer proprement
az containerapp delete --name app-churn-api --resource-group rg-mlops-workshop --yes
az containerapp env delete --name env-mlops-workshop --resource-group rg-mlops-workshop --yes
az acr delete --name $ACR_NAME --resource-group rg-mlops-workshop --yes
az group delete --name rg-mlops-workshop --yes
```

## État Prêt au Déploiement
Vous êtes prêt lorsque :
- ✅ `az login` → Connecté
- ✅ `az account show` → Affiche un abonnement actif  
- ✅ `docker --version` → Version affichée
- ✅ `az extension list` → containerapp présent
- ✅ `az group create` → Test réussi

Exécutez le script de vérification pour confirmer que tous les prérequis sont satisfaits avant de commencer le déploiement.


### 14. Commandes Utiles Anaconda/Conda

#### Gestion des environnements
```bash
# Créer un nouvel environnement
conda create --name mlops-env python=3.9

# Créer un environnement avec des packages spécifiques
conda create --name mlops-env python=3.9 numpy pandas scikit-learn

# Activer un environnement
conda activate mlops-env

# Désactiver l'environnement actuel
conda deactivate

# Lister tous les environnements
conda env list
conda info --envs

# Supprimer un environnement
conda remove --name mlops-env --all
conda env remove --name mlops-env

# Cloner un environnement
conda create --name mlops-env-copy --clone mlops-env
```

#### Gestion des packages
```bash
# Installer des packages dans l'environnement actif
conda install numpy pandas matplotlib
conda install jupyter notebook scikit-learn tensorflow

# Installer une version spécifique
conda install python=3.10
conda install numpy=1.24.0

# Mettre à jour des packages
conda update numpy
conda update --all

# Supprimer un package
conda remove numpy

# Lister les packages installés
conda list
conda list --name mlops-env

# Rechercher un package
conda search tensorflow
conda search "scikit-learn>=1.0"
```

#### Exportation et réplication
```bash
# Exporter l'environnement dans un fichier YAML
conda env export --name mlops-env > environment.yml

# Exporter sans les versions de build (plus portable)
conda env export --name mlops-env --no-builds > environment.yml

# Exporter seulement les packages installés explicitement
conda env export --name mlops-env --from-history > environment.yml

# Créer un environnement à partir d'un fichier YAML
conda env create -f environment.yml

# Mettre à jour un environnement existant
conda env update -f environment.yml --prune

# Créer requirements.txt pour pip
pip freeze > requirements.txt
```

#### Nettoyage et maintenance
```bash
# Nettoyer le cache de conda
conda clean --all

# Vérifier la santé de conda
conda doctor

# Réinitialiser conda (en cas de problèmes)
conda init --reverse
conda init

# Mettre à jour conda
conda update conda
conda update anaconda

# Informations système
conda info
conda config --show
```

### 15. Commandes Utiles Docker

#### Gestion des images
```bash
# Lister les images locales
docker images
docker image ls

# Rechercher une image sur Docker Hub
docker search python

# Télécharger (pull) une image
docker pull python:3.9-slim
docker pull mcr.microsoft.com/azureml/base:latest

# Supprimer une image
docker rmi python:3.9-slim
docker image rm image_id

# Nettoyer les images non utilisées
docker image prune
docker image prune -a  # Supprimer toutes les images non utilisées

# Inspecter une image
docker inspect python:3.9-slim

# Taguer une image
docker tag bank-churn-api:v1 username/bank-churn-api:latest
```

#### Construction d'images
```bash
# Construire une image
docker build -t bank-churn-api:v1 .
docker build -t myapp:latest -f Dockerfile.prod .

# Construire sans cache
docker build --no-cache -t bank-churn-api:v1 .

# Construire avec des arguments
docker build --build-arg PYTHON_VERSION=3.9 -t bank-churn-api:v1 .

# Sauvegarder/charger une image
docker save -o bank-churn-api.tar bank-churn-api:v1
docker load -i bank-churn-api.tar
```

#### Gestion des conteneurs
```bash
# Lancer un conteneur
docker run -d -p 8000:8000 bank-churn-api:v1
docker run -it --rm python:3.9 bash

# Lancer avec variables d'environnement
docker run -e PORT=8000 -e DEBUG=True bank-churn-api:v1

# Lancer avec volume
docker run -v $(pwd):/app bank-churn-api:v1

# Lister les conteneurs
docker ps      # Conteneurs en cours d'exécution
docker ps -a   # Tous les conteneurs

# Arrêter/démarrer des conteneurs
docker stop container_id
docker start container_id
docker restart container_id

# Supprimer des conteneurs
docker rm container_id
docker rm $(docker ps -aq)  # Supprimer tous les conteneurs arrêtés

# Exécuter une commande dans un conteneur
docker exec -it container_id bash
docker exec container_id python manage.py migrate

# Voir les logs
docker logs container_id
docker logs -f container_id  # Suivre en temps réel

# Inspecter un conteneur
docker inspect container_id
docker stats container_id    # Ressources utilisées
```

#### Docker Compose (si utilisé)
```bash
# Démarrer les services
docker-compose up
docker-compose up -d        # Mode détaché
docker-compose up --build   # Reconstruire les images

# Arrêter les services
docker-compose down
docker-compose down -v      # Supprimer aussi les volumes

# Voir les logs
docker-compose logs
docker-compose logs -f service_name

# Lancer une commande dans un service
docker-compose exec web python manage.py migrate
```

#### Nettoyage Docker
```bash
# Nettoyer tous les conteneurs arrêtés
docker container prune

# Nettoyer tous les éléments non utilisés
docker system prune
docker system prune -a      # Plus agressif

# Voir l'espace utilisé
docker system df

# Supprimer tous les conteneurs et images
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
```

#### Docker pour le développement ML
```bash
# Lancer Jupyter dans Docker
docker run -p 8888:8888 -v $(pwd):/workspace jupyter/datascience-notebook

# Lancer un serveur MLflow
docker run -p 5000:5000 mlflow/mlflow

# Construire une image pour un modèle ML
docker build -t ml-model:latest -f Dockerfile.ml .

# Tester l'API de prédiction
docker run -p 5000:5000 ml-model:latest
curl -X POST http://localhost:5000/predict -d '{"data": [...]}'
```

#### Intégration avec Azure
```bash
# Se connecter à Azure Container Registry
az acr login --name votreACR

# Taguer une image pour ACR
docker tag bank-churn-api:v1 votreACR.azurecr.io/bank-churn-api:v1

# Pousser l'image vers ACR
docker push votreACR.azurecr.io/bank-churn-api:v1

# Tirer une image depuis ACR
docker pull votreACR.azurecr.io/bank-churn-api:v1
```
