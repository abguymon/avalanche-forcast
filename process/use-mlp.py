from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np
import csv


data = []
header_row = None
with open('./allData.csv', mode='r', newline='') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if row[1] == 'Date':
            header_row = row
        else:
            data.append(row)

header_row = np.array(header_row)
data = np.array(data)

print(header_row)

selected_headers = ['maxtempC', 'mintempC', 'totalSnow_cm', 'tempC', 'windspeedKmph', 'winddirDegree', 'precipMM', 'humidity']
selected_mapping = [np.where(header_row == header)[0][0] for header in selected_headers ]
# print(selected_mapping)
# print(np.shape(data))
# selected_data = np.array(data[:,selected_mapping]).astype(np.float64)
# print(np.shape(selected_data))

labels = data[:,-1]
lb = LabelBinarizer()
lb.fit(labels)
labels = lb.transform(labels)

done = set()


def do_for_mapping(headers, mapping):
    if len(headers) == 0 or str(mapping) in done:
        return 0, []
    selected_data = np.array(data[:,mapping]).astype(np.float64)

    trainData, testData, trainLabels, testLabels = train_test_split(selected_data, labels, test_size=.25)

    trainLabels = np.reshape(trainLabels, (-1,))
    testLabels = np.reshape(testLabels, (-1,))

    # print(testData)
    print(headers)

    model_list = []

    for dummy_iterator in range(10):
        model_list.append([])
        mlp = MLPClassifier(hidden_layer_sizes=[len(selected_headers)] * len(selected_headers), validation_fraction=.25, early_stopping=True)
        # mlp = MLPClassifier(validation_fraction=.25, early_stopping=False)
        model_list[-1].append(mlp)
        mlp.fit(trainData, trainLabels)
        model_list[-1].append(mlp.score(testData, testLabels))

    avg = 0

    with open('./data/mlp_out.txt', mode='a') as outfile:
        outfile.write(str(selected_headers) + '\n')
        for row in model_list:
            outfile.write(str(row) + '\n')
            avg += row[-1]
        avg /= len(model_list)
        outfile.write("\n\nAverage accuracy:" + str(avg) + '\n\n')

    done.add(str(mapping))

    best_headers = headers

    for index in range(len(headers)):
        new_headers = headers[0:index] + headers[index +1:]
        new_mapping = mapping[0:index] + mapping[index + 1:]
        an_average, some_headers = do_for_mapping(new_headers, new_mapping)
        if an_average > avg:
            avg = an_average
            best_headers = some_headers

    return avg, best_headers

avg, headers = do_for_mapping(selected_headers, selected_mapping)
with open('./data/mlp_out.txt', mode='a') as outfile:
    outfile.write("\n\nBest average:" + str(avg) + " With headers " + str(headers))
