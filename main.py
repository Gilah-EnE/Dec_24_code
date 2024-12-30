from statistical_analysis import compression_test

with open("c:/Users/Gilah/Documents/Зразки шифрування/xaa", 'rb') as file:
    data = file.read()
    print(compression_test(data))