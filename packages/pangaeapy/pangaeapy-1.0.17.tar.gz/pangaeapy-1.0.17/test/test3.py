import os

from src.pangaeapy.exporter.pan_dwca_exporter import PanDarwinCoreAchiveExporter
from src.pangaeapy.pandataset import PanDataSet
import inspect
#ds = PanDataSet('10.1594/PANGAEA.756784',expand_terms=True, enable_cache=False)
#ds = PanDataSet('10.1594/PANGAEA.896818',expand_terms=True)
#https://doi.pangaea.de/10.1594/PANGAEA.552469 life stages
#ds = PanDataSet('10.1594/PANGAEA.231616',expand_terms=1)
#ds = PanDataSet('10.1594/PANGAEA.953846')
ds = PanDataSet('10.1594/PANGAEA.931888',expand_terms=1)
dwca_exporter = PanDarwinCoreAchiveExporter(ds)
print(dwca_exporter.get_eml_xml().decode())
#print(ds.getParamDict())
#for ev in ds.events:
#    print(ev.campaign.name)
#    print(ev.campaign.start)
#print(ds.data.head(100))

#taxoncolums = dwca_exporter.get_taxon_columns()
#print('####',dwca_exporter.verify(),dwca_exporter.logging)
#print(taxoncolums)
#print(dwca_exporter.get_dwca_data(taxoncolums))
#zipbuffer=ds.to_dwca(save=True)
#print(zipbuffer)
#if isinstance(zipbuffer, BytesIO):
#    print('####')
#create_res = dwca_exporter.create()
#dwca_exporter.save()
#print(dwca_exporter.filelocation)
print(dwca_exporter.logging)
### EML
