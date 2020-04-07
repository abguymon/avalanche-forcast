from sklearn.cluster import AgglomerativeClustering
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

# print(header_row)

selected_headers = ['maxtempC', 'mintempC', 'totalSnow_cm', 'tempC', 'windspeedKmph', 'winddirDegree', 'precipMM', 'humidity']
selected_mapping = [np.where(header_row == header)[0][0] for header in selected_headers ]
# print(selected_mapping)
# print(np.shape(data))
selected_data = np.array(data[:,selected_mapping]).astype(np.float64)
# print(np.shape(selected_data))

labels = data[:,-1]

lb = LabelBinarizer()
lb.fit(labels)
labels = np.reshape(lb.transform(labels), (-1,))

# trainData, testData, trainLabels, testLabels = train_test_split(selected_data, labels, test_size=.25)

# trainLabels = np.reshape(trainLabels, (-1,))
# testLabels = np.reshape(testLabels, (-1,))

# model_list = []

# model_list.append([])

done = set()

def do_for_mapping(headers, mapping):
    if len(headers) == 0 or str(mapping) in done:
        return -1 * np.inf, []

    selected_data = np.array(data[:,mapping]).astype(np.float64)
    
    hac = AgglomerativeClustering()
    print(headers)

    predict = hac.fit_predict(selected_data)
    # print(labels)
    count = 0
    for h, l in zip(predict, labels):
        # print(h, l)
        if (h == l):
            count += 1
    # print(str(count / len(labels)))
    count /= len(labels)
    count -= .5
    count = abs(count)

    with open('./data/hac_out.txt', mode='a') as outfile:
        outfile.write(str(hac) + '\n')
        outfile.write('accuracy ' + str(count) + '\n\n')

    done.add(str(mapping))

    best_score = count
    best_headers = headers

    for index in range(len(headers)):
        new_headers = headers[0:index] + headers[index +1:]
        new_mapping = mapping[0:index] + mapping[index + 1:]
        a_count, some_headers = do_for_mapping(new_headers, new_mapping)
        if a_count > best_score:
            best_score = a_count
            best_headers = some_headers
    
    return best_score, best_headers

score, headers = do_for_mapping(selected_headers, selected_mapping)

with open('./data/hac_out.txt', mode='a') as outfile:
    outfile.write("\n\nBest score:" + str(score) + " With headers " + str(headers))
