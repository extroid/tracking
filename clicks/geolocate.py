class ip_to_geo:
    def __init__(self,ip,city=False,state=False,country=True):
        if ip:
            return look_up(ip,city,state,country)
        
def look_up(self,ip,city,state,country):
    status = 'OK' #or error
    return (city,state,country,status)