import numpy as np
from datetime import datetime, timedelta
import time

def main():
    while True:
        print(calculate(3600000, 10, 15, 9, 18))
        time.sleep(1)


def calculate(wage, the_day, start, end):
    # 저번 달 정산일 다음날 부터 이번 달 정산일까지의 날 수를 구한다.
    my_wage = ''
    now = datetime.today()
    if now.day < the_day:
            prev_month = now.replace(day=1) - timedelta(days=1)
            prev_month = prev_month.month
            next_month = now.month
    elif now.day - the_day == 0:
        if now.hour - end < 0:
            prev_month = now.replace(day=1) - timedelta(days=1)
            prev_month = prev_month.month
            next_month = now.month
        else:
            prev_month = now.month
            next_month = now.month + 1
    else:
        prev_month = now.month
        next_month = now.month + 1

    
    work_start = datetime.strptime(f'{now.year}/{now.month}/{now.day}/{start:02d}', '%Y/%m/%d/%H')
    a = f'{now.year}-{prev_month:02d}-{the_day:02d}' # 이전 정산일
    b = f'{now.year}-{next_month:02d}-{the_day:02d}' # 다음 정산일    

    if end < start:
        working_time = (24 - start) + end
        total_sec_per_day = working_time * 3600 # 총 일하는 시간 -> 초 단위
        total = (np.busday_count(a,b)+1) * total_sec_per_day

        if now.day == the_day and now.hour >= end and now.hour < start:
            # paid_time = datetime.strptime(f'{now.year}/{now.month}/{now.day}/{end}', '%Y/%m/%d/%H')
            # until_now = (now - paid_time).total_seconds()
            percentage = 1
            my_wage = format(int(percentage * wage), ',')

        elif now.weekday() != 6: # 토요일 넘어가는 새벽까지 일할 수 있으므로
            until_now = 0
            if now.hour >= start:
                until_now = np.busday_count(a, datetime.strftime(now, '%Y-%m-%d'), weekmask=[1,1,1,1,1,1,0]) * total_sec_per_day + (now - work_start).total_seconds()
            elif now.hour < end:
                work_start = datetime.strptime(f'{now.year}/{now.month}/{now.day - 1}/{start:02d}', '%Y/%m/%d/%H') # 하루 지남. 어제 일 시작했으니 now.day - 1
                until_now = (np.busday_count(a, datetime.strftime(now, '%Y-%m-%d'), weekmask=[1,1,1,1,1,1,0])-1) * total_sec_per_day + (now - work_start).total_seconds()
            else:
                until_now = (np.busday_count(a, datetime.strftime(now, '%Y-%m-%d'), weekmask=[1,1,1,1,1,1,0])) * total_sec_per_day
            percentage = until_now / total
            my_wage = format(int(percentage * wage), ',')

        else:
            until_now = ((np.busday_count(a, datetime.strftime(now, '%Y-%m-%d'))))* total_sec_per_day
            percentage = until_now / total
            my_wage = format(int(percentage * wage), ',')

    else:
        working_time = end-start
        total_sec_per_day = working_time * 3600 # 총 일하는 시간 -> 초 단위
        total = (np.busday_count(a,b)+1) * total_sec_per_day

        if now.day == the_day and now.hour >= end:
            # paid_time = datetime.strptime(f'{now.year}/{now.month}/{now.day}/{end}', '%Y/%m/%d/%H')
            # until_now = (now - paid_time).total_seconds()
            percentage = 1
            my_wage = format(int(percentage * wage), ',')

        elif now.weekday() not in [5,6] and now.hour >= start and now.hour < end:
            until_now = ((np.busday_count(a, datetime.strftime(now, '%Y-%m-%d')))) * total_sec_per_day + (now - work_start).total_seconds()
            percentage = until_now / total
            my_wage = format(int(percentage * wage), ',')

        else:
            until_now = ((np.busday_count(a, datetime.strftime(now, '%Y-%m-%d'))))* total_sec_per_day
            percentage = until_now / total
            my_wage = format(int(percentage * wage), ',')

    return my_wage

if __name__ == "__main__":
    main()