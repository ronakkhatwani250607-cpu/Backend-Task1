log_file = "Logfile.txt"  

total_requests = 0
endpoint_hits = {}
endpoint_times = {}
users = set()
users_by_year = {}
total_timetables = 0
algo_usage = {"Backtracking": 0, "Iterative random sampling": 0}

def add_count(dictionary, key):
    dictionary[key] = dictionary.get(key, 0) + 1

with open(log_file, "r", errors="ignore") as f:
    for line in f:
        line_lower = line.lower()

        #Detect requests & endpoints
        if "get" in line_lower or "post" in line_lower:
            total_requests += 1
            parts = line.split()
            for i in range(len(parts)):
                if parts[i].upper() in ["GET", "POST"]:
                    endpoint = parts[i+1]
                    add_count(endpoint_hits, endpoint)
                    break

        #Capture response times (ms or µs)
        if ("ms" in line_lower or "µs" in line_lower) and ("get" in line_lower or "post" in line_lower):
            parts = line.split()
            for w in parts:
                if "ms" in w or "µs" in w:
                    try:
                        if "ms" in w:
                            time_value = float(w.replace("ms", ""))
                        elif "µs" in w:
                            time_value = float(w.replace("µs", "")) / 1000  # convert µs to ms
                        endpoint_times.setdefault(endpoint, []).append(time_value)
                    except:
                        pass

        #Detect unique users
        if "[" in line and "]" in line:
            content = line.split("[")[-1].split("]")[0]
            if len(content) ==13 and content[:4].isdigit():
                users.add(content)
                year = content[:4]
                add_count(users_by_year, year)

        # Detect timetables
        if "generation complete" in line_lower and "timetables" in line_lower:
            total_timetables += 1

        #Detect algorithm usage 
        if "backtracking" in line_lower:
            algo_usage["Backtracking"] += 1
        elif "iterative" in line_lower:
            algo_usage["Iterative random sampling"] += 1

#Calculate performance metrics
performance = {}
for ep, times in endpoint_times.items():
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        performance[ep] = (avg_time, max_time, len(times))

#Print report 

print(f" Total API requests: {total_requests}")
print("\n Endpoint popularity:")
for ep, count in sorted(endpoint_hits.items(), key=lambda x: x[1], reverse=True):
    print(f"{count}")

print("\n Performance metrics:")
for ep, stats in performance.items():
    print(f" avg: {stats[0]:.2f} ms   max: {stats[1]:.2f} ms   samples: {stats[2]}")

print(f"\n Unique users: {len(users)}")
print("   Users by year:")
for year, count in sorted(users_by_year.items()):
    print(f"{year}: {count} Unique IDs")

print(f"\n Total timetables generated: {total_timetables}")
print("\n Algorithm usage:")
for algo, count in algo_usage.items():
    print(f"{algo}: {count}")
