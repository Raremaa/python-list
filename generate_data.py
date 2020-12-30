import redis

# 快速生成若干Redis数据
if __name__ == '__main__':
    r = redis.Redis()
    pipe = r.pipeline()
    for i in range(5000000):
        temp = str(i)
        pipe.set('myKey' + temp, 'myValue' + temp)
    pipe.execute()
