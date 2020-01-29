#k is cust_id and v is dict of{loan"contact_no": row[1],"disbursal_date": row[2],"loan_amount": row[3],"paid_status": row[4]}
from datetime import datetime, date, timedelta
import requests
import json
import csv
# from . import sms
emi_amount_1 = lambda loan_amt: int(loan_amt) * .80
emi_amount_2 = lambda loan_amt: int(loan_amt) * .20
base_penalty = 50
charge_per_day = .01
interest = 12
path_message = r'/home/credicxo/credicxo-project/'


def penalty_1(total_day, loan):
    loan = int(loan)
    return int((total_day - 15) * (charge_per_day * emi_amount_1(loan)) + base_penalty)


def penalty_2(total_day, loan):
    loan = int(loan)

    return int((total_day - 61) * (charge_per_day * emi_amount_1(loan)) + base_penalty)


def generate_text(v,users_name,ref_dict,bank_dict):
    #ref_dict is dictionary of reference_name and reference_number fbank_dict is dictionary of bank_account_number
    text = None
    msg_number = str(v["contact_no"])
    name_dict = users_name
    date_format = "%Y-%m-%d"
    today = datetime.strptime(str(date.today()), date_format)
    entry_in = []

    loan_amt = v["loan_amount"]
    loan_date = datetime.strptime(str(v["disbursal_date"]), date_format)
    delta = today - loan_date
    # temp = today - timedelta(days = 14)
    # delta = today - temp
    # print(delta.days)
    # print("=====================")

    if v["paid_status"] == '0':

        msg_number = str(v["contact_no"])
        if delta.days in [10, 11, 12, 13]:
            entry_in.append("EMI1_10-13")
            text = f'Dear {name_dict}, your 1st EMI repayment schedule date is on {str((loan_date + timedelta(days=15)).date())}. Please repay on time to avoid any penalty charges.'
        elif delta.days == 14:
            entry_in.append("EMI1_14")
            text = f"Dear {name_dict}, your 1st EMI loan repayment date is tomorrow. Please repay on time to avoid any penalty charges and to maintain a good credit score."
        elif delta.days == 15:
            entry_in.append("EMI1_15")
            text = f"Dear {name_dict}, today is the last day of your 1st EMI payment. Please make the payment today {today.strftime('%Y-%m-%d')} before 4 pm to avoid incurring any additional charge and to maintain a good credit score."
        elif delta.days in range(16, 26):
            entry_in.append("EMI1_16-25")
            penalty_now = penalty_1(delta.days, v["loan_amount"])
            text = f'Dear {name_dict}, you have exceeded your 1st EMI loan repayment by {str(delta.days - 15)} days. You have been charged with Rs {str(penalty_now)} as a penalty and the new amount to be paid is Rs {str(emi_amount_1(loan_amt) + interest + penalty_now)}. Please make the payment today {str(today.strftime("%Y-%m-%d"))} before 4 pm to avoid incurring any additional charge otherwise it will affect your credit score.'
        elif delta.days in range(26, 31):
            entry_in.append("EMI1_26-30")
            penalty_now = penalty_1(delta.days, v["loan_amount"])
            text = f'LEGAL NOTICE ALERT - Dear {name_dict}, this is to inform you that your 1st EMI amount of Rs {str(int(emi_amount_1(loan_amt)) + interest + penalty_now)} (with penalty of Rs {str(penalty_now)} included) is overdue since {str((loan_date + timedelta(days=15)).date())}. Hence, we request you to make the payment on priority. In case it is not done, you may receive a Legal Notice from us and we may initiate Legal Proceedings on your contract as per policy. Please ignore if already paid.'
        elif delta.days in range(31, 36):
            entry_in.append("EMI1_31-35")
            penalty_now = penalty_1(delta.days, v["loan_amount"])
            text = f'Dear {name_dict}, despite several reminders, re-payment of 1st EMI of Rs {str(int(emi_amount_1(loan_amt)) + interest + penalty_now)} (with penalty of Rs {str(penalty_now)} included) is still not received and it is over-due since {str((loan_date + timedelta(days=15)).date())}. Request you to make the due payment immediately, failing which your credit history will be impacted. Also, your reference contacts will be used to recover the amount if payment not made by today 4 pm.'
        elif delta.days in range(36, 46, 2):
            entry_in.append("EMI1_36-45")
            penalty_now = penalty_1(delta.days, v["loan_amount"])
            #cust_ref(k)
            msg_number = str(ref_dict['ref_number'][0])
            print(msg_number)
            text = f'Dear Sir/Mam, This is to inform you that {name_dict} (Phone number - {v["contact_no"]}) has  taken a loan from Credicxo and has not repaid since {str(str((loan_date + timedelta(days=15)).date()))}.As you are listed as a reference in the Loan application,kindly urge them to repay the loan to avoid legal proceedings.'

        elif delta.days in range(56, 61, 2):
            entry_in.append("EMI1_56-60")
            text = f'Dear {name_dict} your loan is overdue on Credicxo. If there is no payment today, your CIBIL score will be lowered and you will be listed as a defaulter. Your reference contacts will be sent a copy of the legal notice. Kindly pay through https://play.google.com/store/apps/details?id=com.credicxo.loan.personal'

        elif delta.days in range(61, 65, 2):
            entry_in.append("EMI1_61-64")
            text = f'Dear {name_dict}, This is the Final Warning to repay the pending EMI on Credicxo. Under Breach of Trust & Section 420 IPC, a case has been registered under your name. Copy of the Notice already dispatched from Indian Post Service. Kindly pay through https://play.google.com/store/apps/details?id=com.credicxo.loan.personal'

        elif delta.days in range(65, 71, 2):
            entry_in.append("EMI1_65-70")
            #bank_acc(k)
            text = f'Dear {name_dict}, The Honourable Court has issued a summons for your appearance in a criminal case filed by Credicxo Tech Pvt. Ltd. for the dishonour of Personal Loan a/c ending with {str(bank_dict["account_number"])[-4:]}. Non-appearance may lead to the issuance of a warrant. Kindly pay through https://play.google.com/store/apps/details?id=com.credicxo.loan.personal'

        else:
            print(delta.days, "th day is not handeled for emi 1")
            #continue

    elif v["paid_status"] == '1':

        msg_number = str(v["contact_no"])
        if delta.days in range(56, 60):
            entry_in.append("EMI2_56-59")
            text = f'Dear {name_dict}, your 2nd EMI repayment schedule date is on {str((loan_date + timedelta(days=61)).date())}. Please repay on time to avoid any penalty charges.'
        elif delta.days == 60:
            entry_in.append("EMI2_60")
            text = f'Dear {name_dict}, your 2nd EMI loan repayment date is tomorrow. Please repay on time to avoid any penalty charges and to maintain a good credit score.'
        elif delta.days == 61:
            entry_in.append("EMI2_61")
            text = f'Dear {name_dict}, today is the last day of your 2nd EMI payment. Please make the payment today {today.strftime("%Y-%m-%d")} before 4 pm to avoid incurring any additional charge and to maintain a good credit score.'
        elif delta.days in range(62, 71):
            entry_in.append("EMI2_62-70")
            penalty_now = penalty_2(delta.days, v["loan_amount"])
            text = f'Dear {name_dict}, you have exceeded your 2nd EMI loan repayment by {str(delta.days - 61)} days. You have been charged with Rs {str(penalty_now)} as a penalty and the new amount to be paid is {str(int(emi_amount_2(loan_amt)) + interest + penalty_now)}. Please make the payment today {today.strftime("%Y-%m-%d")} before 4 pm to avoid incurring any additional charge otherwise it will affect your credit score.'
        elif delta.days in range(71, 76):
            entry_in.append("EMI2_71-75")
            penalty_now = penalty_2(delta.days, v["loan_amount"])
            text = f'LEGAL NOTICE ALERT - Dear {name_dict}, this is to inform you that your 2nd EMI amount of {str(int(emi_amount_2(loan_amt)) + interest + penalty_now)} is overdue since {str(delta.days - 61)}. Hence, we request you to make the payment on priority. In case it is not done, you may receive a Legal Notice from us and we may initiate Legal Proceedings on your contract as per policy. Please ignore if already paid.'
        elif delta.days in range(76, 82, 2):
            entry_in.append("EMI2_76-81")
            penalty_now = penalty_2(delta.days, v["loan_amount"])
            text = f'Dear {name_dict}, despite several reminders, re-payment of 2nd EMI {str(int(emi_amount_2(loan_amt)) + interest + penalty_now)}  is still not received and it is over-due by {str(delta.days - 61)} days. Request you to make the due payment immediately, failing which your credit history will be impacted. Also, your reference contacts will be used to recover the amount if payment not made by today 4 pm.'

        elif delta.days in range(82, 91, 2):
            entry_in.append("EMI2_82-91")
            text = f'Dear {name_dict} your loan is overdue on Credicxo. If there is no payment today, your CIBIL score will be lowered and you will be listed as a defaulter. Your reference contacts will be sent a copy of the legal notice. Kindly pay through https://play.google.com/store/apps/details?id=com.credicxo.loan.personal'

        else:
            print(delta.days, "th day is not handeled for emi 2")
    return [text, msg_number, entry_in]


