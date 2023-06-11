# %%
import json
import glob
import cv2
import matplotlib.pyplot as plt
import os

# %%
from sympy import sec
from shapely.geometry import Polygon
from shapely.strtree import STRtree

# %% [markdown]
# ## Global Object Variable

# %%
color = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 0, 255), (255, 255, 0), (255, 255, 255)]
disease = ['Bacteria', 'Blight', 'Leaf', 'Mold', 'Normal', 'Yellow_Virus']

# %% [markdown]
# ## Function Definition

# %%
def DrawBox(im, Box, color, disease, thickness):
    start_point = (Box['box'][0], Box['box'][1])   #(x,y)
    end_point = (Box['box'][2], Box['box'][3])    #(x + w ,y + h
    im = cv2.rectangle(im, start_point, end_point, color[Box['class']], thickness)
    return cv2.putText(im, disease[Box['class']] + ' ' + str(Box['score']), (Box['box'][0],Box['box'][1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color[Box['class']], 1, cv2.LINE_AA)

# %%
def DrawRec(img, boxes, color, thickness):
    for i in range(len(boxes)):
        img = cv2.rectangle(img, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]), color[boxes[i][5]], thickness)
        img = cv2.putText(img, str(i+1) + '.' + disease[boxes[i][5]]  + ' ' + str(boxes[i][6]), (boxes[i][0], boxes[i][1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color[boxes[i][5]]  , 1, cv2.LINE_AA)
    return img

# %%
def ShowImage(im):
    plt.figure()
    plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    plt.show() 

# %%
def Box_List(Box):
    b = []
    b.extend(Box["box"][:4])
    c = [int((Box['box'][0] + Box['box'][2])/2), int((Box['box'][1] +Box['box'][3])/2)]
    b.append(c)    
    b.extend([Box['class'], Box['score']])    
    return b

# %%
def box_sequence(boxes):
    return sorted(boxes, key=lambda x: (x[0], x[1]))
    #return sorted(boxes, key=lambda x: x[0])
    

# %%
def mergeBox(dat, tol):
    flag = True
    while (flag):
        flag = False
        sect = []
        for i in range(len(dat)-1):
            a = dat[i]
            b = dat[i+1]
            polys = [Polygon([(a[0], a[1]), (a[2] - tol, a[1]), (a[2]-tol, a[3]), (a[0], a[3])])]
            s = STRtree(polys)
            query_geom = Polygon([(b[0]+tol, b[1]+tol), (b[2], b[1]+tol), (b[2], b[3]), (b[0]+tol, b[3])])
            result = s.query(query_geom)
            sect.append(polys[0] in result)
        i = 0
        new_dat = []
        while(True):
            if (i < len(sect)):
                if sect[i]:
                    if dat[i][5] == dat[i+1][5]:
                        flag = True
                        x = min(dat[i][0], dat[i+1][0])
                        y = min(dat[i][1], dat[i+1][1])
                        w = max(dat[i][2], dat[i+1][2]) - min(dat[i][0], dat[i+1][0])
                        h = max(dat[i][3], dat[i+1][3]) - min(dat[i][1], dat[i+1][1])
                        c = (2*x + w)/2, (2*y + h)/2
                        if (dat[i][6] >= dat[i+1][6]):
                            classes = dat[i][5]
                            score = dat[i][6]
                        else:
                            classes = dat[i+1][5]
                            score = dat[i+1][6]
                        new_dat.append([x , y,  x+w, y+ h ,c, classes, score])
                        new_dat.extend(dat[i+2:])
                        break        
                    else:
                        new_dat.append(dat[i])
                        i += 1           
                else:
                    new_dat.append(dat[i])
                    i += 1
            else:
                new_dat.extend(dat[i:])
                break
        dat = new_dat 
    return dat

# %% [markdown]
# ## 1. Python read JSON file
# read the YOLO's results of classification

# %%
with open('data.json', 'r') as fp:
  data = json.load(fp)
print(data)
print(data['detections'])

# %% [markdown]
# ## Use Image Names to retrive Json data
# To retrive the reult's images

# %%
path = 'C:/Users/Rosary/Desktop/LeafDetectionProjectApp/images/'
keys = []
for name in glob.glob(path + '*.jpg'):
    # print(name)
    # keys.append(name.replace(path,""))
    filename = os.path.basename(name)
    keys.append(filename)
# keys=['image2.jpg']
# print(keys)

# %% [markdown]
# # 2. Manage Json Dictionary to specific pattern

# %%
spaces = []
for key in keys:
    span = dict()
    BoxList = []
    span['image'] = key
    span['results'] = list()
    bounds = data['detections'][key]
    print(bounds)
    img = cv2.imread(path+key)
    out = img.copy()
    for b in bounds:
        mDict = dict()
        mDict['box'] = [int(x) for x in b[:4]]
        mDict['class'] = (int(b[5]))
        mDict['score'] = round(b[4],2)
        out = DrawBox(out, mDict, color, disease, 1)
        BoxList.append(Box_List(mDict))
        span['results'].append(mDict)
    spaces.append(span)
    BoxList= box_sequence(BoxList)
    new_list = mergeBox(BoxList, 10)
    img = DrawRec(img, new_list, color, 1)

# %% [markdown]
# ## Write Json with the specific pattern

# %%
with open('boxs.json', 'w') as fp:
  json.dump(spaces, fp)

# %% [markdown]
# 

# %%
rows, columns =1, 2
fig = plt.figure()
fig.add_subplot(rows, columns, 1)
# plt.imshow(out)
plt.axis('off')
plt.title("Original Disease")
  
fig.add_subplot(rows, columns, 2)
# plt.imshow(img)
plt.axis('off')
plt.title("Cut off redundant desease")
  
# plt.show()
  

# %%
# ShowImage(img)

# %%
# ShowImage(out)

# %%
def calculate_disease_percentage(disease_counts):
    total = sum(disease_counts.values())
    disease_percentages = {}
    for disease_name, count in disease_counts.items():
        disease_percentages[disease_name] = round(count / total * 100, 2)
    return disease_percentages

disease_counts = {
    'Bacteria': 0,
    'Blight': 0,
    'Leaf': 0,
    'Mold': 0,
    'Normal': 0,
    'Yellow_Virus': 0
}

for space in spaces:
    for result in space['results']:
        disease_class = disease[result['class']]
        disease_counts[disease_class] += 1

disease_percentages = calculate_disease_percentage(disease_counts)
print("Disease Percentages:", disease_percentages)

# ตัวอย่างการแสดงผลลัพธ์เป็นเปอร์เซ็นต์
for disease_name, percentage in disease_percentages.items():
    print(f"{disease_name}: {percentage}%")

# %%

def plot_disease_percentages(disease_percentages):
    names = list(disease_percentages.keys())
    values = list(disease_percentages.values())

    plt.bar(names, values)
    plt.xlabel('Disease Types')
    plt.ylabel('Percentage')
    plt.title('Disease Percentages')
    plt.xticks(rotation=45)
    # plt.show()

plot_disease_percentages(disease_percentages)

# %%
with open('disease_percentages.json', 'w') as fp:
    json.dump(disease_percentages, fp)
print(disease_percentages)


