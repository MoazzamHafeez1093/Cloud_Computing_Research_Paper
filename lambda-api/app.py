import json
import time
import math

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    workload = params.get('workload', 'light')
    
    limits = {'light': 500, 'medium': 5000, 'heavy': 50000}
    limit = limits.get(workload, 500)
    
    start = time.time()
    
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [x for x in range(2, limit) if is_prime(x)]
    
    end = time.time()
    duration_ms = round((end - start) * 1000, 2)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda",
            "workload": workload,
            "primes_found": len(primes),
            "computation_ms": duration_ms
        })
    }