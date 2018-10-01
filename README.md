# Wordpress_backup_py2.7
Script de backup pour un site wordpress en python 2.7.

(Ce script est créé dans la cadre de la formation Administrateur Infrastructures et Cloud d'Openclassrooms.)

Il est utilisé pour réaliser une sauvegarde d'un site wordpress automatiquement (en l'ajoutant dans une tâche cron) une fois par jour. Il fournit aussi une base simple de logs automatique pour faire un suivi des sauvegardes.
Tout le script est commenté et il est possible de modifier un certain nombre de variables. 

Il n'est pas totalement fonctionel en l'état puisque qu'il faut un petit fichier d'authentification nommé credentials, à placer normalement dans le dossier ~/.aws/.
Ce fichier permet au SDK Boto3 de s'authentififier à Amazon S3 afin dy envoyer le fichier.

Je vous laisse découvrir le script au travers des commentaires internes.

Voici une description des variables:

### Base Variables ###
- session = boto3.Session(profile_name='default') -> Le profil des sessions Boto3 généralement à laisser comme ca.
- s3 = boto3.client('s3')	-> Le type de service souhaité avec boto3 sur Amazon (ici connexion à S3). S3 est un stockage en ligne dont une partie est gratuite et proposé par amazon.					
- bucket_name = 'projet9oc'	-> Le dossier S3 dans lequel mettre les fichiers (à vous de mettre le votre).
- backup_dir = '/home/administrateur/Documents/wordpress'	-> Le dossier local pour stocker les fichiers (à modifier à votre convenance).
- source = '/var/www/html/wordpress' -> Le chemin local d'installation de wordpress (à modifier si nécessaire).
- date = (time.strftime("%d-%m-%Y")) -> La date du jour (pas besoin d'y toucher).
- now = time.time()	-> Récupération de le date et de l'heure quand le script est lancé (pas besoin d'y toucher).
- old = now - 86400	-> La durée pendant laquelle les dossiers de sauvegarde sont gardés en secondes (ici juste un jour, à changer pour une durée plus réglementaire).
- site_name = 'monsite'	-> Le nom du site, sert à créer un sous-dossier dans le dossier de sauvegarde vu plus haut (mettez ce que vous voulez).
- database = 'wordpress1'	-> le nom de votre base de données contenant les données wordpress (bien sur à modifier suivant votre configuration).
- backdir = backup_dir+'/'+date+'/'+site_name+'/'	-> sert pour la création du sous-dossier de sauvegarde (modifiez ceci si vous savez ce que vous faites).
- login = 'user' -> le login d'accès à votre base de données Mysql (à modifier suivant l'utilisateur qui a l'accès à la base de données.).
- password = 'user'	-> le mot de passe pour l'accès à votre base de données Mysql (à modifier suivant l'utilisateur qui a l'accès à la base de données).
- filename = date+site_name+'.tar.gz' -> Sert pour la création du nom de l'archive (modifiez ceci si vous savez ce que vous faites).
######

### Logging configuration ###
- logger = logging.getLogger ('backup_wp')	-> Id de login (peut être ce que vous voulez, c'est juste pour s'y retrouver).
- logger.setLevel(logging.INFO)	-> Le niveau de logging déclaré (je vous invite à consulter la documentation lié à la fonction logging de python avant de modifer ceci).
- formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')	-> Le format du message écrit dans le fichier de log (Peut être modifier si vous savez ce que vous faites).
- logHandler = handlers.TimedRotatingFileHandler('/home/administrateur/Bureau/backup_wp.log', when='D', interval=1, backupCount=7) -> Ce paramètre permet de définir combien de fichiers logs l'on veut, comment ils sont créés et leur localisation. Ici on crée un fichier par jour et on les gardent 7 jours (donc 7 fichiers) ensuite les fichiers sont réécrits (peut être modifier si vous savez ce que vous faites).
- logHandler.setLevel(logging.INFO)	-> Niveau de logging pour les futurs logs (peut être modifier si vous savez ce que vous faites).
- logHandler.setFormatter(formatter) -> Application du format choisi sur les messages "logHandler" (Pas de raison de modifier ceci).
- logger.addHandler(logHandler) -> Enregistrement de la configuration précédente (peut être modifier si vous savez ce que vous faites).
######

Instructions d'installation:

Comme précisé plus haut, ce script est fait pour être exécuté tous les jours par une tâche cron. Il est important de toujours utiliser le même utilisateur pour lancer ce script (pas besoin d'accès root) pour une question de droit sur les dossiers et fichiers et d'accès au fichier de configuration boto3.
Concernant la connexion à Amazon S3, il faut placer dans le répertoire home de l'utilisateur qui lance le script un dossier /.aws contenant un fichier credentials, je vous invite à consulter la documentation de boto3 pour aller plus loin. 
