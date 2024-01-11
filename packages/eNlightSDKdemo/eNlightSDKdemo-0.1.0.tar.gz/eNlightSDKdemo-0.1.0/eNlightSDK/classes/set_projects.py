import json, os
from classes.api_caller import caller
# from classes.get_config import get_config_data
import codecs
import base64

def set_active_project(host, token, project_id):
	try:
		# data = get_config_data()
		# if "host" in data and data['host'] != "":

		# 	host = data['host']
		# else:
		# 	print("Please provide host URL")

		# if "project_id" in data and data["project_id"]!="":
		# 	project_id= data['project_id']
		# else:
		# 	print("please enter project id")

		# if "token" in data and data['token'] != "":
		# 	token = data['token']
		# else:
		# 	print("Please provide valid token")

		port = 30142
		api_endpoint = "set_active_project"
		project_url = f"http://{host}:{port}/{api_endpoint}"
		parameters = {"project_id": project_id, "module_key": "ENLIGHT360"}
		method="POST"
		response_data = caller(token,project_url,method,parameters)
		# print(response_data)


	except Exception as e:
		print("get project id",e)

