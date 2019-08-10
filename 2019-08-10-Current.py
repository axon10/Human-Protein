import csv
import os
from html import escape
import io
import time
import webbrowser
import datetime


raw_table_src_dir = "./tables/"
final_table_src_dir = "./pages/"

# This program creates html(web) files from csv (data) files within a subdirectory, and links it to an index page, which it then opens.
# Beautiful Soup is a tool used to copy-paste the csv data in table form, into a basic template used for all database web files.
def openIndex(index_file):
    webbrowser.open(index_file, new = 2)

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
    table_name.string = dictionary(table_id, 'index.csv')
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

def restyle(style_file,  raw_file):
    from bs4 import BeautifulSoup
    with open(style_file, 'r') as style_src:
        new_style = BeautifulSoup(style_src.read(), 'lxml').find_all('style')[0]
        with open(raw_file, 'r') as new_file:
            new_file = BeautifulSoup(raw_file.read(), 'lxml')
        new_file.find_all('style')[0].replace_with(style)
    with open(raw_file, 'w+') as new_style:
        new_style.write(str(new_file))       
def initIndex(index_file, template_with_script):
    from bs4 import BeautifulSoup
    ### open up the index, and find all of the items to link
    with open(index_file, 'r') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
         ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
        iterRows = iter(soup.find_all('tr'))
        for row in iterRows:
            cell = row.find_all('td')
            ### cell in row one/two should link to full IPR table.
            domain_id = cell[1].get_text()
            for index, cell in enumerate(cell):
                if os.path.isfile(raw_table_src_dir + '/col_' + str(index+1) + '_' + domain_id + '.html'):
                    link = BeautifulSoup('<a href="' + final_table_src_dir + "col_" + str(index+1) + "_" + domain_id +'.html">' + cell.get_text() + "</a>", 'lxml').a
                    cell.string = ""
                    cell.append(link)
    ## update new css and scripts
    with open(template_with_script, 'r') as css_src:
        ## works because the script and the div are not imported to the index
        full_table = BeautifulSoup(css_src.read(), 'lxml')
        full_table.body.insert_after(soup.table)
        for script in soup.find_all('script'):
            full_table.body.append(script)
    with open(index_file,'w+', encoding="utf-8") as new_index:
        new_index.write(str(full_table))
    ###### add the new scripts
    # with open('landing_page_template.html', 'r', encoding ="utf-8") as src:
        # style = (BeautifulSoup(src.read(), 'lxml').style)
        # with open(index_file,'r+', encoding="utf-8") as new_index:
            # new_ind = BeautifulSoup(new_index.read(), 'lxml')
            ## insert the style.
            # new_ind.head.append(style)
            # for index, header in enumerate(new_ind.table.find_all('th')):
                # if (header.text() == BeautifulSoup(src.read(), 'lxml').table.th[index].get_text()): 
                    #header.replacewith(BeautifulSoup(src.read(), 'lxml').table.th[index].div
                    # print('hello')
