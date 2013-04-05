from HTMLParser import HTMLParser
from unicodedata import normalize
from urllib2 import urlopen

from PageCounter import PageCounter

class CityListParser(HTMLParser, object):

    
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.parsing_listagem = False
        self.parsing_first_child = False
        self.parsing_a = False

        self.temp_content = ''
        self.city_list = []

        # o codigo da cidade nao pode ser um int pra nao causar erros na hora de formar as urls. culpa do portal
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
                    # o codigo da cidade nao pode ser um int pra nao causar erros na hora de formar as urls. culpa do portal
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
            self.parsing_first_child = False

            if len(self.city_name) > 0:
                self.city_list.append((self.city_code, normalize('NFKD',self.city_name).encode('ascii','ignore')))
    
        if self.parsing_first_child and tag == 'td':
            self.parsing_first_child = False

        if tag == 'table':
            if self.parsing_listagem:
                self.parsing_listagem = False

    def get_city_list(self):
        return self.city_list