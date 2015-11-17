import yaml
from tabulate import tabulate

class L:
    
    def read_data(self, key='database/library.yml'):
        with open(key, 'r') as f:
            doc = yaml.load(f)

        return doc

    def shelves(self):

        table=[]
        doc = self.read_data()    
        for item in doc:
            table.append([item['SHELF'], item['name']])

        print tabulate(table,
                       headers=['SHELF', 'DESCRIPTION'],
                       tablefmt='orgtbl')

    def shelf(self, key):
        count = 0
        book_count = 0
        table=[]
        a = self.read_data()
        for item in a:
            count += 1
            if item['SHELF']==key:
                for book in item['content']:
                    if 'BOOK' in book:
                        book_count += 1
                        table.append(['%d/%d' % (count, book_count), book['BOOK'], book['name'][:50]])
                    else:
                        continue
                break
            count+=1
        
        if len(table)==0:
            print '-----------'
            print 'No Results'
            print '-----------'
        else:
            print tabulate(table,
                           headers=['ID', 'BOOK', 'DESCRIPTION'],
                           tablefmt='orgtbl')

    def book(self, key):
        count_shelf = 0
        count_book = 0
        count_page = 0
        table=[]
        a = self.read_data()
        for shelf in a:
            count_shelf += 1
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book += 1
                    if book['BOOK']==key:
                        for page in book['content']:
                            count_page += 1
                            table.append(['%d/%d/%d' % (count_shelf, count_book, count_page) , page['PAGE'], page['name'][:50]])
                            
        if len(table)==0:
            print '-----------'
            print 'No Results'
            print '-----------'
        else:
            print tabulate(table,
                           headers=['ID', 'PAGE', 'DESCRIPTION'],
                           tablefmt='orgtbl')

    def page(self, key):
        count_shelf = 0
        count_book = 0
        count_page = 0
        table = []
        a = self.read_data()
        for shelf in a:
            count_shelf += 1
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book +=1
                    for page in book['content']:
                        if 'PAGE' in page and page['PAGE']==key:
                            count_page += 1
                            print page['path']
                            b =  self.read_data('database/%s' % (page['path']))
                            print b['REFERENCES']
                            print b['COMMENTS']

                
            

        
            
