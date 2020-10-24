import csv
from . import datastore


STARTING_HEADERS = ["Name", "Description", "Price", "Quantity"]


def validate_headers(headers):
    starting_headers = headers[:len(STARTING_HEADERS)]
    if starting_headers != STARTING_HEADERS:
        msg = f"Expecting headers of {STARTING_HEADERS}, got {starting_headers}"
        raise Exception(msg)


def read_csv(path: str, username: str) -> None:
    """
    Read a CSV and put the results into a database corresponding to the username
    """
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_number = 0
        store_mapping = None
        stores = None
        for row in csv_reader:
            if line_number == 0:
                # reading headers in
                validate_headers(row)
                stores = row[len(STARTING_HEADERS):]
                line_number += 1
                store_mapping = datastore.ensure_stores(stores)
                continue
            item_name, description, price = row[0], row[1], float(row[2])
            for index, store in enumerate(stores):
                print(row)
                item = datastore.add_item(item_name, description, price, row[len(STARTING_HEADERS) + index], store, store_mapping)
                print(item.name, item.store_id, item.price)
            line_number += 1
    
    print(store_mapping)

if __name__ == "__main__":
    read_csv("test.csv", datastore.TEMP_USERNAME)
