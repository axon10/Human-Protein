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
        soup = BeautifulSoup(file.read(), 'lxml')
         ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
        iterRows = iter(soup.find_all('tr'))
        for row in iterRows:
            cells = row.find_all('td')
            ### cells in row one/two should link to full IPR table.
            domain_id = cells[1].get_text()
            domain_name = cells[2].get_text()
            full_table_link = BeautifulSoup('<a href="../tables/' + domain_id +'.html">' + domain_name + "</a>", 'lxml').a
            cells[2].string = ""
            cells[2].append(full_table_link)
            for index, cell in enumerate(cells):
                if (index >= 3 and index <= 8):
                    col = str(index-2)
                    link = BeautifulSoup('<a href="../tables/'+ "col_" + col + "_" + domain_id +'.html">' + cell.get_text() + "</a>", 'lxml').a
                    cell.string = ""
                    cell.append(link)
                if index >= 10:
                    col = str(index-3)
                    link = BeautifulSoup('<a href="../tables/'+ "col_" + col + "_" + domain_id +'.html">' + cell.get_text() + "</a>", 'lxml').a
                    cell.string = ""
                    cell.append(link)
        ## update new css
        with open(template_with_script, 'r') as css_src:
          ## works because the script and the div are not imported to the index/
          style = BeautifulSoup(css_src.read(), 'lxml').find_all('style')[0]
          old_style = soup.find_all('style')[0]
          old_style.replace_with(style)
    print(str(soup))
    with open(index_file,'w+', encoding="utf-8") as new_index:
           new_index.write(str(soup))
           new_index.close()
 
####Given the full IPR table, it links the pdb to the full table, and it also links the full table and index back to the sub tables.
def initIPR(full_table_file, template_with_script):
   from bs4 import BeautifulSoup
   
   table_id = full_table_file.replace('.html', '').replace('./tables/', '')
   print(table_id)
   
   with open(full_table_file,'r') as file:
       
       raw_table = BeautifulSoup(file.read(), 'lxml')
       
       ## link all the pdb files 
       rows = raw_table.find_all('tr')
       for row in rows:
            cells = row.findChildren('td')
            pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cells[4].get_text() + "','" + cells[5].get_text() + "'" + ')" href="javascript:void(0);">' + cells[4].get_text() + '</a>', 'lxml').a
            cells[4].string = ""
            cells[4].append(pdb_link)
            
       ## import the script + table into the temp, also add links
            
       with open(template_with_script, 'r') as file:
          ## scrape the template
          final_full_table = BeautifulSoup(file.read(), 'lxml')
          
          ## add the div and make it fit
          final_full_table.head.append(BeautifulSoup('<style type="text/css"> #table-icm {width: 50%;}</style>').style)
          final_full_table.body.insert(2, BeautifulSoup('<div id="con"></div>'))
          
          ## link table
          final_full_table.body.insert(3, raw_table.find_all('table')[0])
          for script in raw_table.find_all('script'):
              print(str(script))
              final_full_table.body.append(script)
              
      # done editing, now save the soup
       with open(full_table_file,'w+', encoding="utf-8") as file:
           file.write(str(final_full_table))

       ### now also open the sub tables
       column_number = 1
       while (column_number <= 7):
           ## open the table file
            with open('./tables/' + 'col_' + str(column_number) + '_' + table_id + '.html','r', encoding="utf-8") as old_file:
                print(str(file))
                
                table_file = BeautifulSoup(old_file.read(), 'lxml')
                
                ### load the template style and initial headers
                with open(template_with_script, 'r') as style_src:
                    full_file = BeautifulSoup(style_src.read(), 'lxml')
                     ## also link back to table
                    full_table_link = BeautifulSoup('<a href="./tables/' + table_id + '.html"' + '>' + dictionary(table_id, './ICMEssential/ip_distribution.csv') + "</a>", 'lxml')
                    full_file.body.insert(2, full_table_link)                    
                if (column_number == 6):
                        ## make page fit to width
                        full_file.body.append(BeautifulSoup('<style type="text/css"> #table-icm {width: 50%;}</style>').style)
                        ## add the pdb
                        full_file.body.insert(4, BeautifulSoup('<div id="con"></div>').div)                          
                        ## insert the table links into soup
                        rows = table_file.find_all('tr')
                        for row in rows:
                            cells = row.findChildren('td')
                            pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cells[7].get_text() + "','" + cells[5].get_text() + "'" + ')" href="javascript:void(0);">' + cells[7].get_text() + '</a>', 'lxml').a
                            cells[7].string = ""
                            cells[7].append(pdb_link)
                        full_file.body.insert(5, table_file.find_all('table')[0])
                else:
                    ## insert the table at a diff position
                    full_file.body.insert(4, table_file.find_all('table')[0])
                ## append moledit, sortable, and chemview scripts to bottom of body
                for script in table_file.find_all('script'):
                     full_file.body.append(script)
            with open('./tables/' + 'col_' + str(column_number) + '_' + table_id + '.html','w+', encoding="utf-8") as new_file:
                new_file.write(str(full_file))
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

initIndex('./ICMEssential/ip_distribution.html', './ICMEssential/basicTemplate.html')
clean_page('./ICMEssential/ip_distribution.html')

for root, dirs, files in os.walk('./tables'):
    for file_name in files:
       ###basically if it is a file of format IPR000276.html
       if '_' not in file_name and 'html' in file_name and 'IPR' in file_name:
           clean_page('./tables/' + file_name)
           ### Full table, initialize links to subtables and back to home.
           initIPR('./tables/' + file_name, './ICMEssential/basicTemplate.html')
           

#openIndex()

                                          

