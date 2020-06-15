import asyncio,io,re,socket,traceback,urllib.parse
defaultMsg={400:'Bad Request',401:'Unauthorized',402:'Payment Required',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',406:'Not Acceptable',407:'Proxy Authentication Required',408:'Request Timeout',409:'Conflict',410:'Gone',411:'Length Required',412:'Precondition Failed',413:'Payload Too Large',414:'URI Too Long',415:'Unsupported Media Type',416:'Range Not Satisfiable',417:'Expectation Failed',421:'Misdirected Request',422:'Unprocessable Entity',423:'Locked',424:'Failed Dependency',425:'Too Early',426:'Upgrade Required',428:'Precondition Required',429:'Too Many Requests',431:'Request Header Fields Too Large',451:'Unavailable For Legal Reasons',500:'Internal Server Error',501:'Not Implemented',502:'Bad Gateway',503:'Service Unavailable',504:'Gateway Timeout',505:'HTTP Version Not Supported',506:'Variant Also Negotiates',507:'Insufficient Storage',508:'Loop Detected',510:'Not Extended',511:'Network Authentication Required'}
mediaTypes={'plain':'text/plain;charset=utf-8','html':'text/html;charset=utf-8','css':'text/css','js':'application/javascript','jpeg':'image/jpeg','png':'image/png','svg':'image/svg+xml','bin':'application/octet-stream','woff2':'font/woff2','ttf':'font/ttf','zip':'application/zip'}
class Request(object):
	__slots__=('version', 'method', 'path', 'query', 'match', 'headers', 'body')
class Response(object):
	__slots__=('code', 'headers', 'type', 'body')
	def __init__(self, code=200, body=b'', type='text/plain', headers={}):
		self.code = code
		self.body = body or defaultMsg[code]
		self.type = type
		self.headers = headers
class HTTPServer:
	def __call__(self, path, method='GET'):
		def decorator(func):
			if path not in self.routes:
				self.routes[path] = {}
			assert method not in self.routes[path]
			self.routes[path][method] = func
			return func
		return decorator
	def __init__(self, statics={}):
		self.routes = {path: {'GET': file} for path, file in statics.items()}
	def run(self, addr, port, ctx=None):
		async def serve(ctx):
			self.server = await asyncio.start_server(self.process, addr, port, ssl=ctx)
			async with self.server:
				await self.server.serve_forever()
		try:
			asyncio.run(serve(ctx))
		except KeyboardInterrupt:
			self.server.close()
			asyncio.run(self.server.wait_closed())
	async def process(self, reader, writer):
		peer = writer.get_extra_info('peername')
		print('+{}:{}'.format(*peer))
		while True:
			try:
				code = await self.parse(reader, req:=Request())
			except asyncio.IncompleteReadError:
				print(' {}:{}'.format(*peer))
				break
			if code:
				await self.reply(writer, Response(code, headers={'connection': 'close'}))
				break
			rsp = await self.dispatch(req)
			await self.reply(writer, rsp, withBody=req.method!='HEAD')
		writer.close()
	async def parse(self, reader, req):
		async def getline():
			line = await reader.readuntil()
			return line[:-2] if line[-2]==13 else line[:-1]
		try:
			requestLine = await getline()
		except asyncio.LimitOverrunError:
			return 400
		try:
			method, target, version = requestLine.split(b' ', 2)
			req.method = method.decode('ascii')
			if b'?' in target:
				req.path, querystr = target.decode('ascii').split('?', 1)
				req.query = urllib.parse.parse_qs(querystr, True, True) if querystr else {}
			else:
				req.path = target.decode('ascii')
				req.query = {}
			req.version = tuple(int(x) for x in re.fullmatch(br'HTTP/(\d).(\d)',version).groups())
			if req.version[0] != 1:
				return 505
		except:
			return 400
		req.headers = headers = {}
		while True:
			try:
				field = await getline()
			except asyncio.LimitOverrunError:
				return 431
			if not field:
				break
			try:
				name, value = field.split(b':', 1)
				name = name.lower().decode('ascii')
				value = value.strip(b' \t').decode('ascii')
			except:
				return 400
			if name in headers:
				headers[name] += ',' + value
			else:
				headers[name] = value
		if 'transfer-encoding' in headers:
			return 400
		elif 'content-length' in headers:
			try:
				bodySize = int(headers['content-length'])
			except:
				return 411
			req.body = await reader.readexactly(bodySize)
	async def dispatch(self, req):
		for n, v in self.routes.items():
			if m := re.fullmatch(n, req. path):
				action = v
				break
		else:
			return Response(404)
		try:
			action = action['GET' if req.method=='HEAD' else req.method]
		except KeyError:
			return Response(405)
		if isinstance(action, tuple):
			with open(action[0], 'rb') as file:
				return Response(body=file.read(), type=action[1])
		else:
			req.match = m.groups()
			try:
				return action(req)
			except:
				traceback.print_exc()
				return Response(500)
	async def reply(self, writer, rsp, withBody=True):
		headers = rsp.headers
		body = rsp.body
		if isinstance(body, (io.StringIO, io.BytesIO)):
			body = body.getvalue()
			rsp.body.close()
		if isinstance(body, str):
			body = body.encode()
		if len(body):
			headers['content-type'] = rsp.type
		headers['content-length'] = len(body)
		writer.write(f'HTTP/1.1 {rsp.code} \r\n'.encode('ascii'))
		for name, value in headers.items():
			writer.write(f"{name}:{value}\r\n".encode())
		writer.write(b'\r\n')
		if withBody:
			writer.write(body)