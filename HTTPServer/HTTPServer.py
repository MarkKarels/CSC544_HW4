import socket

class HTTPServer(object):

	def __init__(self, port=9876, ip_addr="127.0.0.1"):
		self.addr = ip_addr
		self.port = port

	def start(self):
		# Establishes connection and specified IP and PORT
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
		self.server.bind((self.addr, self.port))
		self.server.listen()
		print('Listening on port: ' + str(self.port)) # Prints listening at specified port number
		# While socket is open
		while True:
			conn, addr = self.server.accept()
			print(conn, addr)
			request = conn.recv(65538).decode('utf-8')
			string_list = request.split(' ')   # Split request from spaces
		
			method = string_list[0]
			requesting_file = string_list[1]
			filyType = string_list[2]
		
			print('Client Sent Request ',method + " " + filyType + ' 200/OK')
			# Executes if POST method is established
			if method == 'POST':
				try:
					with open(requesting_file+'.txt', 'a+') as self.f:
						for x in range(len(string_list)):
							if x >= 3:
								self.f.write(string_list[x] + ' ')
					self.f.close()

				except FileNotFoundError:
					conn.sendall(b"HTTP/1.0 404 Not Found\r\n\nPage Not Found")
			# Executes if GET method is established
			myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
			myfile = myfile.lstrip('/')
			if(myfile == ''):
				myfile = 'index.html'    # Load index file as default
		
			try:
				file = open(myfile,'rb') # open file , r => read , b => byte format
				response = file.read()
				file.close()
		
				header = 'HTTP/1.1 200 OK\n'
		
				if(myfile.endswith(".jpg")):
					mimetype = 'image/jpg'
				elif(myfile.endswith(".css")):
					mimetype = 'text/css'
				else:
					mimetype = 'text/html'
		
				header += 'Content-Type: '+str(mimetype)+'\n\n'
			# Try Catch for type of connection
			except Exception as e:
				header = 'HTTP/1.1 404 Not Found\n\n'
				response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
			# What is sent back on GET
			final_response = header.encode('utf-8')
			final_response += response
			conn.send(final_response)