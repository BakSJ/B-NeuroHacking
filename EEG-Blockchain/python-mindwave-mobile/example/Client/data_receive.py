import time
from web3 import Web3, HTTPProvider
import contract_abi
from web3.contract import ConciseContract
import json
import hashlib
import socket
# python3 version
# client File Request 
 
HOST = 'localhost'
PORT = 9009
 
def getFileFromServer(filename):
	data_transferred = 0
 
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST,PORT))
		sock.sendall(filename.encode())
 
		data = sock.recv(1024)
		if not data:
			print('File [%s]: Does not exist' %filename)
			return
 
		with open('./' + filename, 'wb') as f:
			try:
				while  data:
					f.write(data)
					data_transferred += len(data)
					data = sock.recv(1024)
			except Exception as e:
				print(e)
 
	# Python program to find SHA256 hash string of a file
	sha256_hash = hashlib.sha256()
	with open(filename,"rb") as f:
		# Read and update hash string value in blocks of 4K
		for byte_block in iter(lambda: f.read(4096),b""):
			sha256_hash.update(byte_block)
		fh = sha256_hash.hexdigest()
		print(sha256_hash.hexdigest())


	contract_address     = '0xf4e6E1D76D994fA9c5ABaE3F3a92C06A38f1dAf6'
	wallet_private_key   = '0x008af62e81d8d081fcacf5047e8d8572bf7d9c41cf798a2453cf92d56aecbf56'
	wallet_address       = '0xceC78B6F85f9214E01B0AAce35faC1C506ad578e'

	w3 = Web3(HTTPProvider('https://ropsten.infura.io/W5xtVeuTIZaaXlTWtalj'))
	print("w3 Connected: ",w3.isConnected()) #connect test True or False
	w3.eth.enable_unaudited_features() 
	print(w3.eth.blockNumber)  #test: blocknumber of mined block
	with open('factory.json', 'r') as abi_definition:
		abi = json.load(abi_definition)   #abi file open, stored -> abi

	nonce = w3.eth.getTransactionCount(wallet_address) # test:account nonce return
	print("nonce  ",nonce)
	print(abi)
	fContract = w3.eth.contract(address=contract_address, abi=abi) #contract connect

	b =w3.eth.getBalance(wallet_address)  # test: account balace retrun
	print(b)
	txn = fContract.functions.set(fh).buildTransaction({'chainId':3,'gas': 4665270,'gasPrice':w3.toWei('1','gwei'),'nonce':nonce})
	#create transaction,set(n),n = hash, chainid = 3(ropsten)
	signed_txn = w3.eth.account.signTransaction(txn,private_key=wallet_private_key)
	#sign using my account private key
	print('signed_txn.hash',signed_txn.hash) # test: return signed transaction
	rw = signed_txn.rawTransaction # infura(provide api key), must make raw transaction
	print(rw) #test: return raw transaction

	#w3.eth.sendRawTransaction(rw) 
	#broadcasting raw Transaction

	t = fContract.functions.get().call() # get function, return hash
	print(t) #test: return get()
	print(type(t)) #test: return get() type

	if t == fh:
		print("file is good :)")
	else:
		print("Warning: file has been changed!!!!!")



	print('File [%s] Finished. Transfer Byte [%d]' %(filename, data_transferred))
 
filename = input('File name :')
getFileFromServer(filename)


