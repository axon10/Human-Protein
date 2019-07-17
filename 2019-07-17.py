import csv
import os
from html import escape
import io
import time
import webbrowser
import pyautogui
import datetime
# This program creates html(web) files from csv (data) files within a subdirectory, and links it to an index page, which it then opens.
# Beautiful Soup is a tool used to copy-paste the csv data in table form, into a basic template used for all database web files.

def dictionary(ipr_code, lookup_file):
    with open(lookup_file, newline='', encoding = "utf-8") as f:
    	# why newline='': see footnote at the end of https://docs.python.org/3/library/csv.html
        reader = csv.reader(f)
        # get the column names
        iterRows = iter(reader)
        for row in iterRows:
            if row[0] == ipr_code:
               return row[1]

def giveTitleToHTML(table_file, table_id):
    from bs4 import BeautifulSoup
    # Open the file template and establish soup connection
    # Copy the template and close the connection
    with open(table_file, 'r') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    table = soup.find_all('table')[0]

    # just for presentation
    table_name = soup.new_tag('h1')
    table_name.string = dictionary(table_id)
   # Provide a table name (presentation purposes)
    soup.body.insert(1,table_name)

    # Save the table file with the new name.
    with open(table_file, 'w', encoding="utf-8") as file:
        file.write(str(soup))
        file.close()
        print('PASSED INSERT TABLE')
    #Change path to reflect file location
    ### scriptDirectory = os.path.dirname(__file__)
    ### Concatenate script directory with location of new file created.
    ### relativeWebFileName = relativeTableSourceFile.replace('csv', 'html').replace('DataFiles', 'WebFiles')
    ###  webbrowser.open_new_tab('file://' + os.path.join(scriptDirectory, relativeWebFileName.replace('./', '')))


def initIndex(index_file):
    from bs4 import BeautifulSoup
    ### open up the index, and find all of the items to link
    with open(index_file, 'r') as file:
        soup = BeautifulSoup(file.read())    
    iterRows = iter(soup.find_all('tr'))
    ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
    for row in iterRows:
        cells = row.find_all('td')
        ### cells in row one/two should link to full IPR table.
        domain_id = cells[0].get_text()
        domain_name = cells[1].get_text()
        full_table_link = BeautifulSoup('<a href="../tables/' + domain_id +'.html">' + domain_name + "</a>", 'lxml').a
        cells[1].string = ""
        cells[1].append(full_table_link)
        ### cells in row 4 should link to pcih
        pcih_link = BeautifulSoup('<a href="../tables/'+ domain_id +'_pcih.html">' + cells[3].string + "</a>", 'lxml').a
        cells[3].string = ""
        cells[3].append(pcih_link)
        ## row 5 is pcipdb
        pcipdb_link = BeautifulSoup('<a href="../tables/'+ domain_id +'_pcipdb.html">' + cells[4].string + "</a>", 'lxml').a
        cells[4].string = ""
        cells[4].append(pcipdb_link)

        pdb_lig_link = BeautifulSoup('<a href="../tables/'+ domain_id +'_pdb_lig.html">' + cells[5].string + "</a>", 'lxml').a
        cells[5].string = ""
        cells[5].append(pdb_lig_link)

        protein_lig_link = BeautifulSoup('<a href="../tables/'+ domain_id +'_protein_lig.html">' + cells[6].string + "</a>", 'lxml').a
        cells[6].string = ""
        cells[6].append(protein_lig_link)

        lig_count_link = BeautifulSoup('<a href="./tables/'+ domain_id +'_lig_count.html">' + cells[7].string + "</a>", 'lxml').a
        cells[7].string = ""
        cells[7].append(lig_count_link)
        
    print(str(soup))
    with open(index_file,'w+', encoding="utf-8") as file:
           file.write(str(soup))
           file.close()
 

