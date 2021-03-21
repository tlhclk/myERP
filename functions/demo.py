# -*- coding: utf-8 -*-
import imaplib,sys,time
import serial.tools.list_ports as lp
from serial import Serial
from serial import serial_for_url
from serial.threaded import LineReader,ReaderThread


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')

    def handle_line(self, data):
        sys.stdout.write('line received: {}\n'.format(repr(data)))

    def connection_lost(self, exc):
        if exc:
            print(exc)
        sys.stdout.write('port closed\n')


class SerialListener:
    def __init__(self,p_name=None):
        if p_name == None:
            self.serial_port=None
        else:
            self.serial_port= Serial(p_name,9600)
    
    def listen_port(self,serial_port):
        while True:
            data=serial_port.read(8)
            print(data.decode("utf-8"))
            
    def get_data(self,serial_port):
        data=serial_port.read(8)
        return data.decode("utf-8").strip()
        
    def get_comport_list(self):
        comport_list=lp.comports()
        return comport_list
        
    def get_port(self):
        return self.get_comport_list()[0]
        
        
    def set_timeout(self,serial_port,time):
        serial_port.timeout=10
        
    def close_port(self,serial_port):
        serial_port.close()
    
    def demo(self):
        ser = serial_for_url('loop://', baudrate=9600, timeout=5)
        print("lol",ser.queue.__dict__)
        with ReaderThread(ser, PrintLines) as protocol:
            protocol.write_line('hello')
            time.sleep(2)