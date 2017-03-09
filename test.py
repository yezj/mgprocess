import cv2
import cv2.cv as cv
from DTK_linux import init_CNN_model, getSegRecResult2

img1 = cv2.cv.LoadImage('test2_0.jpg', 0)
img2 = cv2.cv.LoadImage('test2_1.jpg', 0)
height1 = img1.height
width1 = img1.width

height2 = img2.height
width2 = img2.width
raw_data1 = img1.tostring()
raw_data2 = img2.tostring()
i = init_CNN_model("DTK.prototxt", "DTK.caffemodel", "DTK.binaryproto")
str1 = '{"qz":[{"y":2501,"x":1069,"height":326,"width":964,"scorezones":[{"y":2784,"x":1167,"height":33,"width":58},{"y":2715,"x":1167,"height":34,"width":58},{"y":2646,"x":1167,"height":34,"width":58},{"y":2578,"x":1167,"height":33,"width":58}]},{"y":2449,"x":19,"height":452,"width":985,"scorezones":[{"y":2819,"x":902,"height":67,"width":67},{"y":2819,"x":819,"height":67,"width":67}]},{"y":2221,"x":19,"height":198,"width":985,"scorezones":[{"y":2374,"x":338,"height":34,"width":58},{"y":2374,"x":96,"height":34,"width":57},{"y":2306,"x":360,"height":33,"width":57},{"y":2306,"x":96,"height":33,"width":57}]},{"y":1924,"x":19,"height":267,"width":985,"scorezones":[{"y":2149,"x":339,"height":33,"width":58},{"y":2149,"x":97,"height":33,"width":57},{"y":2080,"x":318,"height":34,"width":57},{"y":2080,"x":97,"height":34,"width":57}]},{"y":1716,"x":19,"height":187,"width":985,"scorezones":[{"y":1858,"x":835,"height":33,"width":57},{"y":1858,"x":624,"height":33,"width":58},{"y":1858,"x":414,"height":33,"width":57},{"y":1858,"x":96,"height":33,"width":57}]},{"y":1711,"x":1069,"height":570,"width":964,"scorezones":[{"y":1724,"x":1952,"height":67,"width":69},{"y":1724,"x":1870,"height":67,"width":68}]},{"y":1398,"x":1069,"height":290,"width":964,"scorezones":[{"y":1611,"x":1952,"height":66,"width":69},{"y":1611,"x":1870,"height":66,"width":68}]},{"y":1394,"x":19,"height":157,"width":985,"scorezones":[{"y":1475,"x":902,"height":66,"width":67},{"y":1475,"x":819,"height":66,"width":67}]},{"y":1033,"x":19,"height":334,"width":985,"scorezones":[{"y":1323,"x":96,"height":34,"width":57},{"y":1254,"x":96,"height":34,"width":57},{"y":1185,"x":96,"height":33,"width":57},{"y":1116,"x":96,"height":34,"width":57}]},{"y":978,"x":1069,"height":395,"width":964,"scorezones":[{"y":1327,"x":1147,"height":34,"width":56},{"y":1193,"x":1147,"height":34,"width":56},{"y":1124,"x":1147,"height":34,"width":56},{"y":1055,"x":1147,"height":33,"width":56}]},{"y":807,"x":19,"height":195,"width":985,"scorezones":[{"y":959,"x":371,"height":34,"width":57},{"y":959,"x":96,"height":34,"width":57},{"y":891,"x":371,"height":33,"width":57},{"y":891,"x":96,"height":33,"width":57}]},{"y":614,"x":1069,"height":334,"width":964,"scorezones":[{"y":899,"x":1147,"height":34,"width":56},{"y":830,"x":1147,"height":34,"width":56},{"y":762,"x":1147,"height":33,"width":56},{"y":692,"x":1147,"height":34,"width":56}]}],"num":8,"no":1,"cid":"58379f74421aa9c513c68d71"}'
str2 = '{"qz":[{"y":2198,"x":22,"height":694,"width":987,"scorezones":[{"y":2454,"x":904,"height":68,"width":67},{"y":2454,"x":822,"height":68,"width":67}]},{"y":1825,"x":22,"height":355,"width":987,"scorezones":[{"y":1899,"x":904,"height":68,"width":67},{"y":1899,"x":822,"height":68,"width":67}]},{"y":1557,"x":22,"height":239,"width":987,"scorezones":[{"y":1721,"x":904,"height":67,"width":67},{"y":1721,"x":822,"height":67,"width":67}]},{"y":1317,"x":22,"height":223,"width":987,"scorezones":[{"y":1464,"x":904,"height":66,"width":67},{"y":1464,"x":822,"height":66,"width":67}]},{"y":1139,"x":22,"height":156,"width":987,"scorezones":[{"y":1219,"x":904,"height":66,"width":67},{"y":1219,"x":822,"height":66,"width":67}]},{"y":1078,"x":1043,"height":1815,"width":991,"scorezones":[{"y":1414,"x":1953,"height":67,"width":67},{"y":1414,"x":1870,"height":67,"width":67}]},{"y":777,"x":22,"height":337,"width":987,"scorezones":[{"y":1068,"x":121,"height":33,"width":57},{"y":999,"x":121,"height":34,"width":57},{"y":930,"x":121,"height":34,"width":57},{"y":862,"x":121,"height":33,"width":57}]},{"y":552,"x":22,"height":197,"width":987,"scorezones":[{"y":705,"x":417,"height":34,"width":57},{"y":705,"x":121,"height":34,"width":57},{"y":637,"x":417,"height":34,"width":57},{"y":637,"x":121,"height":34,"width":57}]},{"y":99,"x":1043,"height":804,"width":991,"scorezones":[{"y":313,"x":1953,"height":68,"width":67},{"y":313,"x":1870,"height":68,"width":67}]},{"y":99,"x":22,"height":427,"width":987,"scorezones":[{"y":481,"x":332,"height":34,"width":56},{"y":481,"x":121,"height":34,"width":57},{"y":412,"x":332,"height":33,"width":56},{"y":412,"x":121,"height":33,"width":57}]}],"num":8,"no":2,"cid":"58379f74421aa9c513c68d71"}'