####Given the full IPR table, it links the pdb to the full table, and it also links the full table and index back to the sub tables.
def initIPR(table_id, template_with_script):
   from bs4 import BeautifulSoup
   print("Table ID: " + table_id)
   column_number = 4
   ## for the different columns that even exist
   while (column_number <= 10):
        fname = raw_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '.html'   
        if os.path.isfile(fname):
            print('operating on ' + fname)
            ## then open the script and the table, merging together
            with open(fname, 'r', encoding = "utf-8") as src_file, open(template_with_script, 'r') as style_src:
                table_file = BeautifulSoup(src_file.read(), 'lxml')
                
                ### load the template style and initial headers
                full_file = BeautifulSoup(style_src.read(), 'lxml')
                
                full_table_link = BeautifulSoup('<h2 align="left" style="margin-top: 50px; display: block;"' + '>' + dictionary(table_id, 'index.csv') + "</h2>").h2
                full_file.body.a.insert_after(full_table_link)
                
                if (column_number == 8):
                    ## add the pdb
                    full_file.body.a.insert_after(BeautifulSoup('<div id="con"></div>').div)
                    ## insert the table links into soup
                    rows = table_file.find_all('tr')
                    for row in rows:
                        cell = row.findChildren('td')
                        pdb_link = BeautifulSoup('<a onclick="getStr(' + "'" + cell[7].get_text() + "','" + cell[5].get_text() + "'" + ')" href="javascript:void(0);">' + cell[7].get_text() + '</a>').a
                        cell[7].string = ""
                        cell[7].append(pdb_link)
                    table = BeautifulSoup('<div id="table" style=" height: 50%; width: 100%; clear: both; overflow: auto; max-height: 550px; margin-top: 23%;">' + str(table_file.table) + '</div>').div
                    full_file.body.append(table)    
                    for script in table_file.find_all('script'):
                        full_file.body.append(script)
                    with open(final_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '.html','w+', encoding="utf-8") as new_file:
                        new_file.write(str(full_file))
                elif (column_number == 5 or column_number == 6):
                        ## need to open the columns first
                        table_rows = table_file.find_all('tr')
                        ## for each entry in column5/6
                        for line in table_rows:
                            cell = line.findChildren('td')                              
                            ## link to subtable
                            sub_file_name = raw_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '_' + cell[2].get_text() + '.html'   
                            if (os.path.isfile(sub_file_name)):
                                subtable_link = BeautifulSoup('<a href = "' + sub_file_name.replace(raw_table_src_dir, '') + '">'+cell[1].get_text() +' </a>').a
                                cell[1].string = ""
                                cell[1].append(subtable_link)                            
                                ## then open the col5/6 subtable and make insert formatting
                                with open(sub_file_name,'r') as subtable:
                                    ##make a copy of the template style and insert the new table in
                                    with open(template_with_script,'r') as f:
                                        sub_full_table = BeautifulSoup(f.read(), 'lxml') 
                                    new_table = BeautifulSoup(subtable.read()).table
                                    sub_full_table.body.insert_after(new_table)
                                    for script in sub_full_table.find_all('script'):
                                        sub_full_table.body.append(script)
                                    ## link IPR back to column 
                                    sub_full_table.body.a.insert_after(BeautifulSoup('<a style = "float: left; display: block;" href="col_'+ str(column_number) + '_'+ table_id + '.html">' + dictionary(table_id, 'index.csv') + '</a>').a)
                                     ##   insert a subtitle
                                    sub_full_table.body.a.insert_after(BeautifulSoup('<h3 align="left" style="margin-top: 50px; display: block; color: black;"' + '>' + cell[1].get_text() + '</h3>').h3)                                 

                                with open(sub_file_name.replace(raw_table_src_dir, final_table_src_dir),'w+') as final_file:
                                    final_file.write(str(sub_full_table))
                                    clean_page(sub_file_name.replace(raw_table_src_dir, final_table_src_dir))
                        with open(final_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '.html','w+', encoding="utf-8") as f:
                            full_file.body.insert_after(table_file.table)
                            for script in table_file.find_all('script'):
                                full_file.body.append(script)
                            f.write(str(full_file))
                            clean_page(final_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '.html')
                else:
                    ## insert the table at a diff position            
                    table = table_file.table
                    full_file.body.insert(7, table)                   
                    ## append moledit, sortable, and chemview scripts to bottom of body
                    for script in table_file.find_all('script'):
                        full_file.body.append(script)
                    with open(final_table_src_dir + 'col_' + str(column_number) + '_' + table_id + '.html','w+', encoding="utf-8") as new_file:
                        new_file.write(str(full_file))                
        column_number += 1
def clean_page(web_page):
    from bs4 import BeautifulSoup
    ### open up the index, and find all of the items to link
    if (os.path.isfile(web_page)):
        with open(web_page, 'r') as file:
            soup = BeautifulSoup(file.read())
            header = iter(soup.find_all('th'))
        ### in each row, list the full table, pch, pcipdb, pdb_lig, protein, lig_count, etc.
            for index, name in enumerate(header):
                name.string = name.get_text().replace("_", " ")
                if index == 4:
                    name.string = name.get_text()+ (' (%) ')
                if index == 5:
                    name.string = name.get_text()+( ' (nM) ')
            with open(web_page,'w+', encoding="utf-8") as file:
               file.write(str(soup))
               file.close()
    else:
        print('File ' + web_page + " not found.")

initIndex('index.html', 'basicTemplate.html')
clean_page('index.html')

with open('index.csv', newline='', encoding = "utf-8") as f:
    reader = csv.reader(f)
    # get the column names
    iterRows = iter(reader)
    number = 0
    for row in iterRows:
        ip_code = row[1]
        clean_page(raw_table_src_dir + ip_code + '.html')
        initIPR(ip_code,'basicTemplate.html')
        number = number + 1
        print('row : '+ str(number))





