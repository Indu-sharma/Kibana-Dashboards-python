__author__ = "Indu Sharma"
__copyright__ = "Copyright (C) 2018 Indu Sharma"
__license__ = "Public Domain"
__version__ = "1.0"

""" Automatically create TimeLion Visualizations and set them as Dashboards with Python """

import requests
import json


class Vizualize:
    
    """ Generic Utility to manupulate the Kibana TimeLion Visualizations """  
    
    _id = 1001

    def __init__(self, title="AutomatedVisualisations_", ui="http://kibana:5601/",
                 api='api/saved_objects/visualization/'):
        self.id_list = []
        self.api = api
        self.ui = ui
        self.title = title

    @classmethod
    def set_initial_id(cls, _id):
        cls._id = _id

    def __iter__(self):
        return iter(self.id_list)

    def create(self, expression, vis_type='timelion'):
        title = self.title + str(self._id)
        visState = {
            "title": title,
            "type": vis_type,
            "params": {
                "expression": expression,
                "aggs": []
            },
            "interval": "auto"
        }

        data = {
            "attributes": {
                "title": title,
                "visState": json.dumps(visState),
                "uiStateJSON": "{}",
                "description": "",
                "kibanaSavedObjectMeta": {"searchSourceJSON": "{}"},
                "version": 1,
            }
        }
        data = json.dumps(data)
        res = requests.post(self.ui + self.api + str(self._id) + "?overwrite=true",
                            headers={'content-type': 'application/json', 'kbn-xsrf': 'reporting'}, data=data)

        self.id_list.append(self._id)
        self._id = int(self._id) + 1

        print(res.content)


class Dashboards:
    _id = 5001

     """ Generic Utility to manupulate the Kibana Dashboards """  
    
    def __init__(self, title="AutomatedDashboards_", ui="http://kibana:5601/", api='api/saved_objects/dashboard/'):
        self.api = api
        self.ui = ui
        self.title = title

    @classmethod
    def set_initial_id(cls, _id):
        cls._id = _id

    def create(self, vizualizers, time_from="", time_to=""):
        title = self.title + str(self._id)

        panel_dict = []
        x, y, i = 0, 0, 10
        w = 20
        h = 20
        for viz in vizualizers:
            i = + 1
            viz_dict = {
                "gridData": json.dumps({"w": w, "h": h, "x": x, "y": y, "i": str(i)}),
                "version": "6.1.3",
                "panelIndex": str(i),
                "type": "visualization",
                "id": str(viz)
            }
            panel_dict.append(viz_dict)

        data = {
            "attributes": {
                "title": title,
                "hits": 0,
                "description": "",
                "panelsJSON": json.dumps(panel_dict),
                "uiStateJSON": "{}",
                "version": 1,
                "timeRestore": False,
                "kibanaSavedObjectMeta":
                    {
                        "searchSourceJSON": json.dumps(
                            {"query": {"query": "", "language": "lucene"}, "filter": [], "highlightAll": True,
                             "version": True})
                    },
                "optionsJSON": json.dumps({"darkTheme": False, "useMargins": True, "hidePanelTitles": False}),
                "timeTo": "Mon Jun 25 2018 18:20:56 GMT+0530",
                "timeFrom": "Mon Jun 25 2018 17:50:56 GMT+0530"
            }
        }
        data = json.dumps(data)
        res = requests.post(self.ui + self.api + str(self._id) + "?overwrite=true",
                            headers={'content-type': 'application/json', 'kbn-xsrf': 'reporting'}, data=data)
        print(self.ui + self.api + str(self._id) + "?overwrite=true", data)
        self._id = int(self._id) + 1
        print(res.content)


# Testing -- Usage, Make TimeLion Query 

exp = ".es(index=perfsec-d50-1*, q='system.process.name:gsifilter_huntjob-Interactive',metric=sum:system.process.memory.size,fit=nearest).label('Run1_VirtualMemory(GB)').divide(1073741824).color(red).lines(fill=2,width=1),.es(index=perfsec-d50-2*, offset=+68m,q='system.process.name:gsifilter_huntjob2-Interactive', metric=sum:system.process.memory.size,fit=nearest).label('Run2_VirtualMemory(GB)').divide(1073741824).color(green).lines(fill=2,width=1)"

# Create Visualizations with above TimeLion Query

C = Vizualize()
C.set_initial_id(5000)
C.create(expression=exp)

# Create Dashboard with the visualizations created above
Dashboards().create(C)
