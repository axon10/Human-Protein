import csv
import os
from html import escape
import io
import time
import webbrowser
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
            if row[1] == ipr_code:
               return row[2]

def giveTitleToHTML(table_file, table_id):
    from bs4 import BeautifulSoup
    # Open the file template and establish soup connection
    # Copy the template and close the connection
    with open(table_file, 'r') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    table = soup.find_all('table')[0]

    # just for presentation
    table_name = soup.new_tag('h1')
    table_name.string = dictionary(table_id, './ICMEssental/ip_distribution.csv')
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


def initIndex(index_file, template_with_script):
    from bs4 import BeautifulSoup
    ### open up the index, and find all of the items to link
    with open(index_file, 'r') as file:
        soup = BeautifulSoup(file.read()).find_all('table')[0]
    iterRows = iter(soup.find_all('tr'))
    ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
    for row in iterRows:
        cells = row.find_all('td')
        ### cells in row one/two should link to full IPR table.
        domain_id = cells[1].get_text()
        domain_name = cells[2].get_text()
        full_table_link = BeautifulSoup('<a href="../tables/' + domain_id +'.html">' + domain_name + "</a>", 'lxml').a
        cells[2].string = ""
        cells[2].append(full_table_link)
        
        for index, cell in enumerate(cells):
            if index >= 3 :
                col = str(index+1)
                link = BeautifulSoup('<a href="../tables/'+ "col_" + col + "_" + domain_id +'.html">' + cell.get_text() + "</a>", 'lxml').a
                cell.string = ""
                cell.append(link)
    with open(template_with_script, 'r') as file:
          final_full_table = BeautifulSoup(file.read(), 'lxml')
          final_full_table.body.insert(1, soup)
    print(str(final_full_table))
    with open(index_file,'w+', encoding="utf-8") as file:
           file.write(str(final_full_table))
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
       rows = raw_table.find_all('tr')
       for row in rows:
            cells = row.findChildren('td')
            pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cells[4].get_text() + "','" + cells[5].get_text() + "'" + ')" href="javascript:void(0);">' + cells[4].get_text() + '</a>', 'lxml').a
            cells[4].string = ""
            cells[4].append(pdb_link)          
       with open(template_with_script, 'r') as file:
          final_full_table = BeautifulSoup(file.read(), 'lxml')
          final_full_table.body.insert(1, raw_table.find_all('table')[0])
          final_full_table.body.insert(1, raw_table.find_all('script')[0])
          final_full_table.body.insert(1, raw_table.find_all('script')[1])                              
      # done editing, now save the soup
       with open(full_table_file,'w+', encoding="utf-8") as file:
           file.write(str(final_full_table))

   ### now also open the sub tables

       column_number = 4
       while (column_number < 8):
            with open('./tables/' + 'col_' + str(column_number) + '_' + table_id + '.html','r', encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), 'lxml')
                full_table_link = BeautifulSoup('<a href="./tables/' + table_id + '.html"' + '>' + dictionary(table_id, './ICMEssential/ip_distribution.csv') + "</a>", 'lxml').a
                soup.html.insert(0,full_table_link)
                soup.html.append(BeautifulSoup('<a href="../ICMEssential/ip_distribution.html"' + '>INDEX</a>').a)
                if (column_number == 6) :
                    ### load the scripts for pdb and insert into soup
                    with open(template_with_script, 'r') as file:
                          scripts = BeautifulSoup(file.read(), 'lxml').find_all('script')
                          for script in scripts:
                              soup.body.insert(1, script)
                    ## then load the pdb links in each row
                    rows = soup.find_all('tr')
                    for row in rows:
                        cells = row.findChildren('td')
                        pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cells[5].get_text() + "','" + cells[7].get_text() + "'" + ')" href="javascript:void(0);">' + cells[5].get_text() + '</a>', 'lxml').a
                        cells[5].string = ""
                        
                        print(str(pdb_link))
                        cells[5].append(pdb_link)
            with open('./tables/' + 'col_' + str(column_number) + '_' + table_id + '.html','w+', encoding="utf-8") as file:
                file.write(str(soup))
            column_number += 1
            
def clean_page(web_page):
    from bs4 import BeautifulSoup
    ### open up the index, and find all of the items to link
    with open(web_page, 'r') as file:
        soup = BeautifulSoup(file.read())    
        header = iter(soup.find_all('th'))
    ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
        for name in header:
            name.string = name.get_text().replace("_", " ")
        with open(web_page,'w+', encoding="utf-8") as file:
           file.write(str(soup))
           file.close()

#initIndex('./ICMEssential/ip_distribution.html', './ICMEssential/basicTemplate.html')
# clean_page('./ICMEssential/ip_distribution.html')

for root, dirs, files in os.walk('./tables'):
    for file_name in files:
       clean_page('./tables/' + file_name)
       if '_' not in file_name:
         print("GPCR")
          ### Full table, initialize links to subtables and back to home.
         initIPR('./tables/' + file_name, './ICMEssential/basicTemplate.html')

#openIndex()
                                          

