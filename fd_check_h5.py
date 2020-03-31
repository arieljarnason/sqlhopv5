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

mvd_query_template = """
SELECT
    '{A} ->> ({B}, {D}) in {R}' AS Relation,
    CASE WHEN COUNT(*) = 0 THEN
        'MAYBE MVD'
    ELSE
        'NO MVD'
    END AS MVD
FROM (
    SELECT {A}
    FROM {R}
    GROUP BY {A}
    HAVING COUNT(*) > 1
        AND COUNT(*) <> COUNT(DISTINCT {B}) * COUNT(DISTINCT {D})
) X;
"""

tables = [
    ("Rentals", ("PID", "HID", "PN", "S", "HS", "HZ", "HC")),
    ("Coffees", ("DID", "HID", "CID", "DN", "DS", "CN", "CM")),
    ("Projects", ("ID", "PID", "SID", "SN", "PN", "MID", "MN")),
    ("Customers", ("CID", "CN", "CS", "CNr", "CZ", "CC", "EID")),
]

mvdtables = [
    ("Coffees", ("DID", "HID", "CID", "DN", "DS", "CN", "CM")),
    ("Projects", ("ID", "PID", "SID", "SN", "PN", "MID", "MN")),
]

def fdcheck():
    with open("FDcheck.sql", "w") as myfile:
        for table, attributes in tables:
            for a, b in permutations(attributes, 2):
                query = fd_query_template.format(R=table, A=a, B=b)
                # print(query)
                myfile.write(query)

def mvdcheck():
    with open("MVDcheck.sql", "w") as myfile:
        for table, attributes in mvdtables:
            for a, b, d in permutations(attributes, 3):
                query = mvd_query_template.format(R=table, A=a, B=b, D=d)
                # print(query)   
                myfile.write(query)             



# fdcheck()
mvdcheck()