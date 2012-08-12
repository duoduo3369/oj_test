'''
Created on 2012-8-10

@author: duoduo
'''
from oj.constant import MARK_SEPARATOR
def get_string_with_mark_separator(input_string,item_tuple , mark_sp = MARK_SEPARATOR):
    """
        item_tuple = [(),(),()]
    """
    input_string = str(input_string)

    id_strs = input_string.split(MARK_SEPARATOR)
    output_list = []
    #somethin like [(1,input),(2,output)]
    for id_s in id_strs:
        for item in item_tuple:
            if str(item[0]) == id_s:
                output_list.append(item)
    
    return output_list

 