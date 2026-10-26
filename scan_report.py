# Augustine
# Part 1
HIGH_RISK = 4
UNKNOWN_RISK = 3

scan = [
    ("10.0.0.1", 22, "open"),
    ("10.0.0.1", 53, "open"),
    ("10.0.0.1", 80, "closed"),
    ("10.0.0.1", 443, "open"),
    ("10.0.0.10", 21, "open"),
    ("10.0.0.10", 22, "open"),
    ("10.0.0.10", 23, "open"),
    ("10.0.0.10", 80, "open"),
    ("10.0.0.10", 3306, "open"),
    ("10.0.0.20", 80, "open"),
    ("10.0.0.20", 443, "open"),
    ("10.0.0.20", 3306, "filtered"),
    ("10.0.0.20", 8080, "open"),
    ("10.0.0.30", 445, "open"),
    ("10.0.0.30", 3389, "open"),
    ("10.0.0.30", 4444, "open"),
    ("10.0.0.30", 22, "closed"),
    ("10.0.0.40", 22, "filtered"),
    ("10.0.0.40", 80, "closed"),
    ("10.0.0.40", 443, "closed"),
]

services = [
    (21, "ftp", 3),
    (22, "ssh", 1),
    (23, "telnet", 5),
    (25, "smtp", 2),
    (53, "dns", 1),
    (80, "http", 2),
    (443, "https", 1),
    (445, "smb", 4),
    (3306, "mysql", 4),
    (3389, "rdp", 5),
]
print("Scan records:", len(scan))
print("Service records:", len(services))

# Part 2
open_count = 0
closed_count = 0
filtered_count = 0

for host, port, state in scan:
    if state == "open":
        open_count = open_count + 1
    elif state == "closed":
        closed_count = closed_count + 1
    else:
        filtered_count = filtered_count + 1

print("Open:", open_count)
print("Closed:", closed_count)
print("Filtered:", filtered_count)
print("Open percentage: " + f"{open_count / len(scan) * 100:.1f}" + "%")

# Part 3
hosts = []

for host, port, state in scan:
    if host not in hosts:
        hosts.append(host)

print(hosts)
print("How many hosts:", len(hosts))

# Part 4
for host in hosts:
    open_ports = []
    for host2, port, state in scan:
        if host2 == host and state == "open":
            open_ports.append(port)
    open_ports.sort()
    if len(open_ports) == 0:
        print(host, "No open ports")
    else:
        print(host, "has", len(open_ports), ":", open_ports)

# Part 5
unknown = 0

for host, port, state in scan:
    if state == "open":
        name = "unknown"
        risk = UNKNOWN_RISK
        for p, s, r in services:
            if p == port:
                name = s
                risk = r
                break
        if name == "unknown":
            unknown = unknown + 1
        print(host, port, name, risk)

print("Unknown services:", unknown)

# Part 6
alerts = 0

for host, port, state in scan:
    if state == "open":
        for p, s, r in services:
            if p == port:
                if r >= HIGH_RISK:
                    print("ALERT:", host, port, s, r)
                    alerts = alerts + 1
                break

print("Alerts:", alerts)

# Part 7
ranking = []

for host in hosts:
    score = 0
    for host2, port, state in scan:
        if host2 == host and state == "open":
            risk = UNKNOWN_RISK
            for p, s, r in services:
                if p == port:
                    risk = r
                    break
            score = score + risk
    ranking.append((score, host))

ranking.sort(reverse=True)

print("Full ranking:")
for score, host in ranking:
    if score >= 10:
        level = "CRITICAL"
    elif score >= 5:
        level = "HIGH"
    elif score >= 1:
        level = "LOW"
    else:
        level = "CLEAN"
    print(host, score, level)

print("Two most dangrous:")
for score, host in ranking[:2]:
    print(host, score)

# Part 8
while True:
    answer = input("Type a port number (0 to stop): ")
    port_num = int(answer)
    if port_num == 0:
        break
    found = 0
    for host, port, state in scan:
        if port == port_num and state == "open":
            print(host)
            found = found + 1
    if found == 0:
        print("No host has that port open")