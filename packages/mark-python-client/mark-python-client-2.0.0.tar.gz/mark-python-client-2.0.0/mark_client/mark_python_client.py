"""
Python version : 3.8.10
Mark_python_client script is instantiate a client which communicate
with the mark server and read or write data to the Mongo database
"""

from operator import itemgetter
import json
import time
import requests

class Record:
    """
    Data type representing Records
    """
    def __init__(self, id_record:int=None, label:str=None, time_record:float=None, subject:dict=None, data:any=None) -> None:
        self.id = id_record
        self.label = label
        self.time = time_record
        self.subject = subject
        self.data = data

    def set(self, values:dict):
        """
        Fill records with value in the dictionary
        """
        self.id = values["id"]
        self.label = values["label"]
        self.time = values["time"]
        self.subject = values["subject"]
        self.data = values["data"]

    def get(self)->dict:
        '''
        get the record as a dictionary
        '''
        return {'label': self.label,
                    'time': self.time,
                    'subject': self.subject,
                    'data': self.data,
                    'id': self.id}

class Evidence:
    '''
    Data type representing Evidences
    '''
    def __init__(self, id_evidence = None,
                 label = None,
                 time_evidence = None,
                 subject = None,
                 score = None,
                 report = None,
                 references = None, requests_evidence = None,
                 profile=None):
        self.id = id_evidence
        self.label = label
        self.time = time_evidence
        self.subject = subject
        self.score = score
        self.report = report
        self.references = references
        self.requests = requests_evidence
        self.profile = profile

    def set(self, values:dict):
        '''
        Fill records with value in the dictionary
        '''
        self.id = values['id']
        self.label = values['label']
        self.time = values['time']
        self.subject = values['subject']
        self.score = values['score']
        self.report = values['report']
        self.references = values['references']
        self.requests = values['requests']
        self.profile = values['profile']

    def get(self):
        '''
        get the evidence as a dictionary
        '''
        return {'id': self.id,
                     'label': self.label,
                     'time': self.time,
                     'subject': self.subject,
                     'score': self.score,
                     'report': self.report,
                     'references': self.references,
                     'requests': self.requests,
                     'profile': self.profile,
                     }

