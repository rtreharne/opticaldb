import yaml
from tabulate import tabulate
from numpy import linspace, sqrt
from pylab import *
import matplotlib.pyplot as plt
from matplotlib import rc
rc('mathtext', default='regular')

N = 100

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
        
        count_shelf = 0
        count_book = 0
        table=[]
        a = self.read_data()
        for item in a:
            count_shelf += 1
            if item['SHELF']==key:
                for book in item['content']:
                    if 'BOOK' in book:
                        count_book += 1
                        table.append(['%d%03d' % (count_shelf, count_book), book['BOOK'], book['name'][:50]])
                    else:
                        continue
                break
        
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
            count_book=0
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book += 1
                    if book['BOOK']==key:
                        for page in book['content']:
                            count_page += 1
                            table.append(['%d%03d%02d' % (count_shelf, count_book, count_page) , page['PAGE'], page['name'][:50]])
                            
        if len(table)==0:
            print '-----------'
            print 'No Results'
            print '-----------'
        else:
            print tabulate(table,
                           headers=['ID', 'PAGE', 'DESCRIPTION'],
                           tablefmt='orgtbl')

    def page(self, key):
        try:
            key = int(key)
        except ValueError:
            return 'Please enter a valid ID'

        key = map(int, str(key))
        shelf_id = key[0]
        book_id = int(''.join(map(str, key[1:4])))
        page_id = int(''.join(map(str, key[4:])))
        count_shelf = 0
        count_book = 0
        count_page = 0
        table = []
        a = self.read_data()
        for shelf in a:
            count_shelf += 1
            if count_shelf == shelf_id:
                for book in shelf['content']:
                    if 'BOOK' in book:
                        count_book += 1
                        if count_book == book_id:
                            for page in book['content']:
                                count_page += 1
                                if count_page == page_id:
                                    return  self.read_data('database/%s' % (page['path']))

    def search(self, keyword, deep=False):
        a = self.read_data()
        count_shelf = 0
        count_book = 0
        count_page = 0
        table = []
        for shelf in a:
            count_shelf += 1
            count_book = 0
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book += 1
                    count_page = 0
                    for page in book['content']:
                        if 'PAGE' in page:
                            count_page += 1
                            deep_check = ''
                            if deep:
                                try:
                                    deep_check = str(self.read_data('database/%s' % (page['path'])))
                                except:
                                    pass
                            check = '%s, %s, %s' % (page['PAGE'], page['path'], deep_check)
                            if keyword.lower() in check.lower():
                                table.append(['%d%03d%02d' % (count_shelf, count_book, count_page) , shelf['SHELF'], book['BOOK'], page['PAGE'], page['name'][:30]])
                            
        if len(table)==0 and deep:
            print '-----------'
            print 'No Results'
            print '-----------'
        elif len(table) == 0:
            self.search(keyword, deep=True)
        else:
            print tabulate(table,
                           headers=['ID', 'SHELF', 'BOOK', 'PAGE', 'DESCRIPTION'],
                           tablefmt='orgtbl')
        
    def plot(self, key):
        page = self.page(key)
        for item in page['DATA']:
             if item['type'] == 'formula 1':
                 data = []
                 data = self.f2(item['coefficients'], item['range'])
             elif item['type'] == 'formula 2':
                 data = []
                 data = self.f2(item['coefficients'], item['range'])
             elif item['type'] == 'formula 4':
                 data = []
                 data = self.f4(item['coefficients'], item['range'])
             elif item['type'] == 'tabulated nk':
                 data = []
                 data = self.tbnk(item['data'])
             else:
                 return "Can't do this yet"

        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.plot(data[0], data[1], 'o-', color='red')
        ax.set_ylabel(r"$n$")
        ax.set_xlabel(r"Wavelength, $\lambda$ ($\mu$m)")
        if len(data)>2:
            ax2 = ax.twinx()
            ax2.plot(data[0], data[2], 'o-', color='blue')
            ax2.set_ylabel(r"$\kappa$")
        plt.show()
                 

    def f1(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        x = linspace(wlrange[0], wlrange[1], N)
        n = []
        for i in range(0, N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += (coeffs[j]*x[i]**2)/(x[i]**2 - coeffs[j+1]**2)
            sum += coeffs[0]
            n.append(sqrt(sum+1))
        return x, n
    def f2(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        x = linspace(wlrange[0], wlrange[1], N)
        n = []
        for i in range(0, N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += (coeffs[j]*x[i]**2)/(x[i]**2 - coeffs[j+1])
            sum += coeffs[0]
            n.append(sqrt(sum+1))
        return x, n
    
    def f4(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        x = linspace(wlrange[0], wlrange[1], N)
        n = []
        
        for i in range(0, N):
            sum = coeffs[0]
            for j in range(1,8,4):
                sum += (coeffs[j]*x[i]**coeffs[j+1])/(x[i]**2 - coeffs[j+2]**coeffs[j+3])
            if len(coeffs)>9:
                for k in range(9, len(coeffs)-1,2):
                    sum += coeffs[k]*x[i]**coeffs[k+1]
            n.append(sqrt(sqrt(sum**2)))
        return x, n

    

    def tbnk(self, data):
        data = data.split('\n')
        data.pop()
        data = [row.split(' ') for row in data]
        x = [float(row[0]) for row in data]
        n = [float(row[1]) for row in data]
        k = [float(row[2]) for row in data]

        return x, n, k
        
        
