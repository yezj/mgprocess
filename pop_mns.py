import imgprocess
import recognition
pop_mns = imgprocess.MNSReader()

cnt = 0
while 1:
    req = recognition.pick_message(pop_mns)
    cnt += 1
    pop_mns.pop()
    print 'pop_success_{}'.format(cnt)
