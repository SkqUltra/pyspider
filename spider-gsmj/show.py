# -*- coding:utf-8 -*-
import time
import matplotlib.pyplot as plt
import numpy as np

from pymongo import MongoClient

num = 0
yun = []
ind = []
pipeline = [{"$group": {"_id": "$index", "count": {"$sum": 1}}}]
client = MongoClient('mongodb://127.0.0.1:27017/')
data = client.gs.gsmj.aggregate(pipeline)

fig, ax = plt.subplots(figsize = (14,7))

for a in data:
	plt.bar(num, a['count']) 
	plt.text(num, a['count']+0.05, '%.0f' % a['count'], ha='center', va= 'bottom',fontsize=7)
	yun.append(a['_id'])
	ind.append(num)
	num += 1

ax.set_xticks(ind)
ax.set_xticklabels(yun)

plt.show()