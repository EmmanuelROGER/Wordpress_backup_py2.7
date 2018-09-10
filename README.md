# Wordpress_backup_py2.7
Script de backup pour un site wordpress en python 2.7.
Ce script est créé dans la cadre de la formation Administrateur Infrastructures et Cloud d'Openclassrooms.
Il est utilisé pour réaliser une sauvegarde d'un site wordpress automatiquement (en l'ajoutant dans un tâche cron) une fois par jour.
Tout le script est commenté et il est possbile de mofifier un certain nombre de variables. 
Il n'est pas totalement fonctionel en l'état puisque qu'il faut un petit fichier d'authentification nommé credentials, à placer normalement dans le dossier ~/.aws/. 
Ce fichier permet au SDK Boto3 de s'authentififier à Amazon S3 afin dy envoyer le fichier.
