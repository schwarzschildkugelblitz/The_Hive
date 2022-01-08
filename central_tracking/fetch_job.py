jobs = [
    ["FKMP0001", "1", "Ahmedabad"],

    ["FKMP0004", "2", "Bengaluru"],

    ["FKMP0002", "1", "Pune"],
    ["FKMP0003", "2", "Ahmedabad"],
    ["FKMP0004", "2", "Bengaluru"],
    ["FKMP0005", "2", "Kolkata"],
    ["FKMP0006", "1", "Mumbai"],
    ["FKMP0007", "2", "Delhi"],
    ["FKMP0008", "2", "Delhi"],
    ["FKMP0009", "2", "Bengaluru"],
    ["FKMP0010", "2", "Ahmedabad"],
    ["FKMP0011", "1", "Delhi"],
    ["FKMP0012", "2", "Chennai"],
    ["FKMP0013", "1", "Jaipur"],
    ["FKMP0014", "1", "Mumbai"],
    ["FKMP0015", "2", "Hyderabad"],
    ["FKMP0016", "1", "Kolkata"],
    ["FKMP0017", "1", "Bengaluru"],
    ["FKMP0018", "2", "Chennai"],
    ["FKMP0019", "2", "Ahmedabad"]
]


def job_generator():
    for job in jobs:
        yield job
