"""
This module contains compute logic that is used in views.
This provides a logical separation of control logic with views
"""
def get_seats(max_row,max_col):
        row_map = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',
        10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
        21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
        alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        max_row = row_map.get(max_row)
        temp = []
        seats = []
        for alphabet in alphabets:
            temp.append(alphabet)
            if alphabet == max_row:
                temp.append(alphabet)
                break
        for i in range(1,max_col):
            for alphabet in temp:
                seats.append(f"{alphabet}{i}")
            # seats.sort()
        return seats