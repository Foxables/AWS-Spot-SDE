from datetime import datetime, timezone, timedelta
from time import time

def isTodayFridayOrSaturday() -> bool:
    return datetime.today().weekday() == 4 or datetime.today().weekday() == 5

def epoch() -> int:
    return int(time())

def strToDate(string) -> datetime:
    return datetime.strptime(string, '%Y-%m-%d')

def dateToStr(date) -> str:
    return date.strftime('%Y-%m-%d')

def todayAsAWST():
    return datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=timezone(timedelta(hours=8)))

def toHolidayDateFormat(date):
    return date.strftime('%Y%m%d')

def getExpirationTime():
    # 12AM on the first day of the next month.
    nextMonth = datetime.now().month+1
    year = datetime.now().year
    if nextMonth > 12:
        nextMonth = 1
        year += 1

    return int(datetime.now().replace(day=1, month=nextMonth, year=year, hour=0, minute=0, second=0).timestamp())
    
def remapDynamoResponse(dynamoResponse):
    result = []
    for i in range(dynamoResponse.__len__()):
        result.append(dynamoResponse[i]['InstanceId'])

    return result