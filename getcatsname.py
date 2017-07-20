import os
import ks.utils.getcategory

# create a directory
directory = os.getcwd() + '/' + 'RECORD'
if not os.path.exists(directory):
    os.makedirs(directory)

cats = ks.utils.getcategory.get_category()
print 'got categories'

cats.to_csv(directory + '/' + 'categories.csv', index=False)