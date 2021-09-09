from datetime import datetime


# this flag prevent the application to search on itself when get equipment state
# when you put the application id on it getting equipment state will not take into consideration this application
record_flag = -1

def get_record_state(record):

    currentDate = datetime.today().date()
    #dateFrom = record.rental_process_id.date_from
    dateTo = record.rental_process_id.date_to
    isReceived = record.rental_process_id.is_received
    isReturned = record.rental_process_id.is_returned

    if currentDate <= dateTo :
        if not(isReceived) and not(isReturned):
            return 'requested'
        elif (isReceived) and not(isReturned) :
            return 'rented'
        elif (isReceived) and (isReturned) :
            return 'available'
    else:
        if (not(isReceived) and not(isReturned)) or (isReceived) and (isReturned):
            return 'available'
        elif (isReceived) and not(isReturned) :
            return 'late'

# priority function
def choose_state(state1 , state2):
    priority = {
        'rented': 1,
        'late': 1,
        'requested': 2,
        'available': 3
    }
    if priority[state1] < priority[state2]:
        return state1
    else :
        return state2


