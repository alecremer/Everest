import subprocess
import os
import signal
from threading import Thread
import time
class ProcessID():

    process = None
    id = None

    def __init__(self, process, id):

        self.process = process
        self.id = id


class RosManager():

    def __init__(self):

        self.process_list = []

    def get_topics(self):
        result_bytes = subprocess.run(["ros2 topic list"], stdout=subprocess.PIPE, shell=True)
        result_str = result_bytes.stdout.decode("UTF8")
        result_splitted = result_str.split('\n')
        return result_splitted
    
    def pub_bool(self, topic, value, continuos, publisher_id):
        if continuos:

            process_running = False
            # stop if started
            for process in self.process_list:
                if process.id == publisher_id:
                    self.process_list.remove(process)
                    print(self.process_list)
                    print("Join")
                    process.process.join()
                    print("Jointed")
                    process_running = True
                    print("STOP pub continuous")

            if not process_running:
                self.pub_bool_continuous(topic, value, publisher_id)
        
        else:
            self.pub_bool_once(topic, value)
    
    def _pub_continuous_routine(self, topic, value, publisher_id, sleep_time):

        publisher_on = True

        while publisher_on:
            print(f"list: {self.process_list}")
            print(f"publisher id: {publisher_id}")
            
            publisher_on = False
            # only continue if publisher has in list
            for process in self.process_list:
                if process.id == publisher_id:
                    publisher_on = True

            self.pub_bool_once(topic, value)
            time.sleep(sleep_time)
            


    def pub_bool_once(self, topic, value):
        print("pub once")
        result_bytes = subprocess.run([f"ros2 topic pub {topic} std_msgs/msg/Bool \"{{data: {value}}}\" -1"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    def pub_timeout_bool(self, topic, value):
        result_bytes = subprocess.run([f"timeout 3s ros2 topic pub {topic} std_msgs/msg/Bool \"{{data: {value}}}\""], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        
    def pub_bool_continuous(self, topic, value, publisher_id):
        print("start pub continuous")
        process = Thread(target= lambda : self._pub_continuous_routine(topic, value, publisher_id, 0.1))
        self.process_list.append(ProcessID(process, publisher_id))
        process.start()

