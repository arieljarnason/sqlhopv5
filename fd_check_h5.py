from itertools import permutations

fd_query_template = """

SELECT '{R}: {A} --> {B}' AS FD,
    CASE WHEN COUNT(*) = 0 THEN
        'HOLDS'
    ELSE   
        'DOES NOT HOLD'
    END AS VALIDITY
FROM (
    SELECT {A}
    FROM {R}
    GROUP BY {A}
    HAVING COUNT(DISTINCT {B}) > 1
) X;
"""

tables = [
    ("Rentals", ("PID", "HID", "PN", "S", "HS", "HZ", "HC")),
    ("Coffees", ("DID", "HID", "CID", "DN", "DS", "CN", "CM")),
    ("Projects", ("ID", "PID", "SID", "SN", "PN", "MID", "MN")),
    ("Customers", ("CID", "CN", "CS", "CNr", "CZ", "CC", "EID")),
]

def fdcheck():
    with open("FDcheck.sql", "w") as myfile:
        for table, attributes in tables:
            for a, b in permutations(attributes, 2):
                query = fd_query_template.format(R=table, A=a, B=b)
                # print(query)
                myfile.write(query)

fdcheck()