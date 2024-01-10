import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean


filename="codesAndBarcodes.db"
DEVMOD=False
if DEVMOD:
	if Path(filename).exists():
		Path(filename).unlink()
dbfile="sqlite:///"+str(filename)
print(dbfile)
#import sqlite3
#z=sqlite3.connect(filename)
#print(z)
ENGINE=create_engine(dbfile)
BASE=dbase()
#BASE.prepare(autoload_with=ENGINE)

class StartStop(BASE):
	__tablename__="StartStop"
	Start=Column(DateTime)
	Stop=Column(DateTime)
	Start_Location=Column(String)
	Stop_Location=Column(String)
	StartStopId=Column(Integer,primary_key=True)

	def __repr__(self):
		return f"StartStop(Start={self.start},Stop={self.stop},StartStopId={self.StartStopId},Start_Location={self.Start_Location},Stop_Location={self.Stop_Location})"
	def __init__(self,Start,Stop=None,Start_Location=None,Stop_Location=None,StartStopId=None):
		if StartStopId != None:
			self.StartStopId=StartStopId
		self.Start=Start
		if Stop != None:
			self.Stop=Stop
		if Stop_Location:
			self.Stop_Location=Stop_Location
		if Start_Location:
			self.Start_Location=Start_Location


class Entry(BASE):
	__tablename__="Entry"
	Code=Column(String)
	Barcode=Column(String)
	#not found in prompt requested by
	'''
	#name {Entryid}
	#name {Entryid} {new_value}
	
	#price {Entryid}
	#price {Entryid} {new_value}

	#note {Entryid}
	#note {Entryid} {new_value}
	
	#size {Entryid} 
	#size {Entryid} {new_value}
	'''
	Name=Column(String)
	Price=Column(String)
	Note=Column(String)
	Size=Column(String)
	
	CaseCount=Column(Integer)

	Shelf=Column(Integer)
	BackRoom=Column(Integer)
	Display_1=Column(Integer)
	Display_2=Column(Integer)
	Display_3=Column(Integer)
	Display_4=Column(Integer)
	Display_5=Column(Integer)
	Display_6=Column(Integer)
	InList=Column(Boolean)
	Stock_Total=Column(Integer)
	Location=Column(String)
	ListQty=Column(Float)
	upce2upca=Column(String)

	EntryId=Column(Integer,primary_key=True)
	Timestamp=Column(Float)
	def __init__(self,Barcode,Code,upce2upca='',Name='',InList=False,Price=0.0,Note='',Size='',CaseCount=0,Shelf=0,BackRoom=0,Display_1=0,Display_2=0,Display_3=0,Display_4=0,Display_5=0,Display_6=0,Stock_Total=0,Timestamp=datetime.now().timestamp(),EntryId=None,Location='///',ListQty=0.0):
		if EntryId:
			self.EntryId=EntryId
		self.Barcode=Barcode
		self.Code=Code
		self.Name=Name
		self.Price=Price
		self.Note=Note
		self.Size=Size
		self.Shelf=Shelf
		self.CaseCount=CaseCount
		self.BackRoom=BackRoom
		self.Display_1=Display_1
		self.Display_2=Display_2
		self.Display_3=Display_3
		self.Display_4=Display_4
		self.Display_5=Display_5
		self.Display_6=Display_6
		self.Stock_Total=Stock_Total
		self.Location=Location
		self.Timestamp=Timestamp
		self.InList=InList
		self.ListQty=ListQty
		self.upce2upca=upce2upca

	def __repr__(self):
		return f"""{Style.bold}{Style.underline}{Fore.pale_green_1b}Entry{Style.reset}(
		{Fore.hot_pink_2}{Style.bold}{Style.underline}EntryId{Style.reset}={self.EntryId}
		{Fore.violet}{Style.underline}Code{Style.reset}='{self.Code}',
		{Fore.orange_3}{Style.bold}Barcode{Style.reset}='{self.Barcode}',
		{Fore.orange_3}{Style.underline}UPCE to UPCA[if any]{Style.reset}='{self.upce2upca}',
		{Fore.green}{Style.bold}Price{Style.reset}=${self.Price},
		{Fore.red}Name{Style.reset}='{self.Name}',
		{Fore.tan}Note{Style.reset}='{self.Note}',
		{Fore.pale_green_1b}Timestamp{Style.reset}='{datetime.fromtimestamp(self.Timestamp).strftime('%D@%H:%M:%S')}',
		{Fore.deep_pink_3b}Shelf{Style.reset}={self.Shelf},
		{Fore.light_steel_blue}BackRoom{Style.reset}={self.BackRoom},
		{Fore.cyan}Display_1{Style.reset}={self.Display_1},
		{Fore.cyan}Display_2{Style.reset}={self.Display_2},
		{Fore.cyan}Display_3{Style.reset}={self.Display_3},
		{Fore.cyan}Display_4{Style.reset}={self.Display_4},
		{Fore.cyan}Display_5{Style.reset}={self.Display_5},
		{Fore.cyan}Display_6{Style.reset}={self.Display_6},
		{Fore.light_salmon_3a}Stock_Total{Style.reset}={self.Stock_Total},
		{Fore.magenta_3c}InList{Style.reset}={self.InList}
		{Fore.yellow}ListQty{Style.reset}={self.ListQty}
		{Fore.misty_rose_3}Location{Style.reset}={self.Location}
		{Fore.sky_blue_2}CaseCount{Style.reset}={self.CaseCount}
		{Fore.sky_blue_2}Size{Style.reset}={self.Size}
		)
		"""
