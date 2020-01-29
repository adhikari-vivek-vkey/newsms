from .models import Profile, Loans, BankAccountDetails
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, date
from .Newmessage import send_message
import csv

django_path = r'/home/credicxo/credicxo-project/'
date_format = "%Y-%m-%d"
today = datetime.strptime(str(date.today()), date_format)
csv2_dict = {
    "Date": str(today.date()),
    "EMI1_10-13": 0,
    "EMI1_14": 0,
    "EMI1_15": 0,
    "EMI1_16-25": 0,
    "EMI1_26-30": 0,
    "EMI1_31-35": 0,
    "EMI1_36-45": 0,
    "EMI1_56-60": 0,
    "EMI1_61-64": 0,
    "EMI1_65-70": 0,
    "EMI2_56-59": 0,
    "EMI2_60": 0,
    "EMI2_61": 0,
    "EMI2_62-70": 0,
    "EMI2_71-75": 0,
    "EMI2_76-81": 0,
    "EMI2_82-91": 0,
    "total_msg": 0
}


def DailySms():
    FilterDate = str(timezone.now() - timedelta(days=10))
    user_data = Loans.objects.filter(loan_date__lte=FilterDate, repayment_status__lte=1).values(
        'user__id', 'loan_date', 'repayment_status', 'loan_type__amount')

    for i in user_data:
        try:
            profile = Profile.objects.filter(user=i['user__id']).values('name', 'phone_number',
                                                                        'preference__relation', 'preference_number')[0]
            bank_data = BankAccountDetails.objects.filter(user=i['user__id']).values('account_number')[0]
            fin_date = datetime.strptime(str(i['loan_date']), '%Y-%m-%d %H:%M:%S+00:00').date()
            data = {
                "users_name": profile['name'],
                "contact_no": profile['phone_number'],
                "account_number": bank_data['account_number'],
                "ref_name": profile['preference__relation'],
                "ref_number": profile['preference_number'],
                'loan_amount': i['loan_type__amount'],
                'paid_status': str(i['repayment_status']),
                'disbursal_date': fin_date,
                'user_id': str(i['user__id']),
            }

            send_message(data)

        except Exception as e:
            print(e)
            f = open(django_path + "not_work.txt", "a+")
            f.write("{} \n".format(i))

    csv2_fields = ["Date", "EMI1_10-13", "EMI1_14", "EMI1_15", "EMI1_16-25", "EMI1_26-30", "EMI1_31-35", "EMI1_36-45",
                   "EMI1_56-60", "EMI1_61-64", "EMI1_65-70", "EMI2_56-59", "EMI2_60", "EMI2_61", "EMI2_62-70",
                   "EMI2_71-75", "EMI2_76-81", "EMI2_82-91", "total_msg"]
    csv2_rows = []
    csv2_rows.append(csv2_dict)
    if csv2_rows[0]["total_msg"] != 0:
        with open(django_path + 'new_recovery_msg_csv2.csv', 'a') as csvfile2:
            writer = csv.DictWriter(csvfile2, fieldnames=csv2_fields)
            if csvfile2.tell() == 0:
                writer.writeheader()
            writer.writerows(csv2_rows)
