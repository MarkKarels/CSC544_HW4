import socket
import requests


class HTTPClient(object):

	def __init__(self, server_ip="127.0.0.1", server_port=9876):

		self.server_ip = server_ip
		self.server_port = server_port


	def server_connect(self):
		if self.server_ip != '127.0.0.1':
			r = requests.get(str(self.server_ip))
			with open('import.html', 'a+') as self.f:
				self.f.write(r.text)
			self.f.close()
		
		else:
			while 1:
				# Tells you what IP connection you have to the server
				print("[" + self.server_ip + "]> ", end='')
				self.request = input()
				self.request_lst = self.request.split()
				self.request_lst[0] = self.request_lst[0].upper() #Takes any GET/POST request case and capitalizes it

				# If Exit is typed, closes connection with server
				if self.request_lst[0] == "EXIT": 
					self.server_socket.close()
					break

				try: # try catch with connection to requested server
					self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.server_socket.connect((self.server_ip, self.server_port))
					self.inout = [self.server_socket]
		
				except ConnectionRefusedError: # throws exeption if connection cannot be made
					print("\n[-] Connection Establishment Error: Could not connect to "+ self.server_ip + ":" + str(self.server_port))
					return

				for i in range(2, len(self.request_lst)): self.request_lst[i] = self.request_lst[i].upper() # Capitalizes request method

				# Executes if GET is method request
				if self.request_lst[0] == "GET":
					if len(self.request_lst) == 2:
						self.request_lst.append("HTTP/1.0")
						
					self.request = " ".join(self.request_lst)
					self.server_socket.send(self.request.encode())
					self.response = self.server_socket.recv(65538)		
					self.response = self.response.splitlines() #Parse the information to get the actual data			
					
					with open(self.request_lst[1], "a+b")as self.f:
						for x in range(len(self.response)):
							if x >= 3:				
								self.f.write(self.response[x] + b'\n')
					self.f.close()
				# Executes if POST is method request
				elif self.request_lst[0] == "POST":
					newMessage = input('Say something to the server: ')
					if len(self.request_lst) == 2:
						self.request_lst.append("HTTP/1.0")
					self.request_lst.append(newMessage)
					self.request = " ".join(self.request_lst)
					self.server_socket.send(self.request.encode())				
				# Executes if any other type of request
				else:
					print("[-] Unsporrted Request!")
		# Closes connection
		print("[-] Connection Closed")
