# leximpact-survey-scenario


🇬🇧 This repository is created for internal use at [LexImpact](http://LexImpact.an.fr). Nevertheless, if you are interested in this source code, please do not hesitate to contact us! It defines a `LeximpactErfsSurveyScenario` class that allows computations of the effect of the French legislation on a population.  
The legislation model is [OpenFisca-France](https://github.com/openfisca/openfisca-france). The population is built from a revision (FPR) of an [INSEE survey called ERFS](https://www.insee.fr/fr/metadonnees/source/serie/s1231). 

🇲🇫 Ce dépôt est créé à des fins d'usage interne de l'équipe [LexImpact](http://LexImpact.an.fr). Néanmoins, si vous êtes intéressé par ce code source, n'hésitez pas à nous contacter ! Il définit une classe `LeximpactErfsSurveyScenario` permettant les calculs des effets de la législation Française sur une population.  
Le modèle de la législation est [OpenFisca-France](https://github.com/openfisca/openfisca-france). La population est construite à partir d'une version (FPR, Fichiers de Production et Recherche) d'une [enquête INSEE nommée ERFS](https://www.insee.fr/fr/metadonnees/source/serie/s1231).

## Installer `leximpact-survey-scenario`

### Pré-requis

Ce dépôt requiert le langage [Python](https://www.python.org). 

### Installer en mode développement

La gestion des dépendances et du paquetage est effectuée avec [Poetry](https://python-poetry.org).

#### Installer le code source et ses dépendances

Récupérer le code source de l'application avec la commande suivante :

```shell
git clone git@git.leximpact.dev:leximpact/leximpact-survey-scenario.git
```

Puis installer l'application dans un environnement virtuel avec :

```shell
cd leximpact-survey-scenario
make install
```

#### Configurer

Si vous utilisez déjà [openfisca-survey-manager](https://github.com/openfisca/openfisca-survey-manager) et/ou [openfisca-france-data](https://github.com/openfisca/openfisca-france-data) vous disposez probablement déjà d'une configuration des fichiers de données (collections de fichiers de population) dans votre répertoire `$HOME/.config/openfisca-survey-manager`. Par défaut, `leximpact-survey-scenario` hérite du comportement d'`openfisca-survey-manager` et utilisera cette configuration.

En l'absence d'une configuration dans `$HOME/.config/openfisca-survey-manager`, la configuration de ce dépôt sera utilisée : `./.config/openfisca-survey-manager/config.ini`.

### Tester

Après avoir installé et configuré le dépôt, les tests de `leximpact-survey-scenario` peuvent être exécutés en local avec la commande suivante :

```shell
make test
```

###  Publier

La dépendance à une branche de France-reforms empêche de publier cette partie du code source sur PyPI. Néanmoins, nous publions le package `leximpact-survey-scenario` sur PyPI dans la CI en supprimant automatiquement cette dépendance à la volée.
