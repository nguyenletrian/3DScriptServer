from ....api.rest import RestAPI


def activate(page, application_id):
    api = RestAPI("application-instances")
    return api._request("POST", "/activate", {"application_id": application_id})
