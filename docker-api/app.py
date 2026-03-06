from flask import Flask, jsonify
import time
import math

app = Flask(__name__)

@app.route('/')
def hello():
    start = time.time()

    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    primes = [x for x in range(2, 500) if is_prime(x)]

    end = time.time()
    duration_ms = round((end - start) * 1000, 2)

    return jsonify({
        "message": "Hello from Docker on EC2",
        "primes_found": len(primes),
        "computation_ms": duration_ms
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)