from random import randint


def matrix():
    data = []
    f = []
    for i in xrange(0, 5):
        d = [randint(1, 100) for x in xrange(0, 5)]
        d.append(sum(d))
        data.append(d)

    for i in xrange(0, 5):
        for j in xrange(0, 5):
            z = 0

    print(data)


matrix()