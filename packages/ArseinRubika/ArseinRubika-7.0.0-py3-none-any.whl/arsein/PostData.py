import aiohttp
import asyncio
from arsein.Encoder import encoderjson
from arsein.GtM import default_api
from json import dumps, loads,JSONDecodeError
from random import choice,randint
from arsein.Clien import clien
from arsein.Device import DeviceTelephone
import base64 
from base64 import b64decode
from arsein.Error import ErrorPrivatyKey,ErrorServer


async def http(plat:str,js:dict,OrginalAuth:str,auth:str,key:str):
	Full = default_api()
	s = Full.defaultapi()
	enc,Enc = encoderjson(auth,key),encoderjson(OrginalAuth,key)
	if plat == 'web':
		async with aiohttp.ClientSession() as session:
			async with session.post(s, data = dumps({"api_version":"6","auth": OrginalAuth,"data_enc":enc.encrypt(dumps(js)),"sign": enc.makeSignFromData(enc.encrypt(dumps(js)))}),headers = {"Origin": "https://web.rubika.ir","Referer": f"https://web.rubika.ir/","Host":s.replace("https://","").replace("/",""),"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}) as response:
				Post =  await response.text()
				return Post

	elif plat == 'android':
		async with aiohttp.ClientSession() as session:
			async with session.post(s, data = dumps({"api_version":"6","auth": auth,"data_enc":Enc.encrypt(dumps(js)),"sign": Enc.makeSignFromData(Enc.encrypt(dumps(js)))})) as response:
				Post =  await response.text()
				return Post


async def httpfiles(serversfile:str,dade,head:dict):
	async with aiohttp.ClientSession() as session:
		async with session.post(serversfile, data = dade  , headers = head) as response:
			Post =  await response.text()
			return Post


class method_Rubika:
	def __init__(self,plat:str,OrginalAuth:str,auth:str,keyAccount:str):
		self.Plat = plat
		self.Auth = auth
		self.OrginalAuth = OrginalAuth
		self.keyAccount = keyAccount
		self.enc = encoderjson(self.Auth , self.keyAccount) if plat == 'web' else encoderjson(self.OrginalAuth , self.keyAccount)

	def methodsRubika(self,types:str = None,methode:str = None,indata:dict = None,wn:dict = None,server = None,podata = None,header:dict = None):
		self.Type = types
		self.inData = {"method":methode,"input":indata,"client":wn}
		self.serverfile = str(server)
		self.datafile = podata
		self.headerfile = header

		while 1:
			try:
				loop = asyncio.get_event_loop()
				# loop.run_until_complete
				for senddata in range(1):
					if self.Type == "json":
						sendJS:dict =  loads(self.enc.decrypt(loads(loop.run_until_complete(http(plat = self.Plat,js = self.inData,OrginalAuth = self.OrginalAuth,auth = self.Auth,key = self.keyAccount))).get("data_enc")))
						return sendJS
					elif self.Type == "file":
						sendFILE =  loop.run_until_complete(httpfiles(serversfile = self.serverfile,dade = self.datafile,head = self.headerfile))
						return sendFILE
				break
			except JSONDecodeError:
				continue
			except aiohttp.client_exceptions.ClientConnectorError:
				continue
			except aiohttp.client_exceptions.InvalidURL:
				continue
			except Exception as err:
				print("Error methodsRubika: ",err)
				break