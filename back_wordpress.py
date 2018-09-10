# les commandes print sont commentées car ce fichier est censé être automatique mais elles sont laissées en place pour un test du script plus aisé.

import os	#
import tarfile	#
import time	# Importation des différents modules
import boto3	#
import shutil	#

session = boto3.Session(profile_name='default') 
s3 = boto3.client('s3')							# authentification sur Amazon S3
bucket_name = 'projet9oc'						# A MODIFIER: Nom du dossier S3 à utiliser
backup_dir = '/home/administrateur/Documents/wordpress'			# A MODIFIER: chemin du dossier local pour les sauvegardes
source = '/var/www/html/wordpress'					# A MODIFIER SI NECESSAIRE: chemin d'installation de Wordpress
date = (time.strftime("%d-%m-%Y"))					# Date du jour
now = time.time()							# Date et heure au moment du lancement du script
old = now - 86400							# A MODIFIER: Nombre de jours (en secondes) avant de supprimer les anciens répertoires (1 jour dans la configuration actuelle)
site_name = 'monsite'							# A MODIFIER: Nom du site (sert à créer les noms des dossiers et fichiers de sauvegarde), vous pouvez mettre ce que vous souhaitez
database = 'wordpress1'							# A MODIFIER SI NECESSAIRE: Nom de la base de données wordpress
backdir = backup_dir+'/'+date+'/'+site_name+'/'				# Varaible pour la création du dossier de sauvegarde du jour (prend en compte la date du jour et le nom du site)
login = 'user'								# A MODIFIER SI NECESSAIRE: Login d'accès à la base de données Mysql
password = 'user'							# A MODIFIER SI NECESSAIRE: Mot de passe d'accès à la base de données Mysql
filename = date+site_name+'.tar.gz'					# Variable pour la création de l'archive qui sera uploadée.

def del_old_dir():
	for root, dirs, filles in os.walk(backup_dir):			
	   for dir in dirs:						# Pour tous les répertoires placés dans la dossier de backup
	      old_dir = os.path.getmtime(os.path.join(root, dir))	# on récupére la date de dernière modification
	      if old > old_dir:						# on compare cette date avec notre variable pour déterminer les dossiers suffisament agés pour être supprimés
	         try:
		    #print "removing", os.path.join(root, dir)		
		    shutil.rmtree(os.path.join(root, dir))		# on supprime les dossiers et leur contenu
		 except Exception,e:
		    print error      
	     
def create_dir():				
	os.makedirs(backup_dir+'/'+date+'/'+site_name+'/')		# On crée le dossier de backup du jour
	#print 'Directory of the day created'
	
def backup_database():
	os.system("mysqldump -u "+login+" -p"+password+" "+database+" > "+backdir+date+database+".sql")	# On récupère le contenu de la base de données en fichier sql
	#print 'Backup Database done'	

def make_tar_and_upload_s3():
	archive_name = os.path.normpath(backdir+'/'+filename)		# On crée une variable archive_name qui garde en mémoire le chemin d'accès à l'archive
	with tarfile.open(archive_name, "w:gz") as tar:			# on ouvre une archive tar 
		tar.add(source)						# On ajoute le dossier wordpress
		tar.add(backdir)					# on ajoute le fichier sql
	#print 'archivage OK'
	s3.upload_file(archive_name, bucket_name, 'sauvegardes'+'/'+filename)	#On envoie notre archive sur S3
	#print 'file upload done'

def del_database():
	os.remove(backdir+date+database+".sql")				# Finalement on supprime notre fichier sql

def main():
	del_old_dir()
	create_dir()
	backup_database()
	make_tar_and_upload_s3()
	del_database()
	
if __name__ == '__main__':
	main()