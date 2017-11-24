import os
import functions.utils.getcategory

# create a directory
directory = os.getcwd() + '/' + 'RECORD'
if not os.path.exists(directory):
    os.makedirs(directory)

cats = functions.utils.getcategory.get_category()
print 'got categories'

cats.to_csv(directory + '/' + 'categories.csv', index=False)