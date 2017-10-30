from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from newspaper import Article
import urllib.request as req
import urllib.parse as p


def validate_url ( url ) :
    try:
        request =  req.Request ( url )
        response = req.urlopen(request)
        print ( url )
        article = Article ( url )
        article.download ()
        article.parse ()
        article.nlp ()
        return article.summary
    except:
        return ''
        print ( 'prost' )
def train ( ) :
    with open('alin.txt') as f:
         content = f.readlines()
    constructed_array = ''
    for line in content :
        if line is not None :
            validate_url ( line )
            data = validate_url ( line )
            if data is not None :
               constructed_array +=  data
    return constructed_array 
