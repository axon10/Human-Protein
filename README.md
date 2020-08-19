# Human-Protein :pill:
Web database organizing atomic structures of human proteins in order to predict the susceptibility of human genes to therapeutic drugs, with built in 3D viewer!

![Sample web page](https://user-images.githubusercontent.com/25091114/61990894-e63c6e80-b016-11e9-8829-4f76152bb2cb.PNG)
# ICMEssential
A compiled folder of data on the human genome. PDB codes, protein domains, ligand structures, all the raw data you need is here, and can be viewed using MolSoft ICM. This will be updated constantly. It also contains an IP Distribution web page, which contains master links to all the different data, but in a more viewable web database than what Github has to offer. 

# ```tables```
Subtables of the raw data (created for better organization and visibility) should be generated here. Each IPR code has its own set of subtables which can be viewed when searching the IPR code from the IP Distribution home page.

# How to run
```python main.py```- Python program which combines BeautifulSoup and HTML/CSS to link and organize the tables relative to each other. Also manipulates the raw tables by adding an ICMJS extension used to view the 3D pocket of the protein-ligand binding interaction.

# ICM Script
Script written in the ICM language. Generates the raw subtables given ICMEssential raw data, (```/tables``` must be specified as the working directory before starting the script) and also generated the 3D pocket for each entry.

