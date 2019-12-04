'''
Created on Oct 15, 2014

@author: Trung Huynh

'''
from pygoogle import *

from googleplaces import *
from googleplaces import lang
from googleplaces import types

from xml.dom.minidom import Document

#Do not share this key to anyone, it's used to test
MY_API_KEY = 'AIzaSyCkW4zF8TqEZk2_cvN4W97wx2iVmWAAoqw'

#Just for testing Google Ajax, not in use
def test():
    parser = argparse.ArgumentParser(description='A simple Google search module for Python')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Verbose mode')
    parser.add_argument('-p', '--pages', dest='pages', action='store', default=1, help='Number of pages to return. Max 10')
    parser.add_argument('-hl', '--language', dest='language', action='store', default='en', help="language. default is 'en'")
    parser.add_argument('-ip', '--userip', dest='userip', action='store', default='123.20.0.201', help='userip. default is 123.20.0.201')
    parser.add_argument('query', nargs='*', default=None)

    args = parser.parse_args()
    query = ' '.join(args.query)
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    if not query:
        parser.print_help()
        exit()
    search = pygoogle(query=query, pages=args.pages, hl=args.language, userip=args.userip, log_level=log_level)
    search.display_results()

def save(filename = 'restaurant', restaurants=None):
    doc = Document()
 
    root = doc.createElement('list')
    
    doc.appendChild(root)
    
    for restaurant in restaurants:
        # Create Element
        tempChild = doc.createElement('restaurant')
        name = doc.createElement('name')
        text = doc.createTextNode(restaurant[0].encode('utf-8').strip())
        name.appendChild(text)
        
        address = doc.createElement('address')
        text = doc.createTextNode(restaurant[1].encode('utf-8').strip())
        address.appendChild(text)
        
        lphone = doc.createElement('local_phone')
        text = doc.createTextNode(restaurant[2])
        lphone.appendChild(text)
        
        iphone = doc.createElement('inter_phone')
        text = doc.createTextNode(restaurant[3])
        iphone.appendChild(text)
        
        tempChild.appendChild(name)
        tempChild.appendChild(address)
        tempChild.appendChild(lphone)
        tempChild.appendChild(iphone)
        
        root.appendChild(tempChild)
    try:
        doc.writexml( open(filename + '.xml', 'w'),
                  indent="  ",
                  addindent="  ",
                  newl='\n')
        print "Save completed!"
    except Exception as e:
        print e.value
        
    doc.unlink()

def retrieve():

    google_places = GooglePlaces(MY_API_KEY)

    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
            location='Ho Chi Minh, Vietnam',
            keyword='nha hang',
            radius=20000,
            types=[types.TYPE_FOOD])

    if query_result.has_attributions:
        print query_result.html_attributions

    restaurants = []

    for place in query_result.places:
        # Returned places from a query are place summaries.
        print place.name
        
        #print place.geo_location
        #print place.reference

        place.get_details()

        #print place.details
        print place.vicinity
        print place.local_phone_number
        print place.international_phone_number + '\n'
        
        restaurant = [place.name, place.vicinity, place.local_phone_number, place.international_phone_number]
        restaurants.append(restaurant)
        #print place.website
        #print place.url

    while True:
        accept = raw_input('Do you want to save all these? (Y/N): ')
        if accept.lower() == "y" or accept.lower() == 'n':
            break

    if accept.lower() == "y":
        filename = raw_input('Enter file name [restaurant.xml]: ')
        if filename == '':
            save('restaurant', restaurants)
        else:
            save(filename, restaurants)
        

def main():

    #test()
    retrieve()

if __name__ == "__main__":
    main()

