def get_wendu():
    wendu = 22
    print(wendu)
   #print("当前的室温是%d"%wendu)
   # return wendu

def get_wendu_huashi(wendu):
    wendu = wendu + 3
    print("当前的温度（华氏）是%d"%wendu)

wendu=int(get_wendu())
get_wendu_huashi(wendu)
