"""
GLOBAL Helper methods
"""
import datetime
from django.http import Http404
from django.conf import settings
from twilio.rest import Client


def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404

def calculate_next_payment_date(cycle_frequency, current_date):
    if cycle_frequency=="Weekly":
        current_date=datetime.datetime.now() + datetime.timedelta(days=8)
        return current_date
    else:
        pass

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def calculate_payment_cycles(expected_duration, cycle_frequency, expected_payment, first_payment_date):
    if cycle_frequency=="Weekly": 
        cycles=[]
        amount_per_cycle=truncate(expected_payment/expected_duration, -3)
        final_payment = amount_per_cycle + expected_payment-(amount_per_cycle*expected_duration)
        for cycle in range(expected_duration-1):
            cycle_date = first_payment_date + datetime.timedelta(days=7*(cycle+1))
            individual_cycle={
                "cycle_date":cycle_date,
                "amount_expected":amount_per_cycle
            }
            cycles.append(individual_cycle)
        final_cycle = {
            "cycle_date":first_payment_date + datetime.timedelta(days=7*expected_duration),
            "amount_expected":final_payment
        }
        cycles.append(final_cycle)
        return cycles
    else:
        pass

def calculate_balance(larger_amount, smaller_amount):
    result = larger_amount - smaller_amount 
    return result if result > 0 else 0

def generate_account_number(id, account_type):
    if account_type == "savings":
        return "SAC{}{}SA".format(70, 00000000+id)
    else:
        return "SAC{}{}SH".format(80, 00000000+id)


def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    return client.messages.create(to=to, from_='+13092166584', body=message)
    