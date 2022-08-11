This folder contains the test of rule 2 in Huang 2014.
The original rule 2 classify institution pair with different name lengths and no less than 
2 shared words into the C set. It's apparent that this rule can misclassify many institutions.

As a result, this test will see what kind of institution pair can only be found out by rule2, 
Instead of other rules.

#####Result#####
1. It's not wise to simply abondon rule2, the comparsion shows that there actually exist
some institution names which can only be recognized by rule 2.

2. The improvement of module 2 (screening of set D) has obviously reduced the proportion of
misclassification, so the errors brought by rule 2 can be effectively averted. So there is now less 
reason to exclude rule 2.

3. The choice of '>=2' in rule2 with new module2 has shown a much poorer performance under 
the threshold of 2. Although there are more ISS groups compared with '>2' version, the frequent 
misclassification has made the superficial improvement not worth mentioning.

4. To make up the defect of '>=2' rule2, we've raised the threshold from 2 to 3, while the number of ISS
groups has decreased from 1106 to 656. Though the result is still far from being ideal compared with the 
'>=2' rule2 with new module 2 even under the stricter threshold.

#####Discussion#####
1. How about try some stop-words???


