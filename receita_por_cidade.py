from HTMLParser import HTMLParser
from PageCounter import PageCounter
from urllib2 import urlopen

from unicodedata import normalize

import os
# eliminar modulo csv
import csv

class TParser(HTMLParser, object):

    
    def __init__(self):
        HTMLParser.__init__(self)

        # fazer bonitinho. pra nao deixar essa referencia ao arquivo perdida no limbo
        self.csv_writer = csv.writer(open('file.csv', 'ab'), delimiter=',')

        self.parsing_td = False
        self.parsing_th = False
        self.parsing_listagem = False

        self.temp_content = ''
        self.content_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.parsing_td = True

        if tag == 'th':
            self.parsing_th = True

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == 'listagem':
                    self.parsing_listagem = True

    def handle_data(self, data):

        if self.parsing_listagem and (self.parsing_td or self.parsing_th):
            data = data.replace('\n','').replace('\r','').replace('\t','').rstrip(' ').lstrip(' ')
            # precisa dessa checagem?
            if len(data) != 0:
                self.temp_content += data

    def handle_endtag(self, tag):
        if tag in ['td', 'th']:
            # precisa mesmo dessa checagem?
            if len(self.temp_content) > 0:
                self.content_list.append(normalize('NFKD',self.temp_content).encode('ascii','ignore'))

            if tag == 'td':
                self.parsing_td = False
            elif tag == 'th':
                self.parsing_th = False

            self.temp_content = ''

        if tag == 'table':
            if self.parsing_listagem:
                self.parsing_listagem = False
        if self.parsing_listagem and tag == 'tr':
            print 'writing row'
            self.csv_writer.writerow(self.content_list)
            self.content_list = []


if __name__ == '__main__':

    # tratar entrada de estado e municipio

    years = range(2004, 2013)

    cod_mun = 2235

    url_template = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaAcoes.asp?Exercicio=%d&SelecaoUF=1&SiglaUF=PB&CodMun=%d&Pagina=%d'

    for year in years:
        counter = PageCounter()
        url = url_template % (year, cod_mun, 1)

        # continuar daqui

        print 'counting pages from year %d' % year
        print url
        data = urlopen(url).read()
        data = unicode(data, 'iso-8859-1')
        counter.feed(data)

        page_count = counter.get_page_count()

        for page in range(1, page_count + 1):
            print 'parsing year %d, page %d' % (year, page)

            url = url_template % (year, cod_mun, page)
            data = urlopen(url).read()
            data = unicode(data, 'iso-8859-1')

            parser = TParser()
            parser.feed(data)
    
    
    # if os.path.exists('page.html'):
    #     f = open('page.html')
    #     data = f.read()
    #     f.close()
    # else:
    #     try:
    #         print 'file not found. downloading it.'
    #         data = urlopen(url).read()
    #         f = open('page.html','w')
    #         f.write(data)
    #         f.close()
    #     except Exception:
    #         print 'deu pau, viu?'















