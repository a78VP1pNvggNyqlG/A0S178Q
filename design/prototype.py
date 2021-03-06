import aserv, jinja2, json, random, sys, ssl, http.cookies
from aserv import Response

statics = \
{
	'/style': ('style.css', 'text/css'),
	'/data.json': ('data.json', 'application/json'),
	'/showcases/1': ('4.jpeg', 'image/jpeg'),
	'/showcases/2': ('7.jpg', 'image/jpeg'),
	'/showcases/3': ('8.jpg', 'image/jpeg'),
	'/icons/like': ('like.svg', 'image/svg+xml'),
	'/icons/diff': ('diff.svg', 'image/svg+xml'),
	'/icons/cart': ('cart.svg', 'image/svg+xml'),
	'/icons/user': ('user.svg', 'image/svg+xml'),
	'/icons/search': ('search.svg', 'image/svg+xml'),
	'/scripts/selector': ('selector.js', 'application/javascript'),
	'/terms': ('terms.txt', 'text/plain;charset=utf-8'),
}

server = aserv.HTTPServer(statics)
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), autoescape=True)
with open('data.json') as f:
	data = json.load(f)

lookup = {item['id']: item for item in data['items']}

def randitems(n):
	return random.sample(data['items'], min(n, len(data['items'])))

def ask(req):
	cookies = http.cookies.SimpleCookie(req.headers.get('cookie', ''))
	return 'consent' not in cookies

@server('/')
def handle(req):
	template = env.get_template('index.html')
	html = template.render(asking=ask(req), brand=data['brand'], categories=data['nav'], recommendation=randitems(9))
	return Response(body=html, type='text/html;charset=utf-8')

@server('/category')
def handle(req):
	template = env.get_template('category.html')
	html = template.render(asking=ask(req), brand=data['brand'], categories=data['nav'], items=data['items'], cat='所有商品')
	return Response(body=html, type='text/html;charset=utf-8')

@server('/items/(\d+)')
def handle(req):
	template = env.get_template('item.html')
	id = req.match[0]
	try:
		item = lookup[id]
	except KeyError:
		return Response(404)
	html = template.render(asking=ask(req), brand=data['brand'], item=item, categories=data['nav'], recommendation=randitems(6))
	return Response(body=html, type='text/html;charset=utf-8')

@server('/images/(\d+)')
def handle(req):
	img = req.match[0]
	try:
		with open(f'pics/pic{img}.jpg', 'rb') as f:
			blob = f.read()
	except FileNotFoundError:
		return Response(404)
	return Response(body=blob, type='image/jpeg')

@server('/search')
def handle(req):
	q = req.query.get('q', [''])
	if len(q) != 1:
		return Response(400)
	q = q[0]
	result = tuple(item for item in data['items'] if item['name'].find(q) != -1)
	template = env.get_template('category.html')
	html = template.render(asking=ask(req), brand=data['brand'], categories=data['nav'], items=result, cat=q, searched=q)
	return Response(body=html, type='text/html;charset=utf-8')

@server('/consent', 'POST')
def handle(req):
	location = req.headers.get('referer', '/')
	return Response(303, body='已同意用户协议。', headers={'set-cookie': 'consent=;path=/;httpOnly', 'location': location})

if __name__ == '__main__':
	if sys.argv[1:] == ('p',):
		server.run('', 80)
	else:
		sslCtx=ssl.SSLContext()
		sslCtx.load_cert_chain('pub.pem','pvk.pem')
		server.run('', 443, sslCtx)