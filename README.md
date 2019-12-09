## calculate webpage distance by information in skia
### 操作步骤

* 将爬虫获取的skp文件转化为txt文件，txt文件中存储了整个paint操作序列的json对象

* 合并所有layer的操作序列到一个文件中，并对操作序列进行预处理

  ``` python getData.py dirPath outdirPath```

* 将合并预处理后的txt文件当做网页的输入，对两个网页进行比较建图

  ```python buildGraph.py file1 file2```

  会在本地目录下生成一个outfile.txt的文件，表示图的拓扑结构以及权重的值

* 将outfile.txt作为code2文件下code2print.cpp的输入，编译之后执行可执行文件得到结果。