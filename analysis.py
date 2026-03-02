import requests
import time

eu_ip = "http://34.53.249.22:8080"
us_ip = "http://34.27.213.180:8080"

us_results = []
eu_results = []

for i in range(10):
    start = time.time()
    requests.get(us_ip + "/list")
    us_results.append((time.time() - start) * 1000)
  
for i in range(10):
    start = time.time()
    requests.get(eu_ip + "/list")
    eu_results.append((time.time() - start) * 1000)

print("US:", sum(us_results) / 10)
print("EU:", sum(eu_results) / 10)

print("\nPart B")
misses = 0

for i in range(100):
    user = "testuser" + str(i) + str(time.time())
    
    requests.post(us_ip + "/register", json={"username": user})
    
    data = requests.get(eu_ip + "/list").json()
    if user not in data["users"]:
        misses += 1

print("Total misses:", misses)
