import math
import operator

# tinh khoang cach euclid cua 2 diem
def euclidean_distance(point1, point2):
	distance = 0.0
	for i in range(0,len(point1)):
		distance += (point1[i] - point2[i])**2
	return math.sqrt(distance)

# tao 1 hang doi uu tien chi chua duy nhat so phan tu dinh san la nhung phan tu
# gan voi diem can xet nhat
element_max = 1
def enqueue(priority_queue, item):
	if len(priority_queue) < element_max:
		priority_queue.append(item)
		priority_queue.sort(key=lambda k: k['value'])
	else:
		priority_queue.append(item)
		priority_queue.sort(key=lambda k: k['value'])
		priority_queue.pop()

# lay ra tu dien cua dataset da tao tai file create_dictionary.py
def getDictionary():
    path_file = "dataprocessing/dictionary/dictionary.txt"
    file_dictionary = open(path_file, "r", encoding = 'utf-8')
    doc_dictionary = file_dictionary.read()

    tmp = doc_dictionary.split('\n',1)
    number_of_works = tmp[0]
    dictionary_tmp = tmp[1].split('\n')

    dim = []
    dictionary = {}
    for x in dictionary_tmp:
        if x == '': # loai bo di dong cuoi cung
            break
        tmp1 = x.split(" ")
        dictionary[tmp1[1]] = tmp1[0]
        dim.append(tmp1[1])

    print("Da lay xong tu dien tu file dictionary.txt!")
    return [dictionary, dim]

# chuyen mot doan van ban sang vector
def convert_vector(document, dictionary):
    dictionary_mini = {}
    arr_text = document.split(' ')

    # thiet lap tu dien mini trong van ban dang xet
    for x in range(1,len(arr_text)-1):
        if arr_text[x] not in dictionary_mini:
            dictionary_mini[arr_text[x]] = 1
        else:
            dictionary_mini[arr_text[x]] += 1

    vectorDoc = []
    for x in dictionary:
      if x not in dictionary_mini: 
          dictionary_mini[x] = 0
      vectorDoc_tmp = (dictionary_mini[x])
      vectorDoc.append(vectorDoc_tmp)

    return vectorDoc

# chuyen doi vector tu string -> map<int, int>
def handleVector(vector_non_handle):
    array_tmp = vector_non_handle.split(" ",1)
    vector_tmp1 = int(array_tmp[0])
        
    vector_tmp2 = []
    string_tmp = array_tmp[1].split(" ")
    for x in string_tmp:
        x_tmp = int(x)
        vector_tmp2.append(x_tmp)

    item = {"type" : vector_tmp1, "vector" : vector_tmp2}
        
    return item

"""
  bat dau tinh toan
"""
# lay du lieu truoc khi tinh toan
dictionary = {}
dim = []
priority_queue = []
dictionary, dim = getDictionary()

# dua vao 1 van ban va tra ve [n] phan tu gan nhat trong mang
# moi lan xet lai doc lai file BoW.txt -> tranh truong hop file BoW qua lon 
# doc tung dong trong file BoW.txt
def cacl_distance(document, dictionary, priority_queue):
    # lay vector
    vector_list = []
    path_file = "dataprocessing/vector/BoW.txt"
    read_file = open(path_file, "r", encoding = 'utf-8')

    vector_string = read_file.readline()
    while vector_string:
        x = handleVector(vector_string)

        type_document = x["type"]
        point1 = x["vector"]
        point2 = convert_vector(document,dictionary)

        distance = euclidean_distance(point1, point2)
        item = {"type" : type_document, "value" : distance}
        enqueue(priority_queue, item)

        vector_string = read_file.readline()
        
    read_file.close()
    return priority_queue

# bat dau xu ly bo test
def handling(dictionary, priority_queue):
    # mo file de ghi ket qua
    path_file = "result/result.txt"
    write_file_result = open(path_file, "w", encoding = 'utf-8')

    # doc file de lay du lieu
    files_doc = open("path_file_dataset.txt", "r", encoding = 'utf-8')
    tmp = files_doc.read().split('\n',1)
    number_of_file = tmp[0] # lay so luong nhan
    file_doc = tmp[1].split('\n') # lay ten cua tung nhan
    
    index = 0
    for path_list in file_doc: # kiem tra tung loai van ban
        # doc du lieu tu van ban
        path_list = "dataset/test/" + path_list
        doc = open(path_list, "r", encoding = 'utf-8').read()
        arr_doc = doc.split('\n')

        run = 0 # bien run de gioi han viec lay so bai bao
        sum_true = 0
        for element_doc in arr_doc: # kiem tra tung van ban 
            priority_queue = cacl_distance(element_doc, dictionary, priority_queue)
            item = priority_queue[0]
            type_test = item["type"]
            
            if type_test == index:
                sum_true += 1

            if run == 10: # lay 11 bai bao trong moi nhan, bang viec chan bien run
                break
            run += 1
            
            priority_queue.clear()
        print("Ti le dung cua nhan thu ", index + 1, " la : ", sum_true/11 * 100, "%")
        write_file_result.write("Ti le dung cua nhan thu " + str(index + 1) + " la : " + str(sum_true/11 * 100) + "%" + "\n")
        index += 1 
        if index == number_of_file: # tranh truong hop doc phai ki tu khong hop le
            break
        
    write_file_result.close()

handling(dictionary, priority_queue)

