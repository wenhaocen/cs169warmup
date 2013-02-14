from django.db import models

# Create your models here.
SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

class User(models.Model):
	userName = models.TextField(max_length=128, primary_key=True, blank=False)
	password = models.TextField(max_length=128)
	count = models.IntegerField()
	
	def __unicode__(self):
		return str((self.userName, self.password, self.count))
	def TESTAPI_resetFixture(self):
		User.objects.all().delete()
		return SUCCESS
	def add(self,inUserName,inPwd):
		if self.userExist(inUserName)[0]:
			return ERR_USER_EXISTS
		if not self.validateUsername(inUserName):
			return ERR_BAD_USERNAME
        	if not self.validatePassword(inPwd):
			return ERR_BAD_PASSWORD
		tobeAdd = User(userName=inUserName, password = inPwd,count=1)
		tobeAdd.save()
		return 1

	def login(self, inUserName, inPwd):
		temp = self.userExist(inUserName)
		if temp[0] and temp[1].password == inPwd:
			#Auth succeed
			temp[1].count+=1
			tempCount = temp[1].count
			temp[1].save()
			return tempCount
		else:
			return ERR_BAD_CREDENTIALS




	def userExist(self,username):
		try:
			dbresult = User.objects.get(userName = username)
			Exist = True
		except:
			Exist=False
			dbresult = ""
		return (Exist,dbresult)

	def validateUsername(self, name):
		return name!="" and len(name)<=	128
	def validatePassword(self, pwd):
		return len(pwd)<=128
