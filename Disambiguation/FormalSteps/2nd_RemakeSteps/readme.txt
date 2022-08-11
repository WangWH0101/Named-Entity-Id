###
This folder contains the 2nd remade disambiguation steps of Institution Name Disambiguation (IND).
The whole structure of the process is based on the idea of Huang 2014.
The address segments:
Linyi Normal Univ(segment 1), Dept Math (segment 2), Linyi 276005(segment 3), Shandong (segment 4),
People's R China (segment 5)

###
Problem of the original version:
1. The original process compares institution pairs' country addresses after the first round screening of set C.
In practice, it's much more effective to compare the country information at first and directly abondon those 
pairs from different countries.

2. The original rule 2 in module 1 which creates set C for each author block would put institution pairs with 
different name lengths and >=2 shared words  into set C. However, the judgment standard is too loose that many 
institution can reach it. For example, many universities include 'university' and 'of' in their names while combination of
place name and 'university' is quite usual as well. In many tests, the original rule has shown a poorer performance in
precision compared with the '>2' version.

3. The module 2 (i.e., rule 6) of original process has a confusing judgement criterion for address segments utilization. The 
comparison of valid segment number has no theoritical or experimental support. Besides, the paper has chosen the second
segment (Suborganiztion) as one of the decisive criteria for set D selection while many institutions especially universities 
can usually have the same Suborganization such as 'Dept Chem/Math', etc. Moreover, it seems that the paper has considered 
the 'middle segments' (i.e., State, City, PostalCode) of equal importance, while they're definitely not! It's easy to understand that
the 'middle segments' have different levels of geographic accuracy where PostalCode>City>State>Suborganiztaion, so it would 
be a better choice if we give them different weights in the judgement process as we've already done in the modified module 2 (i.e., rule6).

4. The original research have rarely mentioned about the data processing which is as important as the following disambiguation
 procedure. Since the original WoS database hasn't had a rigorous format requirements of authors' institution address, there are 
many missing information and default value in the original data. For example, a certain institution address field(字段) may miss 
any one or more segments like 'Country', 'PostalCode' or even its name.

5. As for the last rule 4 which utilizes the modified version of Jaro-Winkler algorithm has shown a serious problem that it puts too much 
weight on the front of a string making strings with similar/same beginnings easily to be misclassified. For example, many universities have 
the beginnings of 'University of', place name, etc. This common phenomenon has created frequent misclassification by rule 4.

###
The modification of the IND process:
1. About the processing of the original WoS data, the data has already been processed of which the address segments have been 
divided into: 
Institution Name(segment 1), Suborganization(segment 2), State/Province(segment 3), City(segment 4), PostalCode(segment 5),
Country(segment 6).
   Since institutions must have a name for any further work, we've discarded address fields without segment 1. Besides, country is
the most basic and important information in the comparison and an independent judgement criterion in the original research paper,
address fields without segment 6 have been discarded as well. Other missing segments with default value have all been replaced 
with an empty string ''. In addition, we've also found that PostalCode(segment 5) can exist meanwhile invalid. For instance, there 
are address fields with PostalCode like '00000', '000 000' while they are actually different institutions. As a result, ' '(space) and '0' 
are thought as the invalid characters for PostalCode and only when a PostalCode have a character other than ' ' and '0', would the
corresponding institution field be considered as valid. What's more, the orginal institution names may contain some symbols (e.g., '&', '-')
that can interference judgment so we've removed all symbols in institution names before any further processes.

2. In the formal version of IND, the '>=2' criterion has been changed to '>2' with a reletively good balance between precision and
recall.

3. In the screening process, we compare an author block's institution pairs' country information first before any further procedure, 
so that the number of institution pairs for comprison can be reduced to increase the efficiency.

4. In consideration of the middle segments' different geographical accuracy levels, PostalCode has been given the highest priority in
module 2 (rule 6). Besides, it's not wise to abondon any segment with the very limited information, so other middle segments (i.e., Suborganization, State, City)
are taken into account too with a score system. 
   Specifically, when any of the two address fields have invalid PostalCode, we let the other three segments (i.e., Suborganization, State, City)
each contributes +0.5 score when they are identical between the two fields. However, when the PostalCode
segments of the pair are comparable (i.e., both valid), the same PostalCode would contribute +1.0 score while -0.5 score can be added if 
they're different. Finally, we will decide whether a pair in set C of a author block is qualified for the corresponding set D according to its 
score. If the score is >=1.0, the pair will appear in the set D.

5. The adjustment of threshold for 'frequency based institution name mapping' which is the final step in the whole process, has shown a 
disappointing ability to raise the precision while higher threshold (e.g., 3,4,...) can obviously decrease the number of ISS groups leading to 
lower recall rate. Besides, the comparison between threshold 2 and 3 has shown that higher threshold lacks advantage in precison while it 
has obvious defects in recall rate (i.e., number of ISS groups). As a result, we decide to utilize 2 as the threshold.

6. The aim of rule 4 is to compare the similarity between two institution names, while the original method with Jaro-Winkler failed to achieve 
this target. The example in the original research paper (i.e., 'Islam Azad Univ' & 'Islamic Azad Univ') isn't proper for this pair of name can also 
be recognized by rule 3. In the final analysis, this rule aims to measure how much the names are alike in the different parts so that the exactly 
same part should be removed before comparison of the different parts. 
   In short, we should measure how similar the different parts are instead of the exactly same parts which could interfere with our judgment. 
As a result, in the modified version of disambiguation, we've used Jaro-Winkler algorithm to compare institution names after removing of 
typical stop-words and the same words. The reason for removing typical stop-words is that some words have different spellings but the same
meaning which is helpless for identification. For example, 'Univ' and 'University' have the same meaning with different spelling, while it contains 
no other detail information of the corresponding institution. Besides, some common prepositions like 'of', 'and', etc. are removed as well.












 







