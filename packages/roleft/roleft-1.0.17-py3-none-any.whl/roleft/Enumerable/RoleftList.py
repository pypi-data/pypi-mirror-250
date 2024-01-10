from typing import Dict, List, Generic, MutableSequence, TypeVar, Callable, Union
import copy

from roleft.Entities.RoleftKeyValue import KeyValue


T = TypeVar('T')
TOut = TypeVar('TOut')

# class xList(MutableSequence[T], Generic[T]):
class xList(Generic[T]):
    # def __init__(self, list: List[T] = []) -> None:
    #     self.__items: List[T] = list
    
    # 来自 chatgpt: 这是因为在 Python 中，函数默认参数的默认值在函数定义时被计算，
    # 而不是每次函数调用时重新计算。对于可变对象（如列表、字典等），
    # 如果将其作为默认参数，它只会在函数定义时被创建一次，并且之后所有调用该函数的实例都会共享同一个默认对象。
    def __init__(self, list: List[T] = []) -> None:
        self.__items: List[T] = list if len(list) > 0 else []

    def Add(self, item: T):
        self.__items.append(item)
        return self
    
    def AddRange(self, others: list[T]):
        self.__items += others
        return self
        
    def RemoveAt(self, index: int):
        del self.__items[index] # 【闻祖东 2023-07-26 102651】其实 self.__items.pop(index) 也可以
    
    def Remove(self, item: T):
        self.__items.remove(item)
    
    def Exists(self, predicate: Callable[[T], bool]) -> bool:
        for x in self.__items:
            if (predicate(x)):
                return True
            
        return False
    
    def Count(self):
        return len(self.__items)
    
    def Clear(self):
        self.__items = []
    
    def FindAll(self, predicate: Callable[[T], bool]):
        lst: List[T] = []
        for x in self.__items:
            if (predicate(x)):
                lst.append(x)
            
        return xList(lst)
    
    def First(self, predicate: Callable[[T], bool]):
        newItems = self.FindAll(predicate).ToList()
        return newItems[0] if len(newItems) > 0 else None
    
    def FirstIndex(self, predicate: Callable[[T], bool]):
        index = 0
        for x in self.__items:
            if (predicate(x)):
                return index
            index += 1
        
        return -1
    
    def ToList(self):
        return self.__items
    
    def ForEach(self, predicate: Callable[[T], None]):
        for x in self.__items:
            predicate(x)
    
    def Select(self, predicate: Callable[[T], TOut]):
        newList = []
        for x in self.__items:
            temp = predicate(x)
            newList.append(temp)
        
        return xList(newList)
    
    def OrderBy(self, predicate: Callable[[T], str]):
        kts = self.Select(lambda x: KeyValue(predicate(x), x))
        keys = kts.Select(lambda x: x.key).ToList()
        keys.sort()

        newList = list()
        newItems = copy.deepcopy(self.__items)
        for key in keys:
            index = self.FirstIndex(lambda x: key == predicate(x))
            newList.append(newItems[index])
            self.RemoveAt(index)
        
        return xList(newList)
    
    def InsertAt(self, item: T, index: int):
        self.__items.insert(index, item)
    
    def RemoveAll(self, predicate: Callable[[T], bool]):
        indexes = list[int]()
        index = 0
        for item in self.__items:
            if (predicate(item)):
                indexes.append(index)
            index += 1
        
        indexes.reverse()
        for idx in indexes:
            self.RemoveAt(idx)
    
    def Print(self):
        print(self.__items)
