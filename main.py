import csv


def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = [row for row in csv_reader]
    return header, data


if __name__ == "__main__":
    file_path = "data_file/test.csv"
    header, data = read_csv(file_path)
    print("Header:", header)
    print("Data:", data)

print("hello")
print("world")