result = getSegRecResult2(str1, str2, raw_data1, width1, height1, raw_data2, width2, height2)
print 'result: ', dir(result[0])
print 'qzR: ', dir(result[0].qzR[0])
print 'qzone: ', dir(result[0].qzR[0].qzone)
print '---------------page---------------'
for i in range(0, result.size()):
    print 'student: ', result[i].student
    print 'cid: ', result[i].cid
    print 'num: ', result[i].num
    print 'no: ', result[i].no
    print '-----------------qzR-----------------'
    for j in range(0, result[i].qzR.size()):
        print 'score: ', result[i].qzR[j].score
        print 'answer: ', result[i].qzR[j].answer
        print 'type: ', result[i].qzR[j].type
        print 'no: ', result[i].qzR[j].no
        width = result[i].qzR[j].qzone.width
        print 'width: ', width
        height = result[i].qzR[j].qzone.height
        print 'height: ', height
        buffer = result[i].qzR[j].qzone.buffer
        # for iii in range(width * height):
        #	print ord(buffer[iii])
        print 'buffer: ', len(buffer), width * height
        try:
            im = cv.CreateImage((width, height), 8, 1)
            for ii in range(im.height):
                for jj in range(im.width):
                    im[ii, jj] = ord(buffer[jj + ii * width])
            cv.SaveImage("{}{}.jpg".format(i, j), im)
            print 'img ok'
        except:
            print i, j
            print 'img wrong'
        print '------------------next--------------------'

# result[0].getfree(0)#free result:result[num].getfree(num)
# result[1].getfree(1)