####Given the full IPR table, it links the pdb to the full table, and it also links the full table and index back to the sub tables.
def initIPR(full_table_file, template_with_script):
   table_id = full_table_file.replace('.html', '').replace('./tables/', '')
   print(table_id)
   from bs4 import BeautifulSoup
   with open(full_table_file,'r') as file:
       raw_table = BeautifulSoup(file.read(), 'lxml')
       ### link the full table back to home 
       new_link = raw_table.new_tag('a', href = 'ip_distribution.html')
       new_link.string = "INDEX"
       raw_table.body.append(new_link)
       rows = raw_table.find('table').findChildren(['tr'])
       for row in rows:
            cells = row.findChildren('td')
##            for cell in cells:
##               value = cell.string
##               print("The value in this cell is %s" % value)
            pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cells[3].get_text() + "','" + cells[2].get_text() + "'" + ')" href="javascript:void(0);">' + cells[3].get_text() + '</a>', 'lxml').a
            cells[3].string = ""
            cells[3].append(pdb_link)
                        
       with open(template_with_script, 'r') as file:
          final_full_table = BeautifulSoup(file.read(), 'lxml')
          final_full_table.body.insert(1, raw_table.find_all('table')[0])
          final_full_table.body.insert(1, raw_table.find_all('script')[2])
                                    
      # done editing, now save the soup
       with open(full_table_file,'w+', encoding="utf-8") as file:
           file.write(str(final_full_table))
           file.close()
 
       ### now also open the sub tables
       with open('./tables/' + table_id + '_pcih.html','r', encoding="utf-8") as file:
           soup = BeautifulSoup(file.read(), 'lxml')
           full_table_link = BeautifulSoup('<a href="./tables' + table_id + '"' + '>' + dictionary(table_id, 'ip_distribution.csv') + "</a>", 'lxml').a
           soup.html.insert(0,full_table_link)
           soup.html.append(BeautifulSoup('<a href="'+ table_id + '"' + '>INDEX</a>').a)
       with open('./tables/' + table_id + '_pcipdb.html','r', encoding="utf-8") as file:    
           soup = BeautifulSoup(file.read(), 'lxml')
           full_table_link = BeautifulSoup('<a href="./tables' + table_id + '"' + '>' + dictionary(table_id, 'ip_distribution.csv') + "</a>", 'lxml').a
           soup.html.insert(0,full_table_link)
           soup.html.append(BeautifulSoup('<a href="'+ table_id + '"' + '>INDEX</a>').a)
       with open('./tables/' + table_id + '_pdb_lig.html','r', encoding="utf-8") as file:
           soup = BeautifulSoup(file.read(), 'lxml')
           full_table_link = BeautifulSoup('<a href="./tables' + table_id + '"' + '>' + dictionary(table_id, 'ip_distribution.csv') + "</a>", 'lxml').a
           soup.html.insert(0,full_table_link)
           soup.html.append(BeautifulSoup('<a href="'+ table_id + '"' + '>INDEX</a>').a)
       with open('./tables/' + table_id + '_protein_lig.html','r') as file:                                
           soup = BeautifulSoup(file.read())
           full_table_link = BeautifulSoup('<a href="./tables' + table_id + '"' + '>' + dictionary(table_id, 'ip_distribution.csv') + "</a>", 'lxml').a
           soup.html.insert(0,full_table_link)
           soup.html.append(BeautifulSoup('<a href="'+ table_id + '"' + '>INDEX</a>').a)
       with open('./tables/' + table_id + '_lig_count.html','r', encoding="utf-8") as file:                                
           soup = BeautifulSoup(file.read(), 'lxml')
           full_table_link = BeautifulSoup('<a href="./tables' + table_id + '"' + '>' + dictionary(table_id, 'ip_distribution.csv') + "</a>",'lxml').a
           soup.html.insert(0,full_table_link)
           soup.html.append(BeautifulSoup('<a href="'+ table_id + '"' + '>INDEX</a>').a)        

initIndex('./ICMEssential/ip_distribution.html')
for root, dirs, files in os.walk('./tables'):
    for file_name in files:
       if '_' not in file_name:
          ### Full table, initialize links to subtables and back to home.
          initIPR('./tables/' + file_name, './ICMEssential/basicTemplate.html')
##openIndex()
                                          

