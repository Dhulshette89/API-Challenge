import requests
import lob
import sys
import urllib.request
import random  

if __name__ == '__main__':
    
    lob_key = 'test_91135a93a7f7d98990559624ea45ff923c9'
    google_key = 'AIzaSyC6vGh3vqenYV5NXdhEyd0CtEXe0Qn51Hc'
    
    from_address_map = {
    'name':input("Please enter name: "),
    'address_line1': input("Please enter address_line1: "),
    'address_line2': input("Please enter address_line2: "),
    'address_city': input("Please enter address_city: "),
    'address_state':input("Please enter address_state: "),
    'address_zip': input("Please enter address_zip: ")
    }
    
    from_str = ""
    for key in ['name','address_line1', 'address_line2', 'address_city', 'address_state', 'address_zip']:
        while (not from_address_map[key] and key != 'address_line2'):
            print("[ERROR]: " + key + " cannot be empty.")
            from_address_map[key] =input("Please enter " + key + ":- ") 
        if key != 'name':
            from_str += from_address_map[key]
            
    
    content = input("Please enter your message (max 200 words): ")
    length = len(content.split())
    while(length > 200):
        print("[ERROR]: Message cannot exceed 200 word limit. Current message has " + str(length) + " words")
        content = input("Please enter your message: ")
        length = len(content.split())
        
    
    url = "https://www.googleapis.com/civicinfo/v2/representatives?address=" + from_str + "&includeOffices=true&levels=country&roles=legislatorUpperBody" +"&key=" + google_key
    
    r = requests.get(url)
    response = r.json();
    
    if ( 'error' in  response):
        print('[ERROR]: Code: ' + str(response['error']['code']))
        print('[ERROR]: Message: ' + response['error']['message'])
        sys.exit()
    
    try:
        to_address_map = {
        'name': response['officials'][0]['name'],
        'address_line1': response['officials'][0]['address'][0]['line1'],
        'address_city': response['officials'][0]['address'][0]['city'],
        'address_state': response['officials'][0]['address'][0]['state'],
        'address_zip': response['officials'][0]['address'][0]['zip']
        }
    except Exception as e:
        print('[ERROR]: Could not find legislator for the given address. Please try a different one.' + str(e))
        sys.exit()
    
    
    try: 
        lob.api_key = lob_key
        letter = lob.Letter.create(
            description = 'Letter to Legislator',
            to_address = to_address_map,
            from_address = from_address_map,
            file = '<html style="padding-top: 3in; margin: .5 .5 .5 .5in;">Hello {{name}},\
            <br><br>{{content}}<br><br>{{closing}}<br>{{from_name}}</html>',
            merge_variables = {
            'name': to_address_map['name'],
            'content': content,
            'closing': "Sincerely,",
            'from_name': from_address_map['name']
            },
            color = True
            )
    except Exception as e:
            print('[ERROR]: Sorry, I couldn\'t make a letter with your info. Exception message: ' + str(e))
            sys.exit()
    
    letterPDFURL = letter["url"]
    print('\nLetter URL:\n' +  letterPDFURL + '\n')
    '''str1= str(random.randint(1,101))
    name='pdfletterlob'+str1+'.pdf';
    time.sleep(.300)
    urllib.request.urlretrieve(letterPDFURL,name)
    print('The letter is already downloaded in the current directory with name: '+name)'''
    