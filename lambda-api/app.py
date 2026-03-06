import json
import time
import math

def lambda_handler(event, context):
    start = time.time()
    
    # Simulate real computation (prime number check)
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    # Do some work so the function isn't trivially fast
    primes = [x for x in range(2, 500) if is_prime(x)]
    
    end = time.time()
    duration_ms = round((end - start) * 1000, 2)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda",
            "primes_found": len(primes),
            "computation_ms": duration_ms
        })
    }