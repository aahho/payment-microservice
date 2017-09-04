import uuid, os, pygeoip, bcrypt, random, datetime, env

def getenv(key):
    return env.getKey(key)

##
# To generate unique code
# uuid package
##
def generate_uuid():
	return uuid.uuid4()

##
# To hash the access-token
##
def generate_pass_key():
	return bcrypt.hashpw(str(generate_uuid()), bcrypt.gensalt())

##
# To get requested ip current location
# Reference http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
##
def get_location(request):
	ip = get_user_ip(request)
	BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	collection = pygeoip.GeoIP(BASE_PATH+'/GeoLiteCity.dat')
	return collection.record_by_name(ip)

##
# GET USER IP ADDRESS FROM REQUEST
##
def get_user_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	elif request.META.get('HTTP_X_REAL_IP'):
		ip = request.META.get('HTTP_X_REAL_IP')
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

##
# To hash the access-token
##
def generate_hashed_token():
	return bcrypt.hashpw(str(generate_uuid()), bcrypt.gensalt())
	