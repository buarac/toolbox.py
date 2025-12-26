# **🚀 MISSION : Python Automation Toolbox**

L'objectif est de créer un écosystème de scripts Python ("Toolbox") structuré, portable (macOS & Ubuntu) et évolutif. Ce projet permet de générer, stocker et exécuter des scripts utilitaires variés à la demande, tout en centralisant la gestion des dépendances.

## **🛠️ STACK TECHNIQUE**

* **Langage** : Python 3.12+  
* **Compatibilité** : Multi-OS (macOS Sonoma+ et Ubuntu 22.04+)  
* **Gestion des libs** : requirements.txt (centralisé à la racine)  
* **Structure** : Architecture modulaire avec un dossier dédié par script ou un dossier /scripts global.  
* **Entry Point** : toolbox.py pour la gestion et l'appel des utilitaires.

## **📋 BACKLOG INITIAL**

### **🏁 Lot 0 : Architecture & Fondations (Sprint 0\)**

* Initialisation de l'arborescence (/scripts, /docs, /core).  
* Création du requirements.txt initial et d'un script de check de compatibilité OS.  
* Configuration de l'environnement virtuel et du linter (Ruff/Black).

### **🛠️ Lot 1 : Le Cœur "Toolbox"**

* Développement de toolbox.py : CLI pour lister, décrire et lancer les scripts existants.  
* Mise en place du workflow de création : Ajout automatique d'un nouveau script via une commande dédiée.

### **📦 Lot 2 : Gestion des Dépendances & Portabilité**

* Mécanisme de mise à jour automatique de requirements.txt lors de l'ajout de scripts.  
* Validation de la compatibilité des chemins (utilisation de pathlib) pour macOS et Ubuntu.

## **⚙️ RAPPEL OPÉRATIONNEL**

L'application stricte des **GLOBAL\_RULES** est impérative :

1. **Sprint 0** obligatoire avant toute feature.  
2. Développement par **lots fonctionnels** avec validation entre chaque étape.  
3. Utilisation systématique de **branches Git** par lot.  
4. Mise à jour post-merge de **README.md**, **CONTEXT.md** et **BACKLOG\_DONE.md**.

## **🏁 PREMIÈRE ÉTAPE**

"Initialise le projet et présente le plan détaillé du Sprint 0 pour validation."