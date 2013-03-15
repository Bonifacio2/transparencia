from HTMLParser import HTMLParser
from urllib2 import urlopen
from urllib import urlretrieve

class PageCounter(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.parsing_pagina = False
		self.content = ''

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			for attr in attrs:
				if attr[0] == 'class' and attr[1] == 'paginaAtual':
					self.parsing_pagina = True

	def handle_data(self, data):
		if self.parsing_pagina:
			self.content += data

	def handle_endtag(self, tag):
		if self.parsing_pagina:
			self.parsing_pagina = False

	def get_page_count(self):
		return int(self.content[self.content.rfind('/') + 1:])


if __name__ == '__main__':

	counter = PageCounter()

	url = r'http://www.portaltransparencia.gov.br/PortalTransparenciaListaAcoes.asp?Exercicio=2004&SelecaoUF=1&SiglaUF=PB&CodMun=2235&Pagina='
	data = urlopen(url).read()
	data = unicode(data, 'iso-8859-1')
	counter.feed(data)

	print counter.get_page_count()

