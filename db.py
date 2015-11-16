import yaml
from tabulate import tabulate

class Library:
    
    def read_data(self):
        with open('database/library.yml', 'r') as f:
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
        table=[]
        a = self.read_data()
        for item in a:
            if item['SHELF']==key:
                for book in item['content']:
                    if 'BOOK' in book:
                        table.append([book['BOOK'], book['name']])
                    else:
                        continue
                break
            count+=1

        print tabulate(table,
                       headers=['BOOK', 'DESCRIPTION'],
                       tablefmt='orgtbl')

    def book(self, key):
        db = None

        
            
