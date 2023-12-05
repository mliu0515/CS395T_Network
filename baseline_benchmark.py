import os
import subprocess
# Workload genearing script:
'''
../wrk2/wrk -D exp -t 2 -c 100 -d 30s -L -s ./wrk2/scripts/social-network/compose-post.lua https://128.110.218.111:6443/wrk2-api/post/compose -R 1000
'''

# define some variables
t = 4
c = 200
d = 30
T = 1

home = ["read-home-timeline", "home-timeline/read"]
user = ["read-user-timeline", "home-timeline/read"]
compose = ["compose-post", "post/compose"]

# Function to run a command and return its output
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()  # Remove trailing newline
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None

def generate_report(t, c, d, R, cmd_lst):
    # Running the kubectl commands to get SVC_HOST and SVC_PORT
    SVC_HOST = run_command("kubectl get svc nginx-thrift -o jsonpath='{.spec.clusterIP}'")
    SVC_PORT = run_command("kubectl get svc nginx-thrift -o jsonpath='{.spec.ports[?(@.protocol==\"TCP\")].port}'")

    if SVC_HOST is not None and SVC_PORT is not None:
        # Constructing the SVC_URL and the final command
        SVC_URL = f"{SVC_HOST}:{SVC_PORT}"

        # print(f"request number: {R}")
        command = f"../wrk2/wrk -D exp -t {str(t)} -c {str(c)} -d {str(d)}s -L -s ./wrk2/scripts/social-network/{cmd_lst[0]}.lua http://{SVC_URL}/wrk2-api/{cmd_lst[1]} -R {str(R)}"
        print(command)
    
    # Run the command and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the command to complete
    stdout, stderr = process.communicate()

    # Check if the command was successful and get the output as a string
    if process.returncode == 0:
        output = stdout.decode()
    else:
        output = stderr.decode()

        

    with open(f"./no_retry_home_6_compose_10_user_3/{R}_{cmd_lst[0]}_output.txt", "w") as file:
        file.write(output)


for R in range(100, 1100, 100):
    for i in [compose, home, user]:
        generate_report(t, c, d, R, i)