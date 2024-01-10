import json
import requests
import os
from tornado import gen
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from .websocket import DQGPUWebsocketHandler

import tornado


class RouteHandler(APIHandler):
    def get(self):
        self.finish(json.dumps({
            "data": "This is /dq-gpu/get-example endpoint!"
        }))


class DownloadHandler(APIHandler):

    def post(self):
      jsonObj = self.get_json_body()
      print(json.dumps(jsonObj))
      new_file_info = {
          'fileName': jsonObj["fileName"],
          'url': jsonObj["url"],
          'status': 0
      }
      self.downFile(new_file_info)
      model = {
          'errCode': 0,
          'errMsg': '',
          'data': ''
        }
      self.finish(json.dumps(model))


    def downFile(self, new_file_info):
      fileName = new_file_info["fileName"]
      if os.path.exists(fileName):
          new_file_info["status"] = 1
          return

      dirName = os.path.dirname(fileName)
      print(f"dirName = {dirName}")
      if len(dirName) != 0 and not os.path.exists(dirName):
          os.makedirs(dirName)
      try:
          r = requests.get(new_file_info['url'])
          with open(fileName, "wb") as f:
              f.write(r.content)
              new_file_info["status"] = 1
              print("下载文件完成...")
      except:
          print("下载文件失败...")
          new_file_info["status"] = 0
        

_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"
def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "dq-gpu", "get-example")
    download_route_pattern = url_path_join(base_url, "dq-gpu", "download")
    handlers = [
        (route_pattern, RouteHandler),
        (download_route_pattern, DownloadHandler),
        (r"/dq/kernels/%s/channels" % _kernel_id_regex, DQGPUWebsocketHandler)
    ]

    web_app.add_handlers(host_pattern, handlers)
