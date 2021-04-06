from project.resources.utils.requets_api import RequestApi
import json
import string
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
        self.insert_log(data, region['translations']['es'])
        result['data'].append(data)

        return result

    def validation_ip(self, ip, list_ip):
        ip_aws = list(map(lambda x: x['ip_prefix'][:-3] , list_ip))
        return ip_aws.__contains__(ip)
    
    def get_distance(self, distance_source):
        coordinate_argen = json.loads(self.request.get_region())
        distance_calculated = distance(coordinate_argen['latlng'], distance_source)
        return round(distance_calculated.kilometers)
    
    def insert_log(self, data, name):
        data_insert = {
            "ip": data['ip'],
            "country": name,
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

    def get_country(self, name):
        result = {
            "data": [],
            "details": []
        }
        country = self.__repository_register.select()

        if len(country) > 0:
            max_value = max(country_max['distance'] for country_max in country)
            min_value = min(country_min['distance'] for country_min in country)
            value_max = self.get_list_country(max_value, country, 'distance')
            value_min = self.get_list_country(min_value, country, 'distance')
            value_country_user = self.get_list_country(string.capwords(name), country, 'country')


            distance_close = {
                "ip": value_max[0]['ip'],
                "country": value_max[0]['country']
            }

            distance_far = {
                "ip": value_min[0]['ip'],
                "country": value_min[0]['country']
            }

            data_result ={
                "ip_max": distance_close,
                "ip_min": distance_far,
                "country_select": value_country_user
            }
            result['data'].append(self.get_complements_country(data_result, value_min, value_max))
        self.insert_log_user()    
        return result

    def get_complements_country(self, country, value_min, value_max):
        result = {
            "ip_close" : country['ip_max'],
            "ip_far": country['ip_min'],
            "ip_selected": {}
        }
        if len(country['country_select']) > 0:
            if country['ip_min']['country'] == country['country_select'][0]['country']:
               result['ip_far']['distance_average'] = self.sum_values(value_min)
            elif country['ip_max']['country'] == country['country_select'][0]['country']:
               result['ip_close']['distance_average'] = self.sum_values(value_max)
            else:
                result['ip_selected']['ip'] = country['country_select'][0]['ip']
                result['ip_selected']['country'] = country['country_select'][0]['country']
                result['ip_selected']['distance_average'] = self.sum_values(country['country_select'])
        return result    

    def get_list_country(self, value, country, column_name):
        list_value = [data for data in country if data[column_name] == value]
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