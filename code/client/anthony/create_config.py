import json
data = {'cube_id':1}
file = open('config.txt', 'w+')
json.dump(data, file)
file.close()
