The words with high proportion and capital initial can cause misjudgement to the jaro-winkler distance which has a higher weight at the 
front of the string. 

So the words with the following characteristics are chosen as the stop words:
1. The noun word which is so general that it has a relatively higher proportion compared with other words. Besides you can't use this word to tell the difference between them.
(e.g., university,Institute,univ,Universidade,Universidad, Universite, Universiti,Universitat,Universiteit,Universitario,Universitaire)
(without limitation of range such as country, area, region, discipline, )
2. Widely used symbols (e.g., &, -,())
3. Preposition with no specific helpful information for disambiguation (e.g., of, de, for, la)

Other findings:
1. The smaller a institution is, the more possible it uses uncommon words in its name.

After_Report:
1.Since the Jaro-Winkler similarity mainly focuses on the front part of the string, the use of stop words has destroyed the word order information in the original institution name to some extent.
For example, 
'University of California Irvine' & 'California State University Long Beach'  >>> 'CaliforniaIrvine' & 'CaliforniaStateLongBeach', the same beginning word 'California' can strongly mislead the J-W similarity.
The orginal version has a result of J-W similarity of 0.6157, while the version without STOP-WORDS is 1.0.
However, without the utilization of stop-words, instutitions with alike beginnings could be classified into the same group (i.e., the group representing different names of the same institution). 
For example, 
'University of California Berkeley' & 'University of Minnesota Duluth' >>> 'CaliforniaBerkeley' & 'MinnesotaDuluth', with J-W similarity of 1.0 for the original version and 0.4389 for the version without STOP-WORDS.
!!!So it's apparent that there is a contradiction for STOP-WORD utilization, which means J-W similarity isn't a proper method. How about combined similarity measures???