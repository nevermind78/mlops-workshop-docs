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
