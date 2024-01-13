from src.pangaeapy.pandataset import PanDataSet
from src.pangaeapy.panquery import PanQuery as pq

pandata = PanDataSet('doi:10.1594/PANGAEA.924668')
print(pandata.data['Date/Time'][0])