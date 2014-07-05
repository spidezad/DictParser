DictParser
==========

Parsing Dict object from a text file

The following script is able to parse the strings from a text file as separate dict obj with base type. This allows user to create the dict object easily in a text file. As for now, the values the dict can take basic type such as int, float and string.

Creating the text file format is simple. Starting a dict on a new line with $ <dict name>  followed by the key value pairs in each subsequent line. The format for the pair is <key>:<value1,value2…>

Example of a file format used is as below:

## Text file
$first
aa:bbb,cccc,1,2,3
1:1,bbb,cccc,1,2,3

$second
ee:bbb,cccc,1,2,3
2:1,bbb,cccc,1,2,3
## end of file

See http://simplypython.wordpress.com/2014/06/05/parsing-dict-object-from-text-file/ for more details.
