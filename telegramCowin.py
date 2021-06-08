import requests
from datetime import datetime
import time
import schedule

base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
base_api_url = "https://api.telegram.org/bot1835777786:AAGHoF0KQn38yoMouXZZhGboVvRGo5cMkcs/sendMessage?chat_id=@_grpID_&text="
group_id = "cowinalert935"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")


def fetch_data(district_id):

    params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = base_url+params
    
    response = requests.get(final_url, headers=headers)
    filter_data(response)
    # print(response.text)


def filter_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        message=""
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
                message += "Pincode: {} \nName: {} \nSlots: {} \nMinimum Age: {} \nDate: {} \nVaccine: {} \nFee Type: {} \n ------- \n".format(
                    center["pincode"], center["name"], session["available_capacity_dose1"],
                    session["min_age_limit"],session["date"],session["vaccine"],center["fee_type"])
        # print(message)    
        send_message(message)


def send_message(message):
    final_api_url = base_api_url.replace("_grpID_",group_id)
    final_api_url = final_api_url+message
    response = requests.get(final_api_url, headers=headers)
    print(response)



schedule.every(10).seconds.do(lambda: fetch_data(512))
while True:
    schedule.run_pending()
    time.sleep(1)

