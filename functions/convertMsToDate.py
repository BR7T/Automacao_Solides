from datetime import datetime

def timeConvert(ms):
    dt = datetime.fromtimestamp(ms / 1000.0)
    return dt
    