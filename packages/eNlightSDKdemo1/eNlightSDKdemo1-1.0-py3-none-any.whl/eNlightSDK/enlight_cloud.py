
from classes.vm import VM
from typing import Optional, Dict, Any
import requests
from classes.set_projects import set_active_project

class EnlightCloud:

	def __init__(self, host, token, project_id):		
		self.host = host
		self.session = token
		self.project_id = project_id
		set_active_project(self.host, self.session, self.project_id)

	
	def vm_get(self, vm_guid):
		vm_get = VM.get(self.session,self.host,vm_guid)
		return vm_get

	def vm_list(self, vm_guid: Optional[str] = None, get_utilization: Optional[bool] = None, vmm_ip: Optional[str] = None, vmm_id: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None, search_text: Optional[str] = None, encryption_text: Optional[str] = None, compute_name: Optional[str] = None, vm_group: Optional[str] = None, vm_status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, export_type: Optional[str] = None, tools_installed: Optional[str] = None, filter_tag: Optional[str] = None, call_from: Optional[str] = None, hsgcombo: Optional[str] = None, status: Optional[str] = None, power_state: Optional[str] = None, compute_type: Optional[str] = None, is_hsg_vm: Optional[str] = None, data_from_date: Optional[str] = None, data_to_date: Optional[str] = None):
		vm_list = VM.list(self.session, self.host, vm_guid=vm_guid, get_utilization=get_utilization, vmm_ip=vmm_ip, vmm_id=vmm_id, limit=limit, offset=offset, search_text=search_text, encryption_text=encryption_text, compute_name=compute_name, vm_group=vm_group, vm_status=vm_status, from_date=from_date, to_date=to_date, export_type=export_type, tools_installed=tools_installed, filter_tag=filter_tag, call_from=call_from, hsgcombo=hsgcombo, status=status, power_state=power_state, compute_type=compute_type, is_hsg_vm=is_hsg_vm, data_from_date=data_from_date, data_to_date=data_to_date)
		return vm_list

	def vm_create(self, data):
		vm_create = VM.create(self.session, self.host, data)
		return vm_create

	def vm_update(self, vm_guid, data):
		vm_update = VM.update(self.session, self.host, vm_guid, data)
		return vm_update

	def vm_delete(self, vm_guid, delete_mode, schedule):
		vm_delete = VM.delete(self.session, self.host, vm_guid, delete_mode, schedule)
		return vm_delete




