from src.pangaeapy.pandataset import PanDataSet
from src.pangaeapy.panquery import PanQuery as pq

bb = [-11, 48, -10.5, 48.5]
#my_query = pq("method:CTD/Rosette", bbox = bb, limit = 500)
my_query = pq("GDGT data from soils in tropical South America")
my_query.totalcount
import requests
#auth_token = 'sa7hn6kspc5i2cbo6bk2q5gtclypy5skipssvunw5oslxatqbnck6teva3cnnl6f'
n =1
ds = None
successes = 0
errors = 0
for i in range(my_query.totalcount):
  print(my_query.result[i])
  if my_query.result[i]["type"] == 'child':
    # Checks if the data set is a parent data set, in which case we skip it,
    # only "child" data sets containing actual data matter:
    uid = int(my_query.result[i]["URI"].split('.')[-1])
    try:
      ds=PanDataSet(uid)
      successes += 1
    except Exception as e:
      print(uid)
      print(e)
      errors += 1
print(errors, successes)
if ds:
  print(ds.logging)