class MarkClient:
    """
    MarkClient is the python client for the MARk framework.
    It contains 36 methods to add or find evidences,
    data, detectors, file and so on ...
    """

    def __init__(self, server_url:str=None, verbose:bool=False, proxy:str=None, client_id:int=124):
        self.server_url = server_url
        self.verbose = verbose
        self.proxy = proxy
        self.client_id = client_id

    def set_server_url(self, server_url: str):
        '''
        Set URL of the mark server
        '''
        self.server_url = server_url

    def get_server_url(self)->str:
        '''
        Get URL set
        '''
        return self.server_url

    def set_verbose(self, is_verbose:bool):
        '''
        Set verbose option 
        '''
        self.verbose = is_verbose

    def get_verbose(self) -> bool:
        '''
        Get verbose option
        '''
        return self.verbose

    def set_proxy(self, proxy:str):
        '''
        Set the proxy for the requests
        '''
        self.proxy = proxy

    def get_proxy(self) -> str:
        '''
        Get the proxy used for the requests

        '''
        return self.proxy

    def post(self, parameters:list):
        '''
        Post request to the MARk server
        '''
        parameters["id"] = self.client_id
        response = requests.post(self.server_url, data=json.dumps(parameters), proxies=self.proxy)
        if self.verbose:
            print("-- Status of the "+parameters["method"]+" request:")
            print(f"-- {response.json()}")
        if 'result' in response.json():
            return response.json()['result']
        return None

    def test(self) -> str:
        '''
        Testing the server
        '''
        print("- Testing the server -")

        return self.post({"method":"test"})

    def post_test(self, data_string:str):
        """
        Test by sending it a string
        """
        print("- Sending a test string the server -")
        self.post({"method": "testString", 'params' : [data_string]})

    def set_agent_profile(self, profile):
        """
        Add or update the configuration a detector.
        If profile.label is already defined, the configuration is updated, *
        otherwise a new detector is added.
        :param profile: A profile, as a list of activated and configured detectors
        :return:
        """
        print("-- Setting the Agent Profile of the detectors --")
        self.post({'method' : 'setAgentProfile', 'params' : [profile]})

    def get_server_status(self):
        '''
        Get the status of the server
        '''
        print("- Get the status of the server")
        response_data = self.post({'method': 'status'})
        print("-- Current Active Jobs: " + str(response_data["executor.jobs.running"]))
        return response_data

    def add_evidence(self, evidence_data:Evidence):
        '''
        Adding Evidence Data to the server
        '''
        print("- Adding Evidence Data to the server")
        self.post({'method': 'addEvidence', 'params': [evidence_data.get()]})

    def find_last_evidences(self)->list:
        '''
        Fetching Last Evidences from to the server
        '''
        print("- Fetching Evidences from to the server")
        return self.post({'method': 'findLastEvidences'})

    def find_last_evidences_by_label(self, label:str, subject:dict)->list:
        '''
        Find the evidences according to a pattern (that start with provided pattern),
        and if multiple evidences are found with same label,
        return the most recent one.
        :param label: is a string
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :return: Evidence as a list
        '''
        print("-- Fetching Last evidence thanks "
              "to the label from the server --")
        return self.post({'method': 'findLastEvidences',
                          'params': [label, subject]})

    def find_evidences_by_label_in_page(self, label:str, page:int):
        """
        :param label: is a string
        :param page: is an integer, corresponding to a page of the memory
        :return: evidence as a list
        """
        print("-- Fetching Evidences thanks to the label in a page from the server --")
        return self.post({'method': 'findEvidence',
                      'params': [label,page]})


    def find_evidence_since_by_label_and_subject(self, label:str, subject: dict, time:float):
        """
        Find all evidences for a specific detector since a given date.
        :param label: is a string
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :param time: is a time, under the form of a long signed float
        :return: Evidence is returned as a list
        """
        print (f'Fetching Evidences from the server since {time}')
        return self.post({'method' : 'findEvidenceSince',
                      'params' : [label,subject,time]})

    def find_evidence_by_idfile(self, id_file):
        """
        Get a single evidence by id.
        :param id:
        :return: Evidence
        """
        print("--Fetching an evidence thanks to its id")
        return self.post({'method' : 'findEvidenceById',
                     'params' : [id_file]
                     })
    
    def find_evidence_for_period_and_interval(self, periode, interval):
        '''
        Find all evidences during a specific period, 
        response: information on how many evidences were produced by a specific agent for a given time.
        '''
        print("--Find all evidences during a specific period")
        return self.post({'method' : 'findEvidenceById',
                     'params' : [periode, interval]
                     })


    def add_raw_data(self, raw_data:Record):
        """
        A method to add raw data to the datastore and eventually trigger analysis.
        method : "addRawData"
        :param data: is a raw data, as a string
        :return:
        """
        print ("-- Adding raw data to the database --")
        self.post({'method': 'addRawData', 'params': [raw_data.get()]})

    def find_last_raw_data(self):
        """
        Send a get request to the server to obtain the last raw data in the server
        :return: a list containing the last raw data
        """
        print ("--finding the last raw data--")
        return self.post({'method':'findLastRawData'})

    def find_last_raw_data_interval(self, label:str, subject: dict, start:float, stop:float):
        """
        :param label: is a string, the name of the data we are looking for
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :param start: is a long signed float, corresponding to the strating time of the research
        :param stop: is a long signed float, corresponding
        to the ending time of the research
        :return: RawData as a list of raw data posted during the interval
        between the starting and the ending times
        """
        print(f'--Fetching Raw Data from the server between {start} and {stop} --')
        return self.post({'method': 'findRawData',
                      'params': [label, subject, start,stop]})

    def add_file(self, file_bytes, filename:str):
        """
        :param bytes: is a byte (under the form of a list ?)
        :param filename: is string
        :return: An object ID
        """
        print ("-- Adding file to the data base --")
        self.post({'method': 'addFile', 'params': [file_bytes,filename], })

    def find_file(self, file_id):
        """
        Send a request to the server to Find the last data records that were inserted in database
        :param file_id: is a ObjectID
        :return: a byte
        """
        print ("-- Looking in the server for the file with the ID : ")
        print(file_id + " --")
        return self.post({'method': 'findFile', 'id': file_id})

    def store_in_cache(self, key, value):
        """
        Store the value in the cache with the key.
        :param key:
        :param value:
        :return: Nothing
        """
        print(f'-- Storing the value {value} in the {key} cache --')
        self.post({'method': 'storeInCache',
                          'params': [key,value]})

    def get_from_cache(self, key):
        """
        get value from cache represented by a map.
        :param key: is a value corresponding to the cache we want data from
        :return: an object from the cache
        """
        print(f'-- Getting data from the {key} cache --')
        return self.post({'method' : 'getFromCache', 'params' : [key]})

    def remplace_in_cache(self, key, new_value, old_value):
        """
        Compare and swap verify if the current stored value in the cache is
        equals to old_value, or if the value has never been stored in the cache
        for this key. Since multiple agents can get access to the cache, We do
        this verification to not overwrite new values from other agents.

        :param key: is a string corresponding to the cache we want to work in
        :param new_value: is an object we want to put into the cache instead of the ancient one
        :param old_value:is an object we want to remplace by the new value
        :return:boolean
        """
        print(f'-- posting the new value {new_value} ' \
                   f'instead of the old value {old_value} ' \
                   f'in the {key} cache --')
        return self.post({'method' : 'compareAndSwapInCache',
                          'params' : [key,new_value,old_value]})

    def pause(self):
        """
        Pause execution (no algorithm will be scheduled).
        """
        self.post({'method': 'pause'})

    def resume(self):
        """
        Resume execution.
        :return:
        """
        self.post({'method': 'resume'})

    def reload(self):
        """
        Reload the directory containing detection agents profiles.
        :return:
        """
        self.post({'method': 'reload' })

    def restart(self):
        """
        A method to restart the server analysis
        Dangerous! Restart the server: wipe the DB and restart the data agents.
        :return:
        """
        self.post({'method': 'restart', })

    def history(self):
        """
        Get the last previous status objects.
        :return: the history of the actions on the server as a list
        """
        return self.post({'method':'history'})

    def get_ranked_list(self, label):
        '''
        Fetching Evidence Ranked List from the server
        '''
        print("- Fetching Evidence Ranked List from the server")
        result_data = []
        result_data = self.post({'method': 'findEvidence', 'params': [label]})
        # sort the fetched data in descending order (highest score at the top)
        sorted_result_data = sorted(result_data, key=itemgetter('score'), reverse=True)
        return sorted_result_data

    def get_unique_subject_count(self, subject:dict):
        '''
        Fetching count of unique subjects in Evidences
        '''
        print("- Fetching count of unique subjects in Evidences")
        return self.post({'method': 'findUniqueSubjects',
                                  'params': [subject]})

    def get_distinct_entries_for_field(self, field):
        '''
        Fetching unique entries for given field
        '''
        print("- Fetching unique entries for given field")
        return self.post({'method': 'findDistinctEntries',
                                  'params': [field]})

    def get_detectors_activated(self):
        '''
        Fetching unique evidence labels
        '''
        print("- Fetching unique evidence labels")
        unique_labels = []
        response_data = self.post({'method': 'activation'})
        for item in response_data:
            unique_labels.append(item["label"])
        return unique_labels

    def sources(self):
        """
        Get the configuration of data sources.
        :return: DataAgentProfile as a list
        """
        print("-- Getting the configuration of data sources:")
        return self.post({'method' : 'sources'})