#generate_text(v, users_name, ref_dict, bank_dict)
def api_call(text,msg_number):
    API = "https://api.equence.in/pushsms"

    headers = {
        "content-type": "application/json",
        "accept": "application/json",
    }

    data = {
        "username": "credicxo_tr",
        "password": "zzCD-43-",
        "to": "91" + msg_number,
        "from": "CREDXO",
        "text": text,
    }
    response = requests.get(url=API, params=data)
    sequence_url = json.loads(response.text)
    # sequence_url = {'response': [{'destination': '919968038609', 'id': 0, 'mrid': '8001291303196552321', 'segment': 0,
    #                               'status': 'success'}]}
    return sequence_url


def write_in_csv(sequence_url, msg_number, entry_in, user_id_det, con_name):
    date_format = "%Y-%m-%d"
    today = datetime.strptime(str(date.today()), date_format)
    csv1_fields = ["id", "Detail", "Phone_number", "Msg_status", "Date", "Time"]
    csv1_rows = []

    # if str(sequence_url["response"][0]["status"]) == "success":
    #     sms.csv2_dict[entry_in[0]] += 1
    #     sms.csv2_dict["total_msg"] += 1


    csv1_rows.append({
        "id": user_id_det,
        "Detail": con_name,
        "Phone_number": str(msg_number),
        "Msg_status": str(sequence_url["response"][0]["status"]),
        "Date": str(today.date()),
        "Time": str((datetime.now() + timedelta(hours=5, minutes=30)).strftime('%H:%M:%S'))
    })
    with open(path_message + 'day_' + str(today.date()) + '.csv', 'a') as csvfile1:
        writer = csv.DictWriter(csvfile1, fieldnames=csv1_fields)
        if csvfile1.tell() == 0:
            writer.writeheader()

        writer.writerows(csv1_rows)


