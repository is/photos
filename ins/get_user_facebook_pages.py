from defines import getCreds, makeApiCall

def getUserPages( params ) :

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + 'me/accounts' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

params = getCreds() # get creds
params['debug'] = 'yes' # set debug
response = getUserPages( params ) # get debug info

for i in range(len(response['json_data']['data'])):
	print ("\n---- FACEBOOK PAGE INFO %d ----\n" % i) # section heading
	print ("Page Name:") # label
	print (response['json_data']['data'][i]['name']) # display name
	print ("\nPage Category:") # label
	print (response['json_data']['data'][i]['category']) # display category
	print ("\nPage Id:") # label
	print (response['json_data']['data'][i]['id']) # display id
