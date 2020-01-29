from .models import Profile, Loans, BankAccountDetails
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, date
from .Newmessage import send_message
import csv
import sys
import os

django_path = r'/home/credicxo/credicxo-project/'


def DailySms():
    FilterDate = str(timezone.now() - timedelta(days=10))
    user_data = Loans.objects.filter(loan_date__lte=FilterDate, repayment_status__lte=1).values(
        'user__id', 'loan_date', 'repayment_status', 'loan_type__amount')

    for i in user_data:
        try:
            profile = Profile.objects.filter(user=i['user__id']).values('user__username', 'phone_number',
                                                                        'preference__relation', 'preference_number')[0]
            bank_data = BankAccountDetails.objects.filter(user=i['user__id']).values('account_number')[0]
            fin_date = datetime.strptime(str(i['loan_date']), '%Y-%m-%d %H:%M:%S+00:00').date()
            data = {
                "users_name": profile['user__username'],
                "contact_no": profile['phone_number'],
                "account_number": bank_data['account_number'],
                "ref_name": profile['preference__relation'],
                "ref_number": profile['preference_number'],
                'loan_amount': i['loan_type__amount'],
                'paid_status': str(i['repayment_status']),
                'disbursal_date': fin_date,
            }

            send_message(data)

        except Exception as e:
            print(e)
            f = open(django_path + "not_work.txt", "a+")
            f.write("{} \n".format(i))
    date_format = "%Y-%m-%d"
    today = datetime.strptime(str(date.today()), date_format)
    total1 = 0
    total2 = 0
    total3 = 0
    total4 = 0
    total5 = 0
    total6 = 0
    total7 = 0
    total8 = 0
    total9 = 0
    total10 = 0
    total11 = 0
    total12 = 0
    total13 = 0
    total14 = 0
    total15 = 0
    total16 = 0
    total17 = 0
    total = 0
    with open(django_path + "new_recovery_msg_csv2.csv") as fin:
        csv_file = csv.reader(fin)
        csv.field_size_limit(sys.maxsize)
        next(csv_file, None)
        for row in csv_file:
            total1 += int(row[1])
            total2 += int(row[2])
            total3 += int(row[3])
            total4 += int(row[4])
            total5 += int(row[5])
            total6 += int(row[6])
            total7 += int(row[7])
            total8 += int(row[8])
            total9 += int(row[9])
            total10 += int(row[10])
            total11 += int(row[11])
            total12 += int(row[12])
            total13 += int(row[13])
            total14 += int(row[14])
            total15 += int(row[15])
            total16 += int(row[16])
            total17 += int(row[17])
            total += int(row[18])
        print(total1, total2, total3, total4, total5, total6, total7, total8, total9, total10, total11, total12,
              total13, total14, total15, total16, total17, total)
    csv2_fields = ["Date", "EMI1_10-13", "EMI1_14", "EMI1_15", "EMI1_16-25", "EMI1_26-30", "EMI1_31-35", "EMI1_36-45",
                   "EMI1_56-60", "EMI1_61-64", "EMI1_65-70", "EMI2_56-59", "EMI2_60", "EMI2_61", "EMI2_62-70",
                   "EMI2_71-75", "EMI2_76-81", "EMI2_82-91", "total_msg"]
    csv2_dict = {
        "Date": str(today.date()),
        "EMI1_10-13": total1,
        "EMI1_14": total2,
        "EMI1_15": total3,
        "EMI1_16-25": total4,
        "EMI1_26-30": total5,
        "EMI1_31-35": total6,
        "EMI1_36-45": total7,
        "EMI1_56-60": total8,
        "EMI1_61-64": total9,
        "EMI1_65-70": total10,
        "EMI2_56-59": total11,
        "EMI2_60": total12,
        "EMI2_61": total13,
        "EMI2_62-70": total14,
        "EMI2_71-75": total15,
        "EMI2_76-81": total16,
        "EMI2_82-91": total17,
        "total_msg": total,
    }
    csv2_rows = []
    csv2_rows.append(csv2_dict)
    if total != 0:
        with open(django_path + 'final.csv', 'a') as csvfile2:
            writer = csv.DictWriter(csvfile2, fieldnames=csv2_fields)
            if csvfile2.tell() == 0:
                writer.writeheader()
            writer.writerows(csv2_rows)
    os.remove(django_path + 'new_recovery_msg_csv2.csv')