def send_message(d):
    x = d['paid_status']
    v = {}
    ref_dict = {}
    bank_dict = {}
    v['contact_no'] = d['contact_no']
    v['loan_amount'] = d['loan_amount']
    v['paid_status'] = x #d['paid_status'][0],
    v['disbursal_date'] = d['disbursal_date']
    user_id_detail = d['user_id']
    users_name = d['users_name']
    ref_dict['ref_number'] = d['ref_number'],
    ref_dict['ref_name']= d["ref_name"]
    bank_dict['account_number'] = d["account_number"]
    text, msg_number, entry_in = generate_text(v, users_name, ref_dict, bank_dict)
    con_numb = v['contact_no']
    if msg_number == str(con_numb):
        con_name = 'contact_no'
    else:
        con_name = 'preference_number'
    if text != None:
        sequence_url = api_call(text, msg_number)
        print(sequence_url)
        write_in_csv(sequence_url, msg_number, entry_in, user_id_detail, con_name)
    else:
        print('null')


data = {
    "users_name": 'aman',
    "contact_no": 9267988656,
    "account_number": 123456789,
    "ref_name": 'vivek',
    "ref_number": 9968038609,
    'loan_amount': 1000,
    'paid_status': '0',
    'disbursal_date': '2020-01-19',
    'user_id': '123',
}
send_message(data)
