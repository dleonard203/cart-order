import csv


STARTING_HEADERS = ["Name", "Description", "Price"]

def validate_headers(headers):
    starting_headers = headers[:3]
    if starting_headers != STARTING_HEADERS:
        msg = f"Expecting headers of {STARTING_HEADERS}, got {starting_headers}"
        raise Exception(msg)
    


def read_csv(path: str) -> None:
    """
    Read a CSV and put the results into a database
    """
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_number = 0
        for row in csv_reader:
            if line_number == 0:
                # reading headers in
                validate_headers(row)
                stores = row[3:]
                print(stores)

if __name__ == "__main__":
    read_csv("test.csv")