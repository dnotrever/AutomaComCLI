import re
def format_phone(phone):
    phone = ''.join(re.findall('[0-9]+', phone))
    if (len(phone) > 10):
        return f'({phone[:2]}) {phone[2:7]}-{phone[7:11]}'
    elif (len(phone) > 9):
        return f'({phone[:2]}) {phone[2:6]}-{phone[6:10]}'
    else:
        return phone