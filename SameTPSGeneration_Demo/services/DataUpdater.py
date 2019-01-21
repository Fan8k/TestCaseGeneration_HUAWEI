#coding=utf-8

'''
数据修改器：专门负责修改对应rule所匹配的数据
'''

class DataUpdater:

    @classmethod
    def change_strValue(self,pri_str,change_points_location):

        '''
        修改相应的满足条件的位置的信息
        :param pri_str: 原型组的item的response信息
        :param change_points_location: 修改点的位置
        :return:
        '''
        temp = []
        for index,char in enumerate(pri_str):
               #前提是有需要修改的点进来才行
               if len(change_points_location)>0:
                 if change_points_location[0][0] <= index and index < change_points_location[0][1]:
                   if index == change_points_location[0][0]:
                     temp.extend(change_points_location[0][2])
                   if index+1 == change_points_location[0][1]:
                     del change_points_location[0]
                 else:
                     temp.append(pri_str[index])
               else:
                  temp.append(pri_str[index])
        return "".join(temp)


    @classmethod
    def change_strValues(self, pri_str, change_points_location):

        '''
        只有多点匹配可能碰到冲突，所以先消除冲突，找出所有满足不冲突且全部修改点都覆盖到的修改位置信息
        :param pri_str: 原型组的item的response信息
        :param change_points_location: 修改点的位置
        :return: 返回所有满足要求的修改response
        '''
        for _change_points_location in DataUpdater._clear_clash(change_points_location):

            all_rules = [_change_points_location[i][3] for i in range(len(_change_points_location))]
            temp = []
            for index, char in enumerate(pri_str):
                # 前提是有需要修改的点进来才行
                if len(_change_points_location) > 0:
                    if _change_points_location[0][0] <= index and index < _change_points_location[0][1]:
                        if index == _change_points_location[0][0]:
                            temp.extend(_change_points_location[0][2])
                        if index + 1 == _change_points_location[0][1]:
                            del _change_points_location[0]
                    else:
                        temp.append(pri_str[index])
                else:
                    temp.append(pri_str[index])
            yield ("".join(temp),all_rules)


    @classmethod
    def _clear_clash(cls,change_points_location):
        '''
        消除修改过程的冲突
        :param change_points_location: [(start,stop,aim_value)]
        :return: 满足所有修改且不冲突的位置及其修改信息
        '''
        _clash_info = DataUpdater._extract_clash([(item[0],item[1]) for item in change_points_location])
        if _clash_info == None:
            yield change_points_location
        else:
            #记住那些位置是出现冲突的
            _clash_points = []
            print(_clash_info)
            for _key,_values in _clash_info.items():
                if len(_values)>0:
                    _clash_points.append(_key)
            results = []
            temp_results = []
            DataUpdater._clear(_clash_info,_clash_points,results,temp_results,0,len(_clash_points),50)
            for i in results:
                # 每一种结果就是一种组合方式
                mark_label = [1 for _ in range(len(change_points_location))]
                for _index, j in enumerate(i):
                    if j == 0:
                        mark_label[_clash_points[_index]] = 0
                _temp_change_points_location = []
                for _index,_mark in enumerate(mark_label):
                   if _mark==1:
                     _temp_change_points_location.append(change_points_location[_index])
                yield _temp_change_points_location
        return None

    @classmethod
    def _clear(cls,_clash_info,clash_index_map,results,temp_results,index,_len,num):
        '''
        这个方法只把有冲突的位置进行消除，没有冲突的位置是肯定会修改的位置
        :param _clash_info: 一定包含冲突位置信息 []
        :param results: 所有冲突的组合信息
        :param temp_results:
        :param index: 冲突的个数
        :param _len: 冲突的位置的个数
        :return:
        '''
        # 加入num限制
        if len(results) >= num:
            return

        indexs = []
        _clash_points = []
        for j, value in enumerate(temp_results):
            if value == 1:
                _clash_points.extend(_clash_info[clash_index_map[j]])
                indexs.append(clash_index_map[j])

        if index == _len:
            #清除不满足要求的组合
            _temp = set(indexs).union(set(_clash_points))
            if len(_temp) == _len:
                results.append(temp_results.copy())

        else:
            for i in range(1, -1, -1):
                temp_results.insert(index, i)
                # 增加剪枝操作
                indexs = []
                _clash_points = []
                for j, value in enumerate(temp_results):
                    if value == 1:
                        _clash_points.extend(_clash_info[clash_index_map[j]])
                        indexs.append(clash_index_map[j])

                _temp = set(indexs).intersection(set(_clash_points))
                if len(_temp) == 0 and len(results)<num:
                    DataUpdater._clear(_clash_info,clash_index_map,results, temp_results, index + 1, _len,num)
                del temp_results[index]

    @classmethod
    def _clear_deprecate(cls,_clash_info,results,temp_results,index,_len):
        if index == _len:
            indexs = []
            _clash_points = []
            for j, value in enumerate(temp_results):
                if value == 1:
                    _clash_points.extend(_clash_info[j])
                    indexs.append(j)
            _temp = set(indexs).union(set(_clash_points))
            if len(_temp)== _len:
               results.append(temp_results.copy())
        else:
           for i in range(1,-1,-1):
               temp_results.insert(index,i)
               #增加剪枝操作
               indexs = []
               _clash_points = []
               for j,value in enumerate(temp_results):
                   if value ==1:
                       _clash_points.extend(_clash_info[j])
                       indexs.append(j)
               _temp = set(indexs).intersection(set(_clash_points))

               if len(_temp)==0:
                  DataUpdater._clear(_clash_info,results,temp_results,index+1,_len)

               del temp_results[index]

    @classmethod
    def _extract_clash(cls,change_points):
        '''
        提取冲突信息 {节点_index:[冲突点_indexs]}
        :param change_points: [(start,end)] 这个必须是有序的 按照start排序
        :return: 返回冲突信息
        '''
        clash_info = {}
        for i in range(len(change_points)):
            _clash_points = []
            for index in range(i+1,len(change_points)):
               #当前修改点的end坐标
               curent_end_axis = change_points[i][1]
               start_axis = change_points[index][0]
               if start_axis < curent_end_axis:
                  #加入冲突点信息
                  _clash_points.append(index)
                  #前冲突点
                  if clash_info.get(index) ==None:
                      clash_info[index] = [i]
                  else:
                      clash_info[index].append(i)
               else:
                   break
            if clash_info.get(i) == None:
               clash_info[i] = _clash_points
            else:
               clash_info[i].extend(_clash_points)
        #判断是否有冲突
        _isclash = False
        for _v in clash_info.values():
            #只要一个节点有冲突元素
            if len(_v)>0:
                _isclash = True
                break
        return  clash_info if _isclash  else None


