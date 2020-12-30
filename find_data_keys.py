import redis
import time

# Redis Pipeline Demo
if __name__ == '__main__':
    start = time.process_time()

    r = redis.Redis()
    pipe = r.pipeline()
    keys = pipe.keys("myke*")
    pipe.execute()

    end = time.process_time()
    print('Running time: %s Seconds' % (end - start))
