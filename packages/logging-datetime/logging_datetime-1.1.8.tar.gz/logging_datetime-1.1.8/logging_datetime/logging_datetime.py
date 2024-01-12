import re
import os
import pytz
import shutil
from pathlib import Path
from datetime import datetime

prev_hour = None
prev_day = None

def datetime_format():
    '''
    Extract daterime now to get year month day hour minute second and microsecond now
    '''
    datetime_now    = datetime.now(ist)
    year            = str(datetime_now.year)
    month           = '0'+str(datetime_now.month) if len(str(datetime_now.month)) == 1 else str(datetime_now.month)
    day             = '0'+str(datetime_now.day) if len(str(datetime_now.day)) == 1 else str(datetime_now.day)
    hour            = '0'+str(datetime_now.hour) if len(str(datetime_now.hour)) == 1 else str(datetime_now.hour)
    minute          = '0'+str(datetime_now.minute) if len(str(datetime_now.minute)) == 1 else str(datetime_now.minute)
    second          = '0'+str(datetime_now.second) if len(str(datetime_now.second)) == 1 else str(datetime_now.second)
    microsecond     = '0'+str(datetime_now.microsecond) if len(str(datetime_now.microsecond)) == 1 else str(datetime_now.microsecond)
    return year, month, day, hour, minute, second, microsecond

def asctime():
    '''
    Get asctime for message log
    '''
    year, month, day, hour, minute, second, microsecond = datetime_format()
    return f'{year}-{month}-{day} {hour}:{minute}:{second},{str(microsecond)[:3]}'

def get_path_log():
    '''
    Set path log in path logging/yaer/month/day/log_name.log
    '''
    year, month, day, hour, _, _, _ = datetime_format()
    path_name = f'{dir_log}/{year}/{month}/{day}'
    Path(path_name).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging_{hour}, {day}-{month}-{year}.log'
    log_file_full_name = os.path.join(path_name, log_filename)
    return log_file_full_name

def get_path_log_new():
    Path(dir_log).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging.log'
    log_file_full_name = os.path.join(dir_log, log_filename)
    return log_file_full_name

def check_and_move(prev_hour=None):
    year, month, day, _, _, _, _ = datetime_format()
    path_name = f'{dir_log}/{year}/{month}/{day}'
    Path(path_name).mkdir(parents=True, exist_ok=True)
    log_filename = f'logging_{prev_hour}, {prev_day}-{month}-{year}.log'
    log_file_new = os.path.join(path_name, log_filename)
    log_file_old = os.path.join(dir_log, 'logging.log')
    shutil.move(log_file_old, log_file_new)


class SetupLogger:
    '''
        Dinamic Logging set as datetime directory
        Args:
            directory_log(str)  : root directory log
            print_log(boolean)  : print or skip print log
    '''
    def __init__(self, directory_log: str='./', time_zone: str='Asia/Jakarta'):
        global ist; ist = pytz.timezone(time_zone)
        global dir_log; dir_log = directory_log
        self.dir_log  = directory_log
        self.check_logging()
        
    @staticmethod    
    def get_last_log_date(log_file_path):
        try:
            with open(log_file_path, 'r') as log_file:
                # Read the last line of the file
                lines = log_file.readlines()
                last_line = lines[-5:]
                for i in range(len(last_line), 0, -1):
                    regex_datetime = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})', last_line[i-1])
                    if regex_datetime:
                        # Extract the date from the last line
                        date_str = last_line[i-1].split(' | ')[0]
                        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S,%f')
        except Exception as e:
            print(f"Error reading log file: {e}")
        return None
        
    def check_logging(self):
        log_file_path = f'{self.dir_log}/logging.log'

        last_date = self.get_last_log_date(log_file_path)
        if last_date:
            if not int(last_date.day) == int(datetime_format()[2]):
                try:
                    os.remove(log_file_path)
                except: pass
    
class logging:
    
    '''
    Add class method for level log : info error and debug
    '''
    @classmethod
    def info(self, msg):
        self.__write_log(self, msg, level='INFO')
    @classmethod    
    def error(self, msg):
        self.__write_log(self, msg, level='ERROR')
    @classmethod
    def debug(self, msg):
        self.__write_log(self, msg, level='DEBUG')

    def __write_log(self, message, level):
        '''
        Write text log in path log
        '''
        global prev_day, prev_hour

        if not prev_day: prev_day = datetime_format()[2]
        if not prev_hour: prev_hour = datetime_format()[3]
        path_log = get_path_log()
        log_file = open(path_log, 'a+')
        text = f'{asctime()} | {level} : {message}'
        log_file.write(f'{text} \n')
        print(text)
        log_file.close()
    
        path_log = get_path_log_new()
        if not prev_day == datetime_format()[2]:
            try:
                os.remove(path_log)
            except: pass
        log_file = open(path_log, 'a+')
        text = f'{asctime()} | {level} : {message}'
        log_file.write(f'{text} \n')
        log_file.close()