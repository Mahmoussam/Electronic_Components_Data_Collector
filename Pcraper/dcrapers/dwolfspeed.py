from .common_imports import *
logger = logging.getLogger(__name__)

class DSWolfSpeedMOS():
    '''
    Doc scrapper for wolfspeed datasheets
    specficially for mosfets data..
    '''
    def __init__(self):
        self.ignore_headers_list = ['symbol' , 'unit' ,'note','']
        pass
    def __get_tables(self , pdf):
        tables = camelot.read_pdf(pdf,
                          pages="1-3",
                          flavor="lattice")
        return tables
    def __sieve_table(self , table , idx , header = False):
        '''
        Parses first type of tables
        was useful till i discovered that there are two structures of documents (atleast!)
        '''
        if idx > 3:
            logger.error('unexpected Talbe to be parsed [%d]' , idx)
            return []
        data = table.data
        sz = len(data)
        result = []
        #print(data)
        for i in range( 0 if header else 1 , sz):
            row = [ '' , '' , '' , '' , '']
            if data[i][0] == '':
                #ignore it for now..
                continue
            if idx < 2:
                # Key parameters , Electrical Ch/cs
                # [Parameter , min , typ , max , conditions]
                # [0         , 2   , 3   ,  4   , 6]
                row[0] = data[i][0]
                row[1] = data[i][2]
                row[2] = data[i][3]
                row[3] = data[i][4]
                row[4] = data[i][6]
            elif idx == 2:
                # Reverse Diode characteristics
                # [Parameter , typ , max , condtitions]
                # [ 0 ,         2 ,    3 ,   5]
                #=>[0 ,        3   ,  4     6]
                row[0] = data[i][0]
                row[2] = data[i][2]
                row[3] = data[i][3]
                row[4] = data[i][5]
            elif idx == 3:
                # Thermal characteristics
                # [Parameter , Typ]
                #cols : 0 , 2 =>
                #  [ 0 ,    3]
                row[0] = data[i][0]
                row[2] = data[i][2]
            for z in range(5):
                row[z] = row[z].replace('\u2014', '') 
            result.append(row)
            
        return result
    def __clean_header(self , head):
        new_head = []
        for x in head:
            z = x.strip().lower().replace('test' , '').split('\n')
            for token in z:
                ts = token.strip()
                if ts != '':
                    if ts[-1] == '.':
                        ts = ts[:-1]
                    new_head.append(ts)
        return new_head
    def __get_table_headers(self , table):
        head = table.data[0]
        head = self.__clean_header(head)
        #print('?' , head)
        head = [x.replace('Test' , '').lower().strip() for x in head if x.lower().strip() not in self.ignore_headers_list]
        return head
    def __parse_table(self , table , headers):
        data = table.data
        frag_head = self.__clean_header(data[0])
        hsz = len(headers)
        w = len(frag_head)
        
        #build a list that holds real position(column) in the big final table for each column in current table
        final_pos = [-1 for i in range(w)]
        for i in range(w):
            if frag_head[i] in headers:
                idx = headers.index(frag_head[i])
                final_pos[i] = idx
        #now build the rows! FOR THE NATION..
        #print(final_pos)
        #print(frag_head)
        result = []
        for j in range(1 , len(data)):
            if data[j][0] == '':
                continue#ignore for now , must be the case of same parameter different condition 
            drow = data[j]
            row = ['' for i in range(hsz)]
            for i in range(w):
                if final_pos[i] == -1:
                    continue
                row[final_pos[i]] = drow[i]
            #print(drow)
            #print(row)
            result.append(row)
        return result
                
    def scrap(self , pdf , writer):
        '''
        Scraps the data sheet,writing  target tables to data writer
        takes `pdf` which is a file-like obj (or a file name hehe)
        '''
        logger.info("scrapping pdf data sheet of mosfet ")
        
        tables = self.__get_tables(pdf)
        #print('got ',len(tables) )
        headers = []
        for i , table in enumerate(tables):
            h2 = self.__get_table_headers(table)
            for h in h2:
                if h not in headers:
                    headers.append(h)
        sz = len(headers)
        #print(headers)
        writer.write_row(headers)
        for i , table in enumerate(tables ):
            block = self.__parse_table(table ,headers)
            writer.write_rows(block)
        pass
