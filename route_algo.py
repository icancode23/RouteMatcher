import polyline,requests,json

from geopy.distance import vincenty
############## Sending first sample request to directions api ##########


lat1=raw_input("Enter the Latitude of Start point of Car owner: ")
long1=raw_input("Enter the Longitude of Start point of Car Owner: ")
lat2=raw_input("Enter the Latitude of End point of Car Owner: ")
long2=raw_input("Enter the Longitude of End point of Car Owner: ")

###### Get coordinates for Passenger route ##########
lat3=raw_input("Enter the Latitude of Start point of Passenger: ")
long3=raw_input("Enter the Longitude of Start point of Passenger: ")
lat4=raw_input("Enter the Latitude of End point of Passenger: ")
long4=raw_input("Enter the Longitude of End point of Passenger: ")

###### Get coordinates for Owner route ##########
url1="https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&key=AIzaSyAacNLiHHRaHxA___8h9cvTgtrqLfHEOUQ"%(lat1,long1,lat2,long2)
# url1="https://maps.googleapis.com/maps/api/directions/json?origin=28.621732,77.055638&destination=28.552784,77.058683&key=AIzaSyAacNLiHHRaHxA___8h9cvTgtrqLfHEOUQ"
re_1=requests.get(url1)
route_1_polyline=json.loads(re_1.text)["routes"][0]["overview_polyline"]["points"]
re_1_list=polyline.decode(route_1_polyline)


###### Get coordinates for Passenger route ##########
url2="https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&key=AIzaSyAacNLiHHRaHxA___8h9cvTgtrqLfHEOUQ"%(lat3,long3,lat4,long4)
# url2="https://maps.googleapis.com/maps/api/directions/json?origin=28.619365,77.033534&destination=28.557110,77.061303&key=AIzaSyAacNLiHHRaHxA___8h9cvTgtrqLfHEOUQ"
re_2=requests.get(url2)
route_2_polyline=json.loads(re_2.text)["routes"][0]["overview_polyline"]["points"]
re_2_list=polyline.decode(route_2_polyline)


################## Start Matching in O(MxN) ########################

matched_points=[]
prev=None
dist=0

for cord in re_1_list:
	for cord2 in re_2_list:
		if cord==cord2:
			matched_points.append(cord)
			#print cord
			if(prev!=None):
				dist +=  vincenty(prev,cord).miles * 1.6
			prev=cord


####### Calculating the offset from the first and last point #############
########### initial offset ###############
initial_offset=vincenty(re_2_list[0],matched_points[0]).miles * 1.6

final_offset=vincenty(re_2_list[len(re_2_list)-1],matched_points[len(matched_points)-1]).miles * 1.6

print "The initial distance is ",initial_offset
print "The Final Offset is ",final_offset

if(final_offset<0.5 and initial_offset<0.5):
	print "Hey Buddy we found a match"

print len(matched_points)

print "The total common path distance is :",dist,"km"

##get the total distance of both the sides and get a particular proportion above which we can declare a match
## get the first and last matched co_ordinate and find how far the two points are from the given co_ordinate