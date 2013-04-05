from HTMLParser import HTMLParser
from CityListParser import CityListParser
from PageCounter import PageCounter
from urllib2 import urlopen

from unicodedata import normalize

import os
import sys
# eliminar modulo csv
import csv

class TParser(HTMLParser, object):

    '''

    essa classe tah com mais resposabilidades do que deveria

    '''

    
    def __init__(self, year):
        HTMLParser.__init__(self)
        self.year = year

        if os.path.exists('file.csv'):
            csv_file = open('file.csv', 'ab')
            self.csv_writer = csv.writer(csv_file, delimiter=',')
        else:
            csv_file = open('file.csv', 'ab')
            self.csv_writer = csv.writer(csv_file, delimiter=',')
            self.csv_writer.writerow(['Funcao', 'Acao Governamental', 'Linguagem Cidada', 'Total no Ano(R$)', 'Ano'])

        self.parsing_td = False
        self.parsing_listagem = False

        self.temp_content = ''
        self.content_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.parsing_td = True

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == 'listagem':
                    self.parsing_listagem = True


    def handle_data(self, data):

        if self.parsing_listagem and self.parsing_td:
            data = data.replace('\n','').replace('\r','').replace('\t','').rstrip(' ').lstrip(' ')
            # precisa dessa checagem?
            if len(data) != 0:
                self.temp_content += data


    def handle_endtag(self, tag):

        if tag == 'td':
            self.parsing_td = False

        if self.parsing_listagem and tag == 'td':
            # precisa mesmo dessa checagem?
            if len(self.temp_content) > 0:
                self.content_list.append(normalize('NFKD',self.temp_content).encode('ascii','ignore'))
            else:
                self.content_list.append('')

            self.temp_content = ''

        if tag == 'table':
            if self.parsing_listagem:
                self.parsing_listagem = False
        if self.parsing_listagem and tag == 'tr' and len(self.content_list) > 0:
            self.content_list.append(self.year)
            self.csv_writer.writerow(self.content_list)
            self.content_list = []


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'passe o argumento, meu filho'
    else:
        uf = sys.argv[1].upper()
        ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
        if uf not in ufs:
            print 'uf invalido. os validos sao os seguintes:', ufs
        else:
            if len(sys.argv) > 2:

                try:
                    cod_mun = int(sys.argv[2])
                except ValueError as value_error:
                    print "codigo de cidade invalido. tente 'python main.py <UF>' para listar os nomes e respectivos codigos das cidades do seu estado."
                    print "para baixar dados de uma cidade, use: 'main.py <UF> <codigo da cidade>'"

                years = range(2004, 2013)

                url_template = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaAcoes.asp?Exercicio=%d&SelecaoUF=1&SiglaUF=PB&CodMun=%d&Pagina=%d'

                for year in years:
                    counter = PageCounter()
                    url = url_template % (year, cod_mun, 1)

                    data = urlopen(url).read()
                    data = unicode(data, 'iso-8859-1')
                    counter.feed(data)

                    page_count = counter.get_page_count()

                    for page in range(1, page_count + 1):
                        print 'parsing year %d, page %d' % (year, page)

                        url = url_template % (year, cod_mun, page)
                        data = urlopen(url).read()
                        data = unicode(data, 'iso-8859-1')

                        parser = TParser(year)
                        parser.feed(data)

            else:
                url = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaCidades.asp?Exercicio=2004&SelecaoUF=1&SiglaUF=%s' % uf

                counter = PageCounter()
                data = urlopen(url).read()
                data = unicode(data, 'iso-8859-1')
                counter.feed(data)

                page_count = counter.get_page_count()

                for page in range(1, page_count + 1):
                    url_template = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaCidades.asp?Exercicio=2004&SelecaoUF=1&SiglaUF=%s&Pagina=%d'

                    parser = CityListParser()
                    data = urlopen(url_template % (uf, page)).read()
                    data = unicode(data, 'iso-8859-1')
                    parser.feed(data)

                    for city in parser.get_city_list():
                        print city[0], '-', city[1]
    