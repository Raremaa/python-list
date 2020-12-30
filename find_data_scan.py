import redis
import time

# Redis SCAN Demo
if __name__ == '__main__':
    start = time.process_time()

    r = redis.Redis()
    pipe = r.pipeline()
    cursor = 0
    while 1:
        cursor, data = pipe.scan(cursor, "mykey*", 1000000)
        if cursor == 0:
            break
    pipe.execute()

    end = time.process_time()
    print('Running time: %s Seconds' % (end - start))
