# FindJobs
 Парсер сайта https://www.monster.com/ для сбора описания указанных вакансий


 A script for searching job descriptions on https://www.monster.com/


* usage: python findjobs.py [-h] [-v] [-s]

                             -p ["inputfilename"] ["outputfilename"]
                 
                             -p ["url"] ["outputfilename"]
   on Linux use python3

   
* positional arguments:

  -p                      parse the urls in "inputfilename" and save data to "outputfilename"
  
                          by default -p means: -p "urls.txt" "jobs.txt"
                          
                          -p "url" parse the url and save data to "outputfilename"
                          
* optional arguments:

  -h, --help &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Show this help message and exit
  
  -v, --version &nbsp; &nbsp; &nbsp; &nbsp; Show program version info and exit
  
  -s &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp;  &nbsp; Show parsing result, if URLs quantity is more than 100- argument is ignored

