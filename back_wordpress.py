import os				#
import tarfile				#
import time				# Modules importation
import boto3				#
import shutil				#
import logging				#
import logging.handlers as handlers	#

### Base Variables ###
session = boto3.Session(profile_name='default') 
s3 = boto3.client('s3')							# authentification on Amazon S3
bucket_name = 'projet9oc'						# MODIFY ME: S3 directory name to use
backup_dir = '/home/administrateur/Documents/wordpress'			# MODIFY ME: Local path for the backup
source = '/var/www/html/wordpress'					# MODIFY ME IF NECESSARY: installation path for wordpress
date = (time.strftime("%d-%m-%Y"))					# Date of the day
now = time.time()							# Date and time when the script is launch
old = now - 86400							# MODIFY ME: Number of day (in secondes) before old directory deletion (1 day in the actual configuration)
site_name = 'monsite'							# MODIFY ME: Name of the site (used in directory and file creation for the backup), You can use anything you want.
database = 'wordpress1'							# MODIFY ME IF NECESSARY: Name of the wordpress database
backdir = backup_dir+'/'+date+'/'+site_name+'/'				# Variable for the directory creation of the day (use date of the day and name of the site)
login = 'user'								# MODIFY ME IF NECESSARY: Login for the wordpress database
password = 'user'							# MODIFY ME IF NECESSARY: Password for the wordpress database
filename = date+site_name+'.tar.gz'					# Variable for the archive name uploaded on S3
######

### Logging configuration ###
logger = logging.getLogger ('backup_wp')								#MODIFY ME IF NECESSARY: Logging ID
logger.setLevel(logging.INFO)										#MODIFY ME IF NECESSARY: General Logging level	
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')			#MODIFY ME IF NECESSARY: Logging message format
logHandler = handlers.TimedRotatingFileHandler('backup_wp.log', when='D', interval=1, backupCount=7)	#MODIFY ME IF NECESSARY: Create a new file each day for a maximum of 7 files
logHandler.setLevel(logging.INFO)									#Logging level
logHandler.setFormatter(formatter)									#Application of the format
logger.addHandler(logHandler)										#Record of this logging file
######

### We delete the old directories ###
def del_old_dir():
	for root, dirs, filles in os.walk(backup_dir):			
	   for dir in dirs:						# For all the directory in the backup folder
	      old_dir = os.path.getmtime(os.path.join(root, dir))	# we retrieve the date of last modification
	      if old > old_dir:						# we compare with the old variable to determine wich directory need to be removed
	         try:
		    shutil.rmtree(os.path.join(root, dir))		# we delete the old directories
		 except Exception,e:
		    print error      
	logger.info("Old directories deleted")
######

### We create the backup directory of the day ###
def create_dir():
	os.makedirs(backup_dir+'/'+date+'/'+site_name+'/')
	logger.info("Directory backup created")		
######

### We retrieve the content of the database in a sql file ###		
def backup_database():
	os.system("mysqldump -u "+login+" -p"+password+" "+database+" > "+backdir+date+database+".sql")
	logger.info("Sql file created")	
######

### We create the archive and upload it ###
def make_tar_and_upload_s3():
	archive_name = os.path.normpath(backdir+'/'+filename)		# We create a variable that keep in memory the path of the archive
	with tarfile.open(archive_name, "w:gz") as tar:			# We open a tar file
		tar.add(source)						# We add the worpress folder
		tar.add(backdir)					# We add the sql file
	s3.upload_file(archive_name, bucket_name, 'sauvegardes'+'/'+filename)	#We send our archive on S3
	logger.info("Archive created and uploaded")
######
	
#### We delete our sql file ###
def del_database():
	os.remove(backdir+date+database+".sql")	
	logger.info("Sql File deleted")			
######

def main():
	del_old_dir()
	create_dir()
	backup_database()
	make_tar_and_upload_s3()
	del_database()
	
if __name__ == '__main__':
	main()
