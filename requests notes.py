import requests
#%% 获取请求
r = requests.get('http://www.baidu.com')
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)

#%%
r = requests.post('http://www.baidu.com', data={'key':'value'})
r = requests.post('http://www.baidu.com', json={'key':'value'})
files = {'file': open('report.xls', 'rb')}
r = requests.post('http://www.baidu.com', files=files)

#%% 请求
r_put = requests.put('https://httpbin.org/put', data = {'key':'value'})
r_delete = requests.delete('https://httpbin.org/delete')
r_head = requests.head('https://httpbin.org/get')
r_options = requests.options('https://httpbin.org/get')

#%% 请求头
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)

#%% response
r = requests.get('https://httpbin.org/put')
print(r.text. r.content, r.json, r.encoding)

from PIL import Image
from io import BytesIO
i = Image.open(BytesIO(r.content))

r = requests.get('https://api.github.com/events', stream=True)
print(r.raw)

with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
'''
An important note about using Response.iter_content versus Response.raw. 
Response.iter_content will automatically decode the gzip and deflate transfer-encodings.
Response.raw is a raw stream of bytes – it does not transform the response content. 
If you really need access to the bytes as they were returned, use Response.raw.
'''

#%% status code
r = requests.get('https://httpbin.org/get')
r.status_code

#%% headers
r = requests.get('https://httpbin.org/get')
r.headers
'''
However, if we want to get the headers we sent the server, 
we simply access the request, and then the request’s headers:'''
r.request.headers

#%% cookies
r = requests.get(url = 'http://example.com/some/cookie/setting/url')
r.cookies['example_cookie_name']

cookies = dict(cookies_are='working')
r = requests.get('https://httpbin.org/cookies', cookies=cookies)
r.text

'''
Cookies are returned in a RequestsCookieJar, which acts like a dict but also offers a more complete interface, 
suitable for use over multiple domains or paths. Cookie jars can also be passed in to requests:
'''
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
r = requests.get('https://httpbin.org/cookies', cookies=jar)
r.text


session.cookies.clear()

#%% You can tell Requests to stop waiting for a response after a given number of seconds with the timeout parameter.
requests.get('https://github.com/', timeout=0.001)

#%% 会话 the session will keep things like cookies when it exists so that you need not to sent again when asking another url
with requests.Session() as s:
    s.get('https://httpbin.org/get')

s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})

# both 'x-test' and 'x-test2' are sent
s.get('https://httpbin.org/headers', headers={'x-test2': 'true'})

#%% Prepared requests
'''
Whenever you receive a Response object from an API call or a Session call, the request attribute is actually the PreparedRequest that was used.
 In some cases you may wish to do some extra work to the body or headers (or anything else really) before sending a request. 
 The simple recipe for this is the following:
'''

from requests import Request, Session

s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = req.prepare()
# do something with prepped.body
prepped.body = 'No, I want exactly this as the body.'
# do something with prepped.headers
del prepped.headers['Content-Type']
resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)
print(resp.status_code)

#and use session:
from requests import Request, Session
s = Session()
req = Request('GET', url)

prepped = s.prepare_request(req)
# Merge environment settings into session
settings = s.merge_environment_settings(prepped.url, {}, None, None, None)
resp = s.send(prepped, **settings)
print(resp.status_code)

#%% certificate
requests.get('https://github.com', verify='/path/to/certfile')
# if ignore, just set verify as false

#%%  proxy
proxyinfo = "http://{}:{}@{}:{}".format('HH87UY3C38GPV1ID', 'F595952EDA67AA58', 'http-dyn.abuyun.com', '9020')
proxy = {
    "http":proxyinfo, 
    "https":proxyinfo
}