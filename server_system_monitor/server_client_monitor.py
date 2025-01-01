import paramiko
import re
from typing import Self

class ServerClientMonitor:
    def __init__(self,client:paramiko.SSHClient):
    
        self._conn = client

    @staticmethod
    def from_user_password(hostname:str,password:str,username:str,port:int = 22)->Self:
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=hostname,password=password,username=username,port=port)

        return ServerClientMonitor(conn)
        
    def send_ram(self)->dict:
        """
        this method is a wrapper for the 'free' linux command
        """
        stdin , out, er = self._conn.exec_command("free")

        error = er.read().decode()

        if error:
            raise ConnectionError(error)
        
        lines = out.read().decode().splitlines()

        out.close(),er.close(),stdin.close()
        
        data_line = re.sub(r'\s+','+',lines[1])

        del lines,out,er,stdin

        data_line = data_line.replace("Mem:+","")
        data_sections = data_line.split("+")
        out = {
            "total":int(data_sections[0]),
            "used":int(data_sections[1]),
            "free":int(data_sections[2]),
            "shared":int(data_sections[3]),
            "buff/cache":int(data_sections[4]),
            "available":int(data_sections[5])
        }

        return out

    def __del__(self):
        self._conn.close()