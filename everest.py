import subprocess
import os
import signal

class RosManager():

    def get_topics(self):
        result_bytes = subprocess.run(["ros2 topic list"], stdout=subprocess.PIPE, shell=True)
        result_str = result_bytes.stdout.decode("UTF8")
        result_splitted = result_str.split('\n')
        return result_splitted
    
    def pub_bool(self, topic, value):
        print(f"topic: {topic}, value: {value}")
        result_bytes = subprocess.run([f"ros2 topic pub {topic} std_msgs/msg/Bool \"{{data: {value}}}\" -1"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


    def pub_timeout_bool(self, topic, value):
        result_bytes = subprocess.run([f"timeout 3s ros2 topic pub {topic} std_msgs/msg/Bool \"{{data: {value}}}\""], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        
