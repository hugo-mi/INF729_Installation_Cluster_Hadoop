#Programme LAUNCH.py


#START: python3 LAUNCH.py start
#STOP: python3 LAUNCH.py stop
import sys
import subprocess
import threading
import time

def cmdsh(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        return False
    else:
        return True
    
def mt(list_m, fct, *args ):
    threads = []
    for i in list_m:
        x = threading.Thread(target = fct, args = (i, *args))
        threads.append(x)
        x.start()

    for x in threads:
        x.join()

def start_zoo(mach):
    cmd = "ssh "+mach+" /home/ubuntu/zookeeper/bin/zkServer.sh start"
    cmdsh(cmd)
        
def stop_zoo(mach):
    cmd = "ssh "+mach+" /home/ubuntu/zookeeper/bin/zkServer.sh stop "
    cmdsh(cmd)     
    
def start_hbase(mach):
    cmd = "ssh "+mach+" /home/ubuntu/hbase/bin/start-hbase.sh"
    cmdsh(cmd)  
    
def stop_hbase(mach):
    cmd = "ssh "+mach+" /home/ubuntu/hbase/bin/stop-hbase.sh"
    cmdsh(cmd) 
    
def start_spark(mach):
    cmd = "ssh "+mach+" /home/ubuntu/spark/bin/spark-shell && exit"
    cmdsh(cmd) 

def main():
    f = open('/home/ubuntu/HOSTS.txt', 'r')
    hosts = [line.strip() for line in f]
    f.close()
    cmdsh("source .bashrc")
    
    if sys.argv[1] == 'start':
        cmd = "/home/ubuntu/hadoop/sbin/start-all.sh"
        cmdsh(cmd)
        time.sleep(10)
        cmdsh("/home/ubuntu/zookeeper/bin/zkServer.sh start")
        mt(hosts, start_zoo)
        cmdsh("/home/ubuntu/hbase/bin/start-hbase.sh")
        mt(hosts, start_hbase)
        cmdsh("/home/ubuntu/spark/bin/spark-shell && exit")
        mt(hosts, start_spark)
        print('SWITH ON')
        
    if sys.argv[1] == 'stop':
        cmd = "/home/ubuntu/hadoop/sbin/stop-all.sh"
        cmdsh(cmd)
        time.sleep(10)
        cmdsh("/home/ubuntu/zookeeper/bin/zkServer.sh stop")
        mt(hosts, stop_zoo)
        cmdsh("/home/ubuntu/hbase/bin/stop-hbase.sh")
        mt(hosts, stop_hbase)
        print('SWITH OFF')        
    
    elif sys.argv[1] == 'stop':
        cmd = "/home/ubuntu/hadoop/sbin/stop-all.sh"
        cmdsh(cmd)
        
if __name__ == '__main__':
    main()