""" if __name__ == "__main__":
    import inspect
    import ast
    client = MarkClient(server_url="http://127.0.0.1:8080", verbose=True)
    # functions = [client.test, client.post_test, client.set_agent_profile, client.get_server_status, client.add_evidence, client.find_evidence_since_by_label_and_subject, client.find_evidence_by_idfile, client.add_raw_data, client.find_last_raw_data, client.find_last_raw_data_interval, client.add_file, client.find_file, client.store_in_cache, client.get_from_cache, client.remplace_in_cache, client.pause, client.resume, client.reload, client.restart, client.history, client.get_ranked_list, client.get_unique_subject_count, client.get_distinct_entries_for_field, client.get_detectors_activated, client.sources]
    functions = [client.test, client.post_test, client.get_server_status, client.find_evidence_since_by_label_and_subject, client.find_evidence_by_idfile, client.find_last_raw_data, client.find_last_raw_data_interval, client.find_file, client.pause, client.resume, client.reload, client.restart, client.history, client.get_ranked_list, client.get_unique_subject_count, client.get_distinct_entries_for_field, client.get_detectors_activated, client.sources, client.add_raw_data]
    FUNCINFO = "\n".join([f"{i}: {f.__name__} - args: {inspect.getfullargspec(f).args[1:]}" for i, f in enumerate(functions)])
    info = f'''x: quit
v: toggle verbose
s: set server
h: help
{FUNCINFO}
-------------
'''
    print(info)
    while True:
        command = input("command: ")
        if command == 'x':
            break
        elif command == 'v':
            client.set_verbose(not client.get_verbose())
            print(f"\tverbose set to {client.get_verbose()}")
        elif command == 's':
            url = input("\turl: ")
            client.set_server_url(url)
        elif command == 'h':
            print(info)
        else:
            if command.isdecimal():
                func = functions[int(command)]
                argsInfo = inspect.getfullargspec(func)
                args = ()
                for a in  argsInfo.args:
                    if a == 'self':
                        continue
                    annotation = argsInfo.annotations.get(a, "str")
                    if annotation == float:
                        args += (float(input(f"\t{a} -- {annotation}: ")),)
                    elif annotation == dict:
                        print("no")
                        args += (ast.literal_eval(input(f"\t{a} -- {annotation}: ")),)
                    elif annotation == Record:
                        args += (Record(int(input("id: ")), input("label: "), time.time(), {"name": input("subjectName: ")}, input("data: ")), )
                    else:
                        args += (input(f"\t{a} -- {annotation}: "),)

                print(args)
                func(*args)
 """