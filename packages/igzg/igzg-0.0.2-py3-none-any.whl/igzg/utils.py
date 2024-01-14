__version__ = '0.0.0'

def getConfig(configList:list, section:str="DEFAULT", configFilePath:str='config.txt'):
    import configparser
    config = configparser.ConfigParser()

    def handleError(e:Exception):
        print('config.txt파일 오류')
        writeError(e)
        return False        

    for enc in ['utf-8','cp949']:
        try:
            config.read(configFilePath,encoding=enc)
            resList = [config[section][x] for x in configList]
            return resList
        except UnicodeDecodeError as e:
            decDrror = e
            continue
        except Exception as e: 
            return handleError(e)
    else:
        return handleError(decDrror)


def getNowStr(format:str = "%Y-%m-%d %H:%M:%S"):
    from datetime import datetime
    nowStr = datetime.now().strftime(format)

    return nowStr


def writeError(e:Exception, errorFilePath:str='error.txt', consoleLogging:bool=False):
    import traceback
    errLog = f"""{getNowStr()}
    [{type(e).__name__}] - {e.__doc__}
    function: {e.__traceback__.tb_frame.f_code.co_name}({e.args})
    traceback: {traceback.format_exc()}
    """
    fwrite(errLog, errorFilePath)
    if consoleLogging:
        print(errLog)


def fwrite(text, filePath:str="output.txt", encoding:str=None):
    def handleError(e:Exception):
        if e: writeError(e)
        return False

    text = str(text)
    textStr = text + '\n' if (not text) or (text[-1] != '\n') else text
    encList = [encoding] if encoding else ['utf-8','cp949']

    encError = None
    for enc in encList:
        try:
            with open(filePath, 'a', encoding=enc) as f:
                f.write(textStr)
            break
        except UnicodeEncodeError as e: 
            encError = e
            continue
        except Exception as e: 
            handleError(e)
            break
    else:
        handleError(encError)


if __name__ == "__main__":
    ...