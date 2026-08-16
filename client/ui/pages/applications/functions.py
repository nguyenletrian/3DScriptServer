from ....api.rest import RestAPI


def activate(page, application_id):
    if isinstance(application_id, dict): application_id = application_id.get("id")
    return RestAPI("application-instances")._request("POST", "/activate", {"application_id": int(application_id)})