StartStop.metadata.create_all(ENGINE)
Entry.metadata.create_all(ENGINE)
tables={
	'ss':StartStop,
	'Entry':Entry
}
class Main:
	def __init__(self,engine,tables,error_log):
		self.engine=engine
		self.tables=tables
		self.error_log=error_log
		self.modes={
		'1':{
		'cmds':['collect','1','item'],
		'exec':self.startCollectItemMode,
		'desc':'use to collect item data rapidly'
		},
		'2':{
		'cmds':['list','2','+/-','cnt','count'],
		'exec':self.startListMode,
		'desc':"use as a list maker",
		},
		'3':{
		'cmds':['quit','q','3','e'],
		'exec':lambda self=self:exit("User Quit!"),
		'desc':"exit program"
		},
		}
		self.modeString=''.join([f"{Fore.cyan}{self.modes[i]['cmds']} - {self.modes[i]['desc']}{Style.reset}\n" for i in self.modes])
		while True:
			self.currentMode=input(f"which mode do you want to use \n{self.modeString}: ").lower()
			for k in self.modes:
				if self.currentMode in self.modes[k]['cmds']:
					self.modes[k]['exec']()

	def Unified(self,line):
		try:
			return self.unified(line)
		except Exception as e:
			print(e)
			return False


	def unified(self,line):
		args=line.split(",")
		#print(args)
		if len(args) > 1:
			if args[0] == "#remove":
				try:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).delete()
						print(result)
						session.commit()
						session.flush()
				except Exeption as e:
					print(e)
				return True
			elif args[0] == '#name':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Name)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")	
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Name',str(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Name)
				return True
			elif args[0] == '#code':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Code)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Code',str(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Code)
				return True
			elif args[0] == '#barcode':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Barcode)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Barcode',str(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Barcode)
				return True
			elif args[0] == '#note':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Note)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Note',str(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Note)
				return True
			elif args[0] == '#price':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Price)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Price',float(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Price)
				return True
			elif args[0] == '#shelf':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Shelf)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Shelf',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Shelf)
				return True
			elif args[0] == '#backroom':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.BackRoom)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'BackRoom',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.BackRoom)		
				return True
			elif args[0] == '#inlist':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'InList',bool(int(args[2])))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.InList)		
				return True
			elif args[0] == '#display_1':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_1)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_1',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_1)		
				return True
			elif args[0] == '#display_2':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_2)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_2',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_2)		
				return True
			elif args[0] == '#display_3':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_3)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_3',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_3)	
				return True
			elif args[0] == '#display_4':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_4)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_4',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_4)		
				return True
			elif args[0] == '#display_5':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_5)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_5',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_5)		
				return True
			elif args[0] == '#display_6':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.Display_6)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'Display_6',int(args[2]))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.Display_6)			
				return True
			elif args[0] == '#inlist':
				if len(args) == 2:
					with Session(self.engine) as session:
							result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
							if result:
								print(result.InList)
							else:
								print(f"{Fore.yellow}{Style.blink}{Style.bold}Nothing by that EntryId{Style.reset}")
				else:
					with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
						setattr(result,'InList',bool(int(args[2])))
						session.commit()
						session.flush()
						session.refresh(result)
						print(result.InList)	
				return True
			elif args[0] == "#stock_total":
				with Session(self.engine) as session:
					item=session.query(Entry).filter(Entry.EntryId==int(args[1])).first()
					keys=[f'Display_{i}' for i in range(1,7)]
					keys.append('Shelf')
					keys.append('BackRoom')
					print(keys)
					t=0
					for k in keys:
						curr=getattr(item,k)
						if curr:
							t+=curr
						else:
							setattr(item,k,0)
					setattr(item,'Stock_Total',t)
					session.commit()
					session.flush()
					session.refresh(item)
					print(item.Stock_Total)
				return True	
			elif args[0] == "#show":
				with Session(self.engine) as session:
						result=session.query(Entry).filter(Entry.EntryId==int(args[1])).all()
						for num,e in enumerate(result):
							print(num,e)
				return True
		elif args[0] == "#list_all":
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).all()
					for num,e in enumerate(result):
						print(num,e)
			print("-"*10)
			return True
		elif args[0] == "#show_list":
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).filter(Entry.InList==True).all()
					for num,e in enumerate(result):
						print(num,e)
			print("-"*10)
			return True
		elif args[0] == "#clear_list":
			print("-"*10)
			with Session(self.engine) as session:
					result=session.query(Entry).filter(Entry.InList==True).update({'InList':False})
					session.commit()
					session.flush()
					print(result)
			print("-"*10)
			return True
		elif args[0] == "#save_csv":
			df=pd.read_sql_table('Entry',self.engine)
			while True:
				try:
					sfile=input("{Style.bold}Save Where:{Style.reset} ")
					if sfile == "":
						sfile="./db.csv"
						print(f'{Fore.orange_3}{Path(sfile).absolute()}{Style.reset}')
					if sfile.lower() == 'q':
						exit("user quit!")
					elif sfile.lower() == 'b':
						break
					else:
						df.to_csv(sfile,index=False)
					break
				except Exception as e:
					print(e)
					
			return True
		return False

	def startCollectItemMode(self):
		code=''
		barcode=''
		options=['q - quit - 1','2 - b - back','#skip','#?','#tlm','#slm']
		while True:
			other_cmds=False
			while True:
				fail=False
				upce=''
				barcode=input(f"{Fore.green_yellow}Barcode{Style.reset}{options}{Style.bold}\n: ")
				print(f"{Style.reset}")
				if barcode.lower() in ['q','quit','1']:
					exit('user quit!')
				elif barcode in ['2','b','back']:
					return
				elif barcode.lower() in ['#skip',]:
					barcode='1'*11
					break
				elif barcode.lower() in ['#?']:
					self.help()
					break
				elif self.Unified(barcode):
					other_cmds=True
				elif barcode == '':
					barcode='0'*11
					break
				elif barcode.lower() == '#tlm':
					self.listMode=not self.listMode
					print(f"ListMode is now: {Fore.red}{self.listMode}{Style.reset}")
					break
				elif barcode == '#slm':
					print(f"ListMode is: {Fore.red}{self.listMode}{Style.reset}")
					break
				else:	
					if len(barcode) == 8:
						try:
							upce=upcean.convert.convert_barcode(intype="upce",outtype="upca",upc=barcode)
						except Exception as e:
							print(e)				
					for num,test in enumerate([UPCA,EAN8,EAN13]):
						try:
							if test == UPCA:
								if len(barcode) >= 11:
									t=test(barcode)	
								elif len(barcode) == 8:
									t=test(upce)
							else:
								t=test(barcode)
							print(t)
							break
						except Exception as e:
							print(e)
							if num >= 3:
								fail=True
				#print("break",fail)
				if fail:
					barcode='0'*11
					break
				else:
					break

			while True:
				fail=False
				code=input(f"{Style.reset}{Fore.green}Code{Style.reset}{options}{Style.bold}\n: ")
				print(f"{Style.reset}")
				if code.lower() in ['q','quit','1']:
					exit('user quit!')
				elif code in ['2','b','back']:
					return
				elif code.lower() in ['#skip',]:
					code='1'*8
					break
				elif code.lower() in ['#?']:
					self.help()
					break
				elif self.Unified(code):
					other_cmds=True
				elif code == '':
					code='0'*8
					break
				elif code == '#tlm':
					self.listMode=not self.listMode
					print(f"ListMode is now: {Fore.red}{self.listMode}{Style.reset}")
					break
				elif code == '#slm':
					print(f"ListMode is: {Fore.red}{self.listMode}{Style.reset}")
					break
				else:
					fail=False
					for num,test in enumerate([Code39,]):
						try:
							t=test(code,add_checksum=False)
							break
						except Exception as e:
							print(e)
							if num >= 1:
								fail=True
					if fail:
						code='0'*8
						break
					else:
						break
			if not other_cmds:
				with Session(self.engine) as session:
					if len(barcode) == 8:
						query=session.query(self.tables['Entry']).filter(or_(self.tables['Entry'].Barcode.icontains(upce),self.tables['Entry'].Code.icontains(code)))
					else:
						query=session.query(self.tables['Entry']).filter(or_(self.tables['Entry'].Barcode.icontains(barcode),self.tables['Entry'].Code.icontains(code)))
					results=query.all()
					if len(results) < 1:
						print(code)
						print(barcode)
						if (code != '0'*8 and barcode != '0'*11):
							if upce != '':
								entry=self.tables['Entry'](Barcode=upce,Code=code,upce2upca=barcode)
							else:
								entry=self.tables['Entry'](Barcode=barcode,Code=code)
							session.add(entry)
							session.commit()
							session.flush()
							session.refresh(entry)
							print(entry)
					else:
						for num,e in enumerate(results):
							print(f"{Fore.light_red}{num}{Style.reset}->{e}")
						while True:
							msg=input(f"Do you want to edit one? if so enter its {Fore.light_red}entry number{Style.reset}(or {Fore.yellow}-1{Style.reset} to {Fore.yellow}quit{Style.reset},{Fore.cyan}-2{Style.reset} to {Fore.cyan}go back{Style.reset}{Fore.green}[or Hit <Enter>]{Style.reset}): ")
							try:								
								if msg == '':
									if self.listMode and len(results) >=1:
										qty=input("How Much to add? ")
										if qty == '':
											qty=1
										qty=float(qty)
										setattr(results[0],'InList',True)
										setattr(results[0],'ListQty',getattr(results[0],'ListQty')+qty)
										session.commit()
										session.flush()
										session.refresh(results[0])
									break
								num=int(msg)
								if num == -1:
									exit("user quit!")
								elif num == -2:
									break
								else:
									if self.listMode:
										while True:
											qty=input("How Much to add? ")
											if qty == '':
												qty=1
											qty=float(qty)
											setattr(results[num],'InList',True)
											setattr(results[num],'ListQty',getattr(results[num],'ListQty')+qty)
											session.commit()
											session.flush()
											session.refresh(results[num])
											break
									else:
										print(results[num])
										self.editEntry(session,results[num])
									break
							except Exception as e:
								print(e)
							#use first result as found as entry and display it while incrementing it
							

	listMode=False
	def editEntry(self,session,item):
		print(session,item)
		for column in item.__table__.columns:
			while True:
				try:
					if column.name not in ['Timestamp','EntryId']:
						new_value=input(f"{column.name}->{getattr(item,column.name)}('n','s','d','q'): ")
						if new_value in ['s','n']:
							break
						elif new_value in ['d']:
							session.query(self.tables['Entry']).filter(self.tables['Entry'].EntryId==item.EntryId).delete()
							print(item,"Was Deleted!")
							return
						elif new_value in ['b']:
							return	
						elif new_value in ['q']:
							exit("user quit!")

						if isinstance(column.type,Float):
							new_value=float(new_value)
						elif isinstance(column.type,Integer):
							new_value=int(new_value)
						elif str(column.type) == "VARCHAR":
							pass
						elif isinstance(column.type,Boolean):
							if new_value.lower() in ['true','yes','1','y',]:
								setattr(item,column.name,1)
							else:
								setattr(item,column.name,0)
						if str(column.type) not in ['BOOLEAN',]:
							#exit(str((column.name,column.type,isinstance(column.type,Boolean))))
							setattr(item,column.name,new_value)
						session.commit()
					break
				except Exception as e:
					print(e)




	def startListMode(self):
		print(f"{Fore.yellow}List Mode{Style.reset}")
		self.listMode=True
		self.startCollectItemMode()

	def help(self):
		msg="""
#desired tools
	#add barcode,code with EntryId 
	#-- code and barcode are tested before insertion to ensure they are correct
	#-- force a while true if code or barcode is found in table prior to insertion
	#--- to ensure valid data is stored
	#if item is found by either item code or barcode, a prompt to edit current data is displayed
	#collect mode searchs db for items and adds them automatically by code and barcode if no match is found
	
	'commands are prefixed with '#'
	#list all barcodes/codes
	#if code/barcode is in db already print to screen and increment qty field
	#remove,{EntryId} -> removes barcode by EntryId
	

	
	#list mode options:
		#edit_start
		#edit_stop

	#save_csv -- save db to csv file
	q - quit 
	#factor_reset -- clear db of all items and startstop of Entry
	#reset-ss -- reset start/stop
	#set-ss -- prompt for start stop (will reset start and stop times by prompt) 
	#search {fieldname}
		#prompts for data to search by in {fieldname}
		#searches Entry for "like %{fieldname}%" and displays them with their EntryID
	#help,#? -- displays info found here, or help page
	
	[FUTURE-ENDEAVOR]
	#locater {code}
		#a prompt then shows where the user then inputs/scans barcodes until the entry for the 
		#first code is scanned again, either by the first product, or a shelf label containing 
		#the upc or the item_code for the item
		#if multiple Entry
			#display Entry and leave locator mode
		#if single entry is found dislay in bright bold text and leave locator mode

		#if scanned code does not match the first entry, then display nothing and wait for next scan

	#on start prompt for list mode or item mode
		#item mode use as is

		#list mode will:
		#--iterate through Entry
		# set to zero
		#  display_x/stock_total/backroom/shelf
		#  listitem will be set to false
		#entry prompt for codes/barcodes shows
		#each scan will check and set to to true listitem
		#when '#summary' is entered all items in with listitem=True will be displayed

	#not found in prompt requested by
	'''
	#field,{Entryid} -- views Entryid field
	#field,{Entryid},{new_value} -- sets Entryid field
	
	#list mode ONLY
		###only for scanned barcodes/codes as scanned base inventory###
		if +/-{num} at barcode/code input use as qty value:
			set qty to qty+({+/-num})
		else:
		#Qty {Entryid}
		#Qty {Entryid} {new_value}
		{barcode}/{code} adds 1 to found entry

	#stock_total {Entryid} -- calculates from above Entry and updates value automatically

	'''"""
		print(msg)
		return msg

def quikRn():
	Main(engine=ENGINE,tables=tables,error_log=Path("error_log.log"))

if __name__ == "__main__":
	Main(engine=ENGINE,tables=tables,error_log=Path("error_log.log"))