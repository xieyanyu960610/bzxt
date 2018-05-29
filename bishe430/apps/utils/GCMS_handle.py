
# coding: utf-8

# In[55]:


import numpy as np
import os

def GCMS_handle(sample_name, file_in, file_out_folder):
    file_name = os.path.split(file_in)[1]
    name = os.path.splitext(file_name)[0]
    file_length = len(sample_name)
    flag = file_name.find(sample_name)
    number = name[flag+file_length:]
    number = bytes(number,'utf-8')

    file_out = file_out_folder + '/' + file_name
    if os.path.exists(file_out):
        os.remove(file_out)

    f = open(file_in,'rb')
    f1 = open(file_out,'a')
    line = f.readline()
    number_flag = False
    read_flag = False
    while line:
        if line.find(b'm/z') != -1:
            if line.find(number) != -1:
                number_flag = True
        if number_flag and line.find(b'Chromatogram') != -1:
            number_flag = False
            read_flag = False
        if number_flag and line.find(b'Ret.Time') != -1:
            read_flag = True
            line = f.readline()
        if number_flag and read_flag:
            line_tmp = bytes.decode(line)
            f1.write(line_tmp)
        line = f.readline()
    f.close()
    f1.close()
    os.remove(file_in)
    return file_name

