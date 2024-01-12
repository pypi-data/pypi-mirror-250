__version__ = '0.0.0'

#test
def getInsertQuery(tableName:str, dataDict:dict, duplicateUpdate:bool=False, updateItems:list=[])->str:
    query = ''
    itemStr = ','.join(['`'+str(x)+'`' for x in list(dataDict.keys())])
    valueStr= ','.join(["'"+str(x)+"'" for x in list(dataDict.values())])

    if duplicateUpdate:
        updateStr = ','.join(["`"+str(x)+"`='"+str(dataDict[x])+"'" for x in updateItems])
        query = rf"""INSERT INTO `{tableName}` ({itemStr}) VALUES ({valueStr}) ON DUPLICATE KEY UPDATE {updateStr};"""
    else:
        query = rf"""INSERT INTO `{tableName}` ({itemStr}) VALUES ({valueStr});"""

    return query