from datetime import date
import os

current_path = os.path.dirname(os.path.realpath(__file__))

def new_number():
    today=date.today()
    cur_year=today.year

    filepath = "number.txt"
    full_file_path = os.path.join(current_path, filepath)
    f = open(full_file_path, "r")
    
    year=int(f.readline())
    number=int(f.readline())
    ex=""
    if(year==cur_year):
        if(number<9):
            number +=1
            ex += "0" +str(number) + "_" + str(year)
        else:
            number +=1
            ex += str(number) + "_" + str(year)
    else:
        year=cur_year
        number=1
        ex += "0" +str(number) + "_" + str(year)
    f.close()
    f = open(filepath, "w")
    f.write(str(year) +"\n" + str(number))   
    f.close()
    return str(ex)
