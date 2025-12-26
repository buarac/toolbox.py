# **📜 RÈGLES SPÉCIFIQUES : Projet Toolbox Python**

Ce document définit les standards techniques pour la création et la maintenance des scripts au sein de la boîte à outils.

## **📂 ARCHITECTURE DES DOSSIERS**

* /scripts/ : Contient les scripts unitaires. Si un script devient complexe, il doit avoir son propre sous-dossier.  
* /core/ : Contient les fonctions utilitaires partagées (ex: gestion des logs, accès fichiers, parsing de config).  
* /requirements.txt : UNIQUE source de vérité pour toutes les librairies du projet.

## **⌨️ CONVENTIONS DE CODE & PYTHON**

### **🍎 Compatibilité OS (macOS / Ubuntu)**

* **Interdiction** d'utiliser des chemins codés en dur avec / ou \\. Utiliser exclusivement la librairie pathlib.  
* Toute commande système (via subprocess) doit vérifier os.name ou le module platform pour adapter les flags.  
* Privilégier les librairies cross-platform (ex: psutil pour les processus, shutil pour les fichiers).

### **📦 Gestion des Librairies**

* Chaque nouveau script ajouté doit être accompagné d'une vérification de ses dépendances.  
* Si une nouvelle librairie est nécessaire, elle doit être ajoutée au fichier requirements.txt avec sa version (lib==x.y.z).  
* Ajouter un commentaire dans requirements.txt pour indiquer quel script utilise quelle lib si elle est spécifique.

### **📝 Structure d'un Script "Outil"**

Chaque script dans /scripts/ doit suivre ce template minimal :

1. **Docstring** : Description claire de l'action, entrées/sorties et OS testés.  
2. **Shebang** : \#\!/usr/bin/env python3.  
3. **Main Guard** : if \_\_name\_\_ \== "\_\_main\_\_": obligatoire.  
4. **Logging** : Utilisation du module logging plutôt que print().
5. **Emojis** : Les outputs utilisateur (logs INFO/ERROR) DOIVENT utiliser des emojis pour améliorer la lisibilité (ex: ✅, ❌, 🚀, 📦).

## **🧠 LOGIQUE MÉTIER DE GÉNÉRATION**

* Lorsqu'un nouveau script est "commandé", l'agent doit d'abord vérifier si une fonction existante dans /core/ peut être réutilisée.  
* L'agent doit automatiquement mettre à jour le README.md principal pour inclure le nouveau script dans la liste des outils disponibles.

## **📊 VISUALISATION & ARTEFACTS**

* **Mermaid** : Lors de la génération de diagrammes Mermaid (flowchart, graph, etc.), il est **impératif de mettre des guillemets** autour des libellés contenant des caractères spéciaux, des espaces ou des émojis.
    * ❌ Incorrect: `Start --> Do(Action 🚀)`
    * ✅ Correct: `Start --> Do("Action 🚀")`