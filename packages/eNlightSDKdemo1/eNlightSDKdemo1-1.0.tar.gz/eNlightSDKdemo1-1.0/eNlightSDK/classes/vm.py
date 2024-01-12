from typing import Any, Optional
import requests
import json
from classes.api_caller import caller

class VM:
    def list(
        session: str, host: str, vm_guid: Optional[str] = None, get_utilization: Optional[bool] = None, vmm_ip: Optional[str] = None, vmm_id: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None, search_text: Optional[str] = None, encryption_text: Optional[str] = None, compute_name: Optional[str] = None, vm_group: Optional[str] = None, vm_status: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, export_type: Optional[str] = None, tools_installed: Optional[str] = None, filter_tag: Optional[str] = None, call_from: Optional[str] = None, hsgcombo: Optional[str] = None, status: Optional[str] = None, power_state: Optional[str] = None, compute_type: Optional[str] = None, is_hsg_vm: Optional[str] = None, data_from_date: Optional[str] = None, data_to_date: Optional[str] = None
    ) -> None:
        try:
            api_endpoint = "vms"
            api_call_url = f"http://{host}:30157/{api_endpoint}"
            method = "GET"

            params = {
                "vm_guid": vm_guid,
                "get_utilization": get_utilization,
                "vmm_ip": vmm_ip,
                "vmm_id": vmm_id,
                "limit": limit,
                "offset": offset,
                "search_text": search_text,
                "encryption_text": encryption_text,
                "compute_name": compute_name,
                "vm_group": vm_group,
                "vm_status": vm_status,
                "from_date": from_date,
                "to_date": to_date,
                "export_type": export_type,
                "tools_installed": tools_installed,
                "filter_tag": filter_tag,
                "call_from": call_from,
                "hsgcombo": hsgcombo,
                "status": status,
                "power_state": power_state,
                "compute_type": compute_type,
                "is_hsg_vm": is_hsg_vm,
                "data_from_date": data_from_date,
                "data_to_date": data_to_date
            }

            response = caller(session, api_call_url, method, params)
            return response

        except Exception as e:
            print(e)

    def get(session, host, vm_guid):
        try:
            api_endpoint = "vms"
            api_call = f"http://{host}:30157/{api_endpoint}/{vm_guid}"
            method = "GET"
            response = caller(session, api_call, method)
            return response
            
        except Exception as e:
            print(e)
            

    def create(session, host, data):
        try:
            api_endpoint = "vms"
            api_call = f"http://{host}:30157/{api_endpoint}"
            method = "POST"
            response = caller(session, api_call, method, data=data)
            return response
            
        except Exception as e:
            print(e)

    def update(session, host, vm_guid, data):
        try:
            api_endpoint = "vms"
            api_call = f"http://{host}:30157/{api_endpoint}/{vm_guid}"
            method = "PUT"
            response = caller(session, api_call, method, data=data)
            return response
            
        except Exception as e:
            print(e)


    def delete(session, host, vm_guid, delete_mode, schedule):
        try:
            api_endpoint = "vms"
            api_call = f"http://{host}:30157/{api_endpoint}/{vm_guid}"
            method = "DELETE"
            payload= {"vm_guid" :vm_guid, "delete_mode":delete_mode, "schedule": schedule}
            response = caller(session, api_call, method, params=payload)
            return response
            
        except Exception as e:
            print(e)
