from project.resources.utils.requets_api import RequestApi
import json
from datetime import datetime
from geopy.distance import distance
from project.resources.utils.security_token import SecurityToken 
from project.infrastructure.repositories.common_repository\
    import CommonRepository

class AppIpService:
    
    COUNTRY = "%s (%s)"
    NUMBER_ONE = 1
    def __init__(self):
        self.request =  RequestApi()
        self.__repository_register = CommonRepository(
         entity_name="register")
        self.__repositoty_user_log = CommonRepository(
         entity_name="userLog")

    def get_app_ip(self, ip):
        data = {}
        result = {
            "data": [],
            "details": []
        }

        get_ip = self.request.get_ip(ip)
        
        if get_ip is None:
            result['details'].append({
                "code": "400",
                "message": "Not found"            
            })
            return result

        aws = json.loads(self.request.get_ip_aws())
        region = json.loads(self.request.get_region(get_ip['countryCode3']))
    
        validation_ip = self.validation_ip(ip, aws['prefixes'])
        distance_final = self.get_distance(region['latlng'])
        data = {
            "ip": ip,
            "date": datetime.now().isoformat(),
            "country": self.COUNTRY % (region['translations']['es'], region['alpha3Code']),
            "iso_code": region['alpha2Code'],
            "estimated_distance": distance_final,
            "belong_AWS": validation_ip

        }
        self.insert_log(data)
        result['data'].append(data)

        return result

    def validation_ip(self, ip, list_ip):
        ip_aws = list(map(lambda x: x['ip_prefix'][:-3] , list_ip))
        return ip_aws.__contains__(ip)
    
    def get_distance(self, distance_source):
        coordinate_argen = json.loads(self.request.get_region())
        distance_calculated = distance(coordinate_argen['latlng'], distance_source)
        return round(distance_calculated.kilometers)
    
    def insert_log(self, data):
        data_insert = {
            "ip": data['ip'],
            "country": data['country'].split(" ")[0],
            "distance": data['estimated_distance']
        }

        ip_validation = self.__repository_register.select(options={"filters":
                             [['ip', "equals", data['ip']]]
                             })

        if len(ip_validation) > 0:
           data_update = {
            "invocation": ip_validation[0]["invocation"] + self.NUMBER_ONE
           }
           self.__repository_register.update(ip_validation[0]['id'], data_update)
        else:                    
            self.__repository_register.insert(data_insert)

    def get_country(self):
        result = {
            "data": [],
            "details": []
        }
        country = self.__repository_register.select()

        if len(country) > 0:
            max_value = max(country_max['distance'] for country_max in country)
            min_value = min(country_max['distance'] for country_max in country)
            value_max = self.get_list_country(max_value, country)
            value_min = self.get_list_country(min_value, country)
            distance_close = {
                "ip": value_max[0]['ip'],
                "country": value_max[0]['country'],
                "mean_invocation": self.sum_values(value_max)
            }

            distance_far = {
                "ip": value_min[0]['ip'],
                "country": value_min[0]['country'],
                "mean_invocation": self.sum_values(value_min)
            }

            data_result ={
                "ip_close": distance_close,
                "ip_far": distance_far
            }
            result['data'].append(data_result)
        self.insert_log_user()    
        return result    

    def get_list_country(self, value, country):
        list_value = [data for data in country if data['distance'] == value]
        list_final = sorted(list_value, key=lambda country: country['invocation'], reverse=True)  
        return list_final

    def sum_values(self, country):
        return sum(item['invocation'] for item in country) / len(country)

    def insert_log_user(self):
        validation_token = SecurityToken().validate_token()
        data = {
            "user_log": validation_token[2],
            "date_log": datetime.now().isoformat()
        }
        self.__repositoty_user_log.insert(data)