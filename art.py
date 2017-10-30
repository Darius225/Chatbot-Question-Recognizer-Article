from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from newspaper import Article
import urllib.request as req
import urllib.parse as p


def validate_url ( url ) :
    try:
        request =  req.Request ( url )
        response = req.urlopen(request)
        article = Article ( url )
        article.download ()
        article.parse ()
        return article.text
    except:
        return ''
        print ( 'prost' )
def train ( content  ) :
    constructed_array = ''
    data = validate_url ( content )
    if data is not None :
        constructed_array += data
    return constructed_array
