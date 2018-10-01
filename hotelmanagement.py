from validation import Validate
import datetime
from datetime import date
import MySQLdb
class HotelManagement:
	uid=0
	uname=""
	def __init__(self):
		print("init")
		self.db = MySQLdb.connect("localhost","root","root","hoteldb" )
		self.cursor=self.db.cursor()
		sql="select * from tenants"
		try:
			self.cursor.execute(sql)
			records=self.cursor.fetchall()
			for rec in records:
				print(rec[6])
				lfdt=rec[6].split("-")
				leftdt=date(int(lfdt[0]),int(lfdt[1]),int(lfdt[2]))
				todaydt=date.today()
				datediff=leftdt-todaydt
				if datediff.days==0:
					sql="update suprabat_rooms set booked='no' where roomnumber='%d'"%(rec[1])
					sql1="delete from tenants where userid='%d'"%(rec[0])
					try:
						self.cursor.execute(sql)
						self.db.commit()
						self.cursor.execute(sql1)
						self.db.commit()
					except:
						self.db.rollback()
						print("UNABLE TO UPDATE")
		except:
			self.db.rollback()
			print("UNABLE TO UPDATE")
	def signUp(self):
		validtobj=Validate()
		validtobj.setname(input("enter the username: "))        
		validtobj.setmail(input("enter the mail: ")) 
		validtobj.setmobile_no(input('enter the mobile no: '))
		validtobj.setplace(input('enter the native place: ')) 
		pass1=input("enter the password: ")
		pass2=input("Re enter the password: ")
		validtobj.setpassword(pass1,pass2)
		uname=validtobj.username
		sql="select userid from users order by userid"
		try:
			self.cursor.execute(sql)
			records=self.cursor.fetchall()
			if len(records)==0:
				validtobj.id=1001
			else:
				validtobj.id=records[-1][0]
				validtobj.id+=1
		except:
			self.db.rollback()
			print(" unable to READ from users table")
		print(validtobj.id,validtobj.username,validtobj.password,validtobj.mail,int(validtobj.mobile_no),validtobj.place)
		sql1 = "insert into users values('%d','%s','%s','%s','%d','%s')"%(validtobj.id,validtobj.username,validtobj.password,validtobj.mail,int(validtobj.mobile_no),validtobj.place)
		try:
			self.cursor.execute(sql1)
			self.db.commit()
			print("successfully inserted")
		except:
			self.db.rollback()
			print(" unable to insert new user")
			states="succ"
		self.mainMenu()
	def signIn(self):
		username=input("enter username :")
		password=input("enter password :")
		sql="select userid,username from users where username='%s' and password='%s'"%(username,password)
		self.cursor.execute(sql)
		result=self.cursor.fetchall()
		while len(result)==0:
			print("Invalid account")
			username=input("enter username :")
			password=input("enter password :")
			sql="select * from users where username='%s' and password='%s'"%(username,password)
			self.cursor.execute(sql)
			result=self.cursor.fetchall()
		else:
			states="succ"
			print("succc....")
			if len(result)!=0:
				self.uid=result[0][0]
				self.uname=result[0][1]
		self.roomBooking()	
				
				
	def mainMenu(self):
		choice=int(input("1.Sign Up \n 2.Login \n 3.forgot password\n "))
		if choice==1:             
			self.signUp()
		elif choice==2:
			self.signIn()
		else:
			self.forgotPass()


	def roomBooking(self):
		while(1):
			slt=int(input("1.Hotel Suprabat\n 2.Hotel Haritha\n 3. logout"))
			if slt==1:
				print("1.signle bed rooms\n 2.double bed rooms\n")
				roomtype=int(input("please select room type"))
				if roomtype==1:
					roomtype1="single bed room"
				else: 
					roomtype1="double bed room"
				aminity=int(input("1.AC\n 2.Non AC\n please enter AC or Non AC\n"))
				if aminity==1:
					amty="AC"
				else:
					amty="NON AC"
				sql="select roomnumber,roomtype,aminity,cost from suprabat_rooms where booked='no' and roomtype='"+roomtype1+"' and aminity='"+amty+"'"
				try:
					self.cursor.execute(sql)
					self.db.commit()
				except:
					self.db.rollback()
					print(" error ----------122-------")
				recs=self.cursor.fetchall()
				for row in recs:
					print(row[0],"  ",row[1],"   ",row[2],"   ",row[3],"\n")
					cost=row[3]
				roomid=int(input("enter room number"))
				days=int(input("enter no of days"))
				print("you have selected ",roomtype1,"with ",amty," for ",days,"days room cost is : ",days*cost)
				sql="insert into tenants(userid,roomnumber,tenantname,room_type,aminity,booked_date,left_date,amount_paid)values('%d','%d','%s','%s','%s','%s','%s','%d')"%(self.uid,roomid,self.uname,roomtype1,amty,str(date.today()),str(date.today()+datetime.timedelta(days)),days*cost)
				try:
					self.cursor.execute(sql)
					self.db.commit()
				except:
					self.db.rollback()
					print("UNABLE TO INSERT RECORD INTO TENANTS TABLE")
				sql="update suprabat_rooms set booked='YES' where roomnumber='%d'"%(roomid)
				
				try:
					self.cursor.execute(sql)
					self.db.commit()
				except:
					self.db.rollback()
					print("UNABLE TO UPDATE SUPRABAT_ROOMS TABLE")
					print("thank you")
			elif slt==2:
				print("Haritha is not yet implemented")
			elif slt==3:
				break
	def forgotPass(self):
		forgot=int(input("Did you forget password Enter 1 for yes"))
		if forgot==1:
			username=input("enter your username")
			phno=int(input("enter the mobile number which you have used for registation"))
			sql="select * from users where username='%s' and mobile='%d'"%(username,phno)
			try:
				self.execute(sql)
				db.commit()
			except:
				db.rollback()
			mno=self.fetchall()
			if mno!=0:
				password=input("enter the new password")
				sql="update users set password='%s' where mobile='%d'"%(password,phno)
				try:
					rec.execute(sql)
					db.commit()
					states="succ"
				except:
					db.rollback()
					print("unable to update password")
				else:
					print("Invalid user")
					states="not succ"


if __name__=='__main__':
	HMobj=HotelManagement()
	HMobj.mainMenu()
