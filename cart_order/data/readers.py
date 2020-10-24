import csv
from . import datastore


STARTING_HEADERS = ["Name", "Description", "Price", "Quantity"]


def validate_headers(headers):
    starting_headers = headers[:len(STARTING_HEADERS)]
    if starting_headers != STARTING_HEADERS:
        msg = f"Expecting headers of {STARTING_HEADERS}, got {starting_headers}"
        raise Exception(msg)


def read_csv(path: str, username: str) -> list:
    """
    Read a CSV and put the results into a database corresponding to the username. Returns the list of items come across
    in the file.
    """
    items = list()
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
                store_mapping = datastore.ensure_stores(stores, username)
                continue
            item_name, description, price = row[0], row[1], float(row[2])
            for index, store in enumerate(stores):
                print(row)
                item = datastore.add_item(item_name, description, price, row[len(STARTING_HEADERS) + index], store, store_mapping, username)
                print(item.name, item.store_id, item.price)
            items.append(item_name)
            line_number += 1
    
    return items


def print_list(items: list, username: str) -> None:
    """takes in a list of items that the user wants to query, and prints out all stores we have the information for on them"""


if __name__ == "__main__":
    datastore._make_fake_user()
    read_csv("test.csv", datastore.TEMP_USERNAME)
