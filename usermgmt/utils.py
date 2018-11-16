import random
from .models import User

def get_referalurl(request,data):
    return  str(request.get_host())+'/usermgmt/api/'+str(data)


def generate_secretkey():
    secretkey =random.getrandbits(50)
    return secretkey


def authenticate_key(secretkey):
    try:
        user = User.objects.get(referal_code=secretkey)
        return user
    except:
        return False