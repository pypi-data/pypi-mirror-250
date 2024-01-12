from csv import reader

FILE_PATH = "data/statistik_iwak_papuyu.csv"


def get_data(header=False):
    """
    Fungsi untuk mendapatkan data statistik iwak papuyu.

    Parameter:
    - header (boolean): menampilkan judul tiap kolom serta nomor tiap baris data (default: False).

    Return:
    list: berbentuk dua dimensi untuk tiap elemen pada list merupakan baris data. 

    Contoh tanpa header:
    [
      [1.5, 2.2, 3.1, ...],
      [5.6, 6.7, 4.0, ...],
    ]

    Contoh dengan header:
    [
      ['No', 'Panjang Badan', 'Panjang Kepala', ...],
      [1, 1.5, 2.2, 3.1, ...],
      [2, 5.6, 6.7, 4.0, ...],
    ]
    """
    csv = []
    with open(FILE_PATH, mode='r', encoding='utf-8', newline='') as file:
        csv_file = reader(file)
        for row in csv_file:
            if header:
                csv.append(row)
                continue
            csv.append(row[1:])
    if header:
        return csv

    return csv[1:]


def get_header():
    """
    Fungsi untuk mendapatkan header dari data statistik iwak papuyu.

    Return:
    list: berupa daftar judul dari tiap kolom pada data.
    """
    data = get_data(header=True)
    return data[0]


def get_data_by_column(column_name):
    """
    Fungsi untuk data statistik iwak papuyu berdasarkan kolom tertentu.

    Parameter:
    - colum_name (string): nama atau judul dari kolom

    Return:
    list: berupa data berdasarkan kolom tertentu
    """
    data = get_data(header=True)
    header = data.pop(0)
    if column_name not in header:
        raise KeyError(
            f"{column_name} bukan merupakan nama kolom yang terdapat pada data")

    index = header.index(column_name)
    column_data = []
    for row in data:
        column_data.append(float(row[index]))
    return column_data


def average(column_name, precision=3):
    """
    Fungsi untuk mendapatkan rata-rata dari data statistik iwak papuyu berdasarkan kolom tertentu.

    Parameter:
    - colum_name (string): nama atau judul dari kolom
    - precision (int): presisi nilai rata-rata (default: 3 angka setelah koma)

    Return:
    float: berupa rata-rata dari data berdasarkan kolom tertentu
    """
    column_data = get_data_by_column(column_name)
    avg = sum(column_data)/len(column_data)
    formatted_sum = f"{avg:.{precision}f}"
    return formatted_sum


def median(column_name):
    """
    Fungsi untuk mendapatkan median dari data statistik iwak papuyu berdasarkan kolom tertentu.

    Parameter:
    - colum_name (string): nama atau judul dari kolom

    Return:
    float: berupa median dari data berdasarkan kolom tertentu
    """
    sorted_column_data = sorted(get_data_by_column(column_name))
    n = len(sorted_column_data)
    if n % 2 == 1:
        return sorted_column_data[n // 2]

    first_half_middle = sorted_column_data[(n - 1) // 2]
    last_half_middle = sorted_column_data[(n + 1) // 2]
    return (first_half_middle + last_half_middle) / 2


def modes(column_name):
    """
    Fungsi untuk mendapatkan nilai modus dari data statistik iwak papuyu berdasarkan kolom tertentu.

    Parameter:
    - colum_name (string): nama atau judul dari kolom

    Return:
    list: berupa daftar nilai modus dari data berdasarkan kolom tertentu
    """
    freq_dict = {}

    column_data = get_data_by_column(column_name)
    for data in column_data:
        freq_dict[data] = freq_dict.get(data, 0) + 1

    max_freq = max(freq_dict.values())
    return [key for key, value in freq_dict.items() if value == max_freq]
