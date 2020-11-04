import re


class FileManager:

    def __init__(self, relativepath, Lfiles, logger):
        self.__logger = logger
        self.__LFiles_to_process = []
        self.__Linfo = []
        for file in Lfiles:
            self.__LFiles_to_process.append("{0}{1}".format(relativepath,file))

    def run(self):
        for file in self.__LFiles_to_process:
            f_opened = open(file)
            print "reading: {0}".format(file)
            self.__logger.info("reading: {0}".format(file))
            self.__processLines(f_opened.read())


    def __processLines(self,f_opened):
        start = f_opened.find('select ') + 6
        to_from = f_opened.find('from ', start)
        columns_select_raw = f_opened[start:to_from]
        L_lines_raw = columns_select_raw.replace('\n', '').split(',')
        L_columns_parsed=[]
        for a in L_lines_raw:
            if '\'' in a.strip():
                L_columns_parsed.append(a.split('\'')[1].strip())
            else:
                L_columns_parsed.append(a.strip().split(' ')[0])
        columns_clean = ','.join(L_columns_parsed)
        from_from = f_opened.find('from ') + 5
        source_table_raw = f_opened[from_from:len(f_opened)]
        source_table = source_table_raw.split('\'')[-2]
        self.__Linfo.append(source_table+': '+columns_clean)

    def getInfo(self):
        return self.__Linfo



