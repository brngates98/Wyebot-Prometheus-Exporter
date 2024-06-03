import logging
import time
import requests
from prometheus_client import start_http_server, Gauge, Summary, Info

# Set up logging
logging.basicConfig(level=logging.INFO)

# Prometheus metrics definitions
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
LOCATION_COUNT = Gauge('wyebot_location_count', 'Total number of locations')
SENSOR_COUNT = Gauge('wyebot_sensor_count', 'Total number of sensors per location', ['location_id', 'location_name'])
LOCATION_DETAILS = Info('wyebot_location_details', 'Details of locations', ['location_id', 'location_name'])
SENSOR_DETAILS = Info('wyebot_sensor_details', 'Details of sensors per location', ['location_id', 'location_name', 'sensor_id', 'sensor_name'])
SENSOR_DATA = Info('wyebot_sensor_data', 'Details of sensor data', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'model', 'serial_number', 'wireless_mac_address', 'wired_mac_address', 'link_speed', 'power_source', 'uptime', 'software_version', 'license_info'])
SENSOR_NETWORK_INFO = Info('wyebot_sensor_network_info', 'Network information of sensors', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'connection_type', 'dhcp', 'ipaddr', 'ip_subnet', 'ip_gateway', 'dns1', 'dns2', 'wireless_network'])
SENSOR_LLDP_INFO = Info('wyebot_sensor_lldp_info', 'LLDP information of sensors', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'interface', 'via', 'age', 'vlan_id', 'pvid', 'chassis_capability', 'chassis_mgmt_ip', 'chassis_id', 'chassis_descr', 'port_descr', 'port_id', 'auto_negotiation_current'])
ACCESS_POINT_DETAILS = Info('wyebot_access_point_details', 'Access point details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'mac_address', 'hostname', 'hostname_type_id', 'channel', 'phy_type', 'max_data_rate', 'signal_strength', 'vendor', 'classification_type'])
CLIENT_DETAILS = Info('wyebot_client_details', 'Client details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'mac_address', 'hostname', 'ssid', 'bssid', 'vendor', 'phy_type', 'band_name', 'channel'])
SSID_DETAILS = Info('wyebot_ssid_details', 'SSID details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'ssid', 'total_bssids', 'security_name', 'hidden_ssid', 'bssid', 'hostname', 'hidden_bssid', 'total_clients', 'channel', 'signal_strength'])
ISSUE_DETAILS = Info('wyebot_issue_details', 'Issue details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'severity_name', 'problem', 'problem_description', 'solution'])
RF_ANALYTICS = Info('wyebot_rf_analytics', 'RF analytics details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'radio_id', 'channel', 'airtime_total_percent', 'mgmt_percent', 'ctrl_percent', 'data_percent', 'others_percent', 'available_percent', 'noise', 'client_mac_list', 'client_hostname_list', 'client_airtime_percentage'])
CLIENT_DISTRIBUTION = Info('wyebot_client_distribution', 'Client distribution details', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'band', 'total', 'percentage', 'mac_address', 'hostname', 'current_band', 'capability_band', 'category_id', 'vendor', 'ssid'])
NETWORK_TEST_PROFILES = Info('wyebot_network_test_profiles', 'Network test profiles', ['location_id', 'location_name', 'network_test_profile_id', 'network_test_profile_name', 'network_test_suite_id', 'network_test_suite_name', 'ssid', 'schedule_type_id', 'schedule', 'enabled', 'is_valid'])
NETWORK_TEST_RESULTS = Info('wyebot_network_test_results', 'Network test results', ['location_id', 'location_name', 'sensor_id', 'sensor_name', 'network_test_profile_id', 'network_test_profile_name', 'network_test_suite_id', 'network_test_suite_name', 'result_status_id', 'result_status_name', 'start_time', 'scheduled_time', 'execution_id'])

# Wyebot API details
BASE_URL = "https://wip.wyebot.com/external_api"
API_KEY = "your_api_key_here"

def get_locations():
    url = f"{BASE_URL}/org/get_locations"
    headers = {"api_key": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_sensors(location_id):
    url = f"{BASE_URL}/org/get_sensors"
    headers = {"api_key": API_KEY}
    data = {"location_id": location_id}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_sensor_info(sensor_id):
    url = f"{BASE_URL}/org/get_sensor_info"
    headers = {"api_key": API_KEY}
    data = {"sensor_id": sensor_id}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_sensor_network_info(sensor_id):
    url = f"{BASE_URL}/org/get_sensor_network_info"
    headers = {"api_key": API_KEY}
    data = {"sensor_id": sensor_id}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_access_point_details(location_id=None, sensor_id=None):
    url = f"{BASE_URL}/dashboard/accesspointlist"
    headers = {"api_key": API_KEY}
    data = {}
    if location_id:
        data["location_id"] = location_id
    if sensor_id:
        data["sensor_id"] = sensor_id
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_client_details(location_id=None, sensor_id=None):
    url = f"{BASE_URL}/dashboard/clientlist"
    headers = {"api_key": API_KEY}
    data = {}
    if location_id:
        data["location_id"] = location_id
    if sensor_id:
        data["sensor_id"] = sensor_id
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_ssid_details(location_id=None, sensor_id=None):
    url = f"{BASE_URL}/dashboard/ssidlist"
    headers = {"api_key": API_KEY}
    data = {}
    if location_id:
        data["location_id"] = location_id
    if sensor_id:
        data["sensor_id"] = sensor_id
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_issue_details(sensor_id):
    url = f"{BASE_URL}/dashboard/sensor_issues"
    headers = {"api_key": API_KEY}
    data = {"sensor_id": sensor_id}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_rf_analytics(location_id=None, sensor_id=None):
    url = f"{BASE_URL}/dashboard/rf_analytics"
    headers = {"api_key": API_KEY}
    data = {}
    if location_id:
        data["location_id"] = location_id
    if sensor_id:
        data["sensor_id"] = sensor_id
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_client_distribution(location_id=None, sensor_id=None):
    url = f"{BASE_URL}/dashboard/clientdistributionlist"
    headers = {"api_key": API_KEY}
    data = {}
    if location_id:
        data["location_id"] = location_id
    if sensor_id:
        data["sensor_id"] = sensor_id
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_network_test_profiles(location_id):
    url = f"{BASE_URL}/test/get_network_test_profiles"
    headers = {"api_key": API_KEY}
    data = {"location_id": location_id}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_network_test_results(location_id, network_test_profile_id, data_range_start_time, data_range_end_time):
    url = f"{BASE_URL}/test/get_network_test_results"
    headers = {"api_key": API_KEY}
    data = {
        "location_id": location_id,
        "network_test_profile_id": network_test_profile_id,
        "data_range_start_time": data_range_start_time,
        "data_range_end_time": data_range_end_time
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def collect_metrics():
    with REQUEST_TIME.time():
        try:
            locations = get_locations().get('location_details', {}).get('data', [])
            LOCATION_COUNT.set(len(locations))
            
            for location in locations:
                location_id = location['location_id']
                location_name = location['location_name']
                LOCATION_DETAILS.labels(location_id=str(location_id), location_name=location_name).info({})
                
                sensors = get_sensors(location_id).get('sensor_details', {}).get('data', [])
                SENSOR_COUNT.labels(location_id=str(location_id), location_name=location_name).set(len(sensors))
                
                for sensor in sensors:
                    sensor_id = sensor['sensor_id']
                    sensor_name = sensor['sensor_name']
                    SENSOR_DETAILS.labels(
                        location_id=str(location_id),
                        location_name=location_name,
                        sensor_id=str(sensor_id),
                        sensor_name=sensor_name
                    ).info({})
                    
                    sensor_info = get_sensor_info(sensor_id).get('sensor_info', {}).get('data', {})
                    hardware_details = sensor_info.get('hardware_details', {})
                    specification = hardware_details.get('specification', {})
                    service = hardware_details.get('service', {})
                    
                    SENSOR_DATA.labels(
                        location_id=str(location_id),
                        location_name=location_name,
                        sensor_id=str(sensor_id),
                        sensor_name=sensor_name,
                        model=specification.get('model', ''),
                        serial_number=specification.get('serial_number', ''),
                        wireless_mac_address=specification.get('wireless_mac_address', ''),
                        wired_mac_address=specification.get('wired_mac_address', ''),
                        link_speed=specification.get('link_speed', ''),
                        power_source=specification.get('power_source', ''),
                        uptime=service.get('uptime', ''),
                        software_version=service.get('software_version', ''),
                        license_info=service.get('license_info', '')
                    ).info({})
                    
                    sensor_network_info = get_sensor_network_info(sensor_id).get('sensor_network_info', {}).get('data', {})
                    
                    SENSOR_NETWORK_INFO.labels(
                        location_id=str(location_id),
                        location_name=location_name,
                        sensor_id=str(sensor_id),
                        sensor_name=sensor_name,
                        connection_type=sensor_network_info.get('connection_type', ''),
                        dhcp=str(sensor_network_info.get('dhcp', '')),
                        ipaddr=sensor_network_info.get('ipaddr', ''),
                        ip_subnet=sensor_network_info.get('ip_subnet', ''),
                        ip_gateway=sensor_network_info.get('ip_gateway', ''),
                        dns1=sensor_network_info.get('dns1', ''),
                        dns2=sensor_network_info.get('dns2', ''),
                        wireless_network=sensor_network_info.get('wireless_network', '')
                    ).info({})
                    
                    lldp_info = hardware_details.get('lldp_info', {}).get('lldp', {}).get('interface', {})
                    
                    for interface, lldp_data in lldp_info.items():
                        chassis = lldp_data.get('chassis', {}).get('sw01', {})
                        port = lldp_data.get('port', {})
                        auto_negotiation = port.get('auto-negotiation', {})
                        
                        SENSOR_LLDP_INFO.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            interface=interface,
                            via=lldp_data.get('via', ''),
                            age=lldp_data.get('age', ''),
                            vlan_id=lldp_data.get('vlan', {}).get('vlan-id', ''),
                            pvid=str(lldp_data.get('vlan', {}).get('pvid', '')),
                            chassis_capability=chassis.get('capability', {}).get('type', ''),
                            chassis_mgmt_ip=chassis.get('mgmt-ip', ''),
                            chassis_id=chassis.get('id', {}).get('value', ''),
                            chassis_descr=chassis.get('descr', ''),
                            port_descr=port.get('descr', ''),
                            port_id=port.get('id', {}).get('value', ''),
                            auto_negotiation_current=auto_negotiation.get('current', '')
                        ).info({})
                        
                    access_point_details = get_access_point_details(location_id=location_id, sensor_id=sensor_id).get('access_point_details', {}).get('data', [])
                    
                    for ap in access_point_details:
                        ACCESS_POINT_DETAILS.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            mac_address=ap.get('mac_address', ''),
                            hostname=ap.get('hostname', ''),
                            hostname_type_id=str(ap.get('hostname_type_id', '')),
                            channel=ap.get('channel', ''),
                            phy_type=ap.get('phy_type', ''),
                            max_data_rate=ap.get('max_data_rate', ''),
                            signal_strength=ap.get('signal_strength', ''),
                            vendor=ap.get('vendor', ''),
                            classification_type=str(ap.get('classification_type', ''))
                        ).info({})
                    
                    client_details = get_client_details(location_id=location_id, sensor_id=sensor_id).get('client_details', {}).get('data', [])
                    
                    for client in client_details:
                        CLIENT_DETAILS.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            mac_address=client.get('mac_address', ''),
                            hostname=client.get('hostname', ''),
                            ssid=client.get('ssid', ''),
                            bssid=client.get('bssid', ''),
                            vendor=client.get('vendor', ''),
                            phy_type=client.get('phy_type', ''),
                            band_name=client.get('band_name', ''),
                            channel=str(client.get('channel', ''))
                        ).info({})
                    
                    ssid_details = get_ssid_details(location_id=location_id, sensor_id=sensor_id).get('ssid_details', {}).get('data', [])
                    
                    for ssid in ssid_details:
                        for bssid in ssid.get('bssid_details_array', []):
                            SSID_DETAILS.labels(
                                location_id=str(location_id),
                                location_name=location_name,
                                sensor_id=str(sensor_id),
                                sensor_name=sensor_name,
                                ssid=ssid.get('ssid', ''),
                                total_bssids=str(ssid.get('total_bssids', '')),
                                security_name=ssid.get('security_name', ''),
                                hidden_ssid=str(ssid.get('hidden_ssid', '')),
                                bssid=bssid.get('bssid', ''),
                                hostname=bssid.get('hostname', ''),
                                hidden_bssid=str(bssid.get('hidden_bssid', '')),
                                total_clients=bssid.get('total_clients', ''),
                                channel=bssid.get('channel', ''),
                                signal_strength=str(bssid.get('signal_strength', ''))
                            ).info({})
                    
                    issue_details = get_issue_details(sensor_id).get('issue_details', {}).get('data', [])
                    
                    for issue in issue_details:
                        ISSUE_DETAILS.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            severity_name=issue.get('severity_name', ''),
                            problem=issue.get('problem', ''),
                            problem_description=issue.get('problem_description', ''),
                            solution=issue.get('solution', '')
                        ).info({})
                    
                    rf_analytics = get_rf_analytics(location_id=location_id, sensor_id=sensor_id).get('rf_details', {}).get('data', {})
                    
                    if isinstance(rf_analytics, list):
                        for rf in rf_analytics:
                            RF_ANALYTICS.labels(
                                location_id=str(location_id),
                                location_name=location_name,
                                sensor_id=str(rf.get('sensor_id', '')),
                                sensor_name=rf.get('sensor_name', ''),
                                radio_id='radio1',
                                channel=str(rf.get('channel_radio1', '')),
                                airtime_total_percent=str(rf.get('airtime_percent_radio1', '')),
                                mgmt_percent='',
                                ctrl_percent='',
                                data_percent='',
                                others_percent='',
                                available_percent='',
                                noise='',
                                client_mac_list='',
                                client_hostname_list='',
                                client_airtime_percentage=''
                            ).info({})
                            RF_ANALYTICS.labels(
                                location_id=str(location_id),
                                location_name=location_name,
                                sensor_id=str(rf.get('sensor_id', '')),
                                sensor_name=rf.get('sensor_name', ''),
                                radio_id='radio2',
                                channel=str(rf.get('channel_radio2', '')),
                                airtime_total_percent=str(rf.get('airtime_percent_radio2', '')),
                                mgmt_percent='',
                                ctrl_percent='',
                                data_percent='',
                                others_percent='',
                                available_percent='',
                                noise='',
                                client_mac_list='',
                                client_hostname_list='',
                                client_airtime_percentage=''
                            ).info({})
                    else:
                        for radio_id, rf in rf_analytics.items():
                            RF_ANALYTICS.labels(
                                location_id=str(location_id),
                                location_name=location_name,
                                sensor_id=str(sensor_id),
                                sensor_name=sensor_name,
                                radio_id=radio_id,
                                channel=str(rf.get('channel', '')),
                                airtime_total_percent=str(rf.get('airtime_total_percent', '')),
                                mgmt_percent=str(rf.get('mgmt_percent', '')),
                                ctrl_percent=str(rf.get('ctrl_percent', '')),
                                data_percent=str(rf.get('data_percent', '')),
                                others_percent=str(rf.get('others_percent', '')),
                                available_percent=str(rf.get('available_percent', '')),
                                noise=str(rf.get('noise', '')),
                                client_mac_list=','.join(rf.get('client_mac_list', [])),
                                client_hostname_list=','.join(rf.get('client_hostname_list', [])),
                                client_airtime_percentage=str(rf.get('client_airtime_percentage', ''))
                            ).info({})
                    
                    client_distribution = get_client_distribution(location_id=location_id, sensor_id=sensor_id).get('client_distribution_list', {}).get('band_usage_array', [])
                    client_distribution_data = get_client_distribution(location_id=location_id, sensor_id=sensor_id).get('client_distribution_list', {}).get('data', [])
                    
                    for dist in client_distribution:
                        CLIENT_DISTRIBUTION.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            band=dist.get('band', ''),
                            total=str(dist.get('total', '')),
                            percentage=dist.get('percentage', ''),
                            mac_address='',
                            hostname='',
                            current_band='',
                            capability_band='',
                            category_id='',
                            vendor='',
                            ssid=''
                        ).info({})
                        
                    for dist_data in client_distribution_data:
                        CLIENT_DISTRIBUTION.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            sensor_id=str(sensor_id),
                            sensor_name=sensor_name,
                            band='',
                            total='',
                            percentage='',
                            mac_address=dist_data.get('mac_address', ''),
                            hostname=dist_data.get('hostname', ''),
                            current_band=dist_data.get('current_band', ''),
                            capability_band=dist_data.get('capability_band', ''),
                            category_id=str(dist_data.get('category_id', '')),
                            vendor=dist_data.get('vendor', ''),
                            ssid=dist_data.get('ssid', '')
                        ).info({})
                    
                    network_test_profiles = get_network_test_profiles(location_id).get('network_test_profiles', {}).get('data', [])
                    
                    for profile in network_test_profiles:
                        NETWORK_TEST_PROFILES.labels(
                            location_id=str(location_id),
                            location_name=location_name,
                            network_test_profile_id=str(profile.get('network_test_profile_id', '')),
                            network_test_profile_name=profile.get('network_test_profile_name', ''),
                            network_test_suite_id=str(profile.get('network_test_suite_id', '')),
                            network_test_suite_name=profile.get('network_test_suite_name', ''),
                            ssid=profile.get('ssid', ''),
                            schedule_type_id=str(profile.get('schedule_type_id', '')),
                            schedule=profile.get('schedule', ''),
                            enabled=str(profile.get('enabled', '')),
                            is_valid=str(profile.get('is_valid', ''))
                        ).info({})
                    
                    for profile in network_test_profiles:
                        network_test_results = get_network_test_results(
                            location_id=location_id,
                            network_test_profile_id=profile.get('network_test_profile_id'),
                            data_range_start_time="2021-02-21 00:40:00",
                            data_range_end_time="2021-02-25 00:40:00"
                        ).get('network_test_results', {}).get('data', [])
                        
                        for result in network_test_results:
                            NETWORK_TEST_RESULTS.labels(
                                location_id=str(location_id),
                                location_name=location_name,
                                sensor_id=str(result.get('sensor_id', '')),
                                sensor_name=result.get('sensor_name', ''),
                                network_test_profile_id=str(profile.get('network_test_profile_id', '')),
                                network_test_profile_name=profile.get('network_test_profile_name', ''),
                                network_test_suite_id=str(result.get('network_test_suite_id', '')),
                                network_test_suite_name=result.get('network_test_suite_name', ''),
                                result_status_id=str(result.get('result_status_id', '')),
                                result_status_name=result.get('result_status_name', ''),
                                start_time=str(result.get('start_time', '')),
                                scheduled_time=result.get('scheduled_time', ''),
                                execution_id=str(result.get('execution_id', ''))
                            ).info({})
            
            logging.info("Metrics updated successfully")
        except Exception as e:
            logging.error(f"Error collecting metrics: {e}")

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    logging.info("Starting HTTP server on port 8000")
    # Continuously collect metrics every 60 seconds.
    while True:
        collect_metrics()
        time.sleep(60)
