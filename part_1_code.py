import urllib.request

hamlet_url = 'https://www.gutenberg.org/files/2265/2265.txt'
response = urllib.request.urlopen(hamlet_url)
data = response.read() 
text = data.decode('utf-8')
print(text)

macbeth_url = 'https://www.gutenberg.org/files/2264/2264.txt'
response = urllib.request.urlopen(macbeth_url)
data = response.read()  
text = data.decode('utf-8')
print(text) 

