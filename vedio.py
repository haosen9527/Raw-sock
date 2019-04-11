import urllib2
print "stand"

for i in range(1, 23, 1):
    url = 'http://newoss.maiziedu.com/yxyh4/pand-%02d.mp4' % i

    f = urllib2.urlopen(url)
    data = f.read()
    name = 'python_pandas_%02d.mp4' % (i)

    with open(name, "wb") as code:
        code.write(data)

print 'end'