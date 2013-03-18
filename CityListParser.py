from HTMLParser import HTMLParser
from unicodedata import normalize
from urllib2 import urlopen
import os
import sys

from PageCounter import PageCounter

class CityListParser(HTMLParser, object):

    
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.parsing_listagem = False
        self.parsing_first_child = False
        self.parsing_a = False

        self.temp_content = ''
        self.content_list = []

        # o codigo da cidade nao pode ser um int pra nao causar erros na hora de formar as urls.
        self.city_code = ''
        self.city_name = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == 'listagem':
                    self.parsing_listagem = True

        if self.parsing_listagem and tag == 'td':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'firstChild':
                    self.parsing_first_child = True

        if self.parsing_first_child and tag == 'a':
            self.parsing_a = True
            for attr in attrs:
                if attr[0] == 'href':
                    cut = attr[1][attr[1].find('CodMun=')+ 7:]
                    # o codigo da cidade nao pode ser um int pra nao causar erros na hora de formar as urls.
                    self.city_code = cut[:cut.find('&')]


    def handle_data(self, data):
      
        if self.parsing_a:
            data = data.replace('\n','').replace('\r','').replace('\t','').rstrip(' ').lstrip(' ')
            # precisa dessa checagem?
            if len(data) != 0:
                self.temp_content += data


    def handle_endtag(self, tag):
        
        if self.parsing_a and tag == 'a':
            self.parsing_a = False
            self.city_name = self.temp_content
            self.temp_content = ''

        if self.parsing_first_child and tag == 'td' and not self.parsing_a:
            print self.city_code, '-', self.city_name
            self.parsing_first_child = False

            # TODO: decidir o que fazer com os dados retirados com o parser. mandar pra banco? apenar armazernar no objeto e criar metodos pra recuperar?

            # essa lista pode ou nao ser mais necessaria
            self.content_list = []


        if self.parsing_first_child and tag == 'td':
            # precisa mesmo dessa checagem?
            if len(self.temp_content) > 0:
                self.content_list.append(normalize('NFKD',self.temp_content).encode('ascii','ignore'))
            else:
                self.content_list.append('')

            self.parsing_first_child = False

        if tag == 'table':
            if self.parsing_listagem:
                self.parsing_listagem = False
                print self.content_list

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print 'passe o argumento, meu filho'
    else:
        uf = sys.argv[1]
        ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
        if uf not in ufs:
            print 'uf invalido'
            print 'os validos sao esses aqui:', ufs
        else:
            url = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaCidades.asp?Exercicio=2004&SelecaoUF=1&SiglaUF=%s' % uf

            counter = PageCounter()
            data = urlopen(url).read()
            data = unicode(data, 'iso-8859-1')
            counter.feed(data)

            page_count = counter.get_page_count()

            # remover para poder coletar todas as paginas
            #for page in range(1, page_count + 1):
            for page in range(1, 3):
                url_template = 'http://www.portaltransparencia.gov.br/PortalTransparenciaListaCidades.asp?Exercicio=2004&SelecaoUF=1&SiglaUF=PE&Pagina=%d'

                parser = CityListParser()
                data = urlopen(url_template % page).read()
                data = unicode(data, 'iso-8859-1')
                parser.feed(data)






















