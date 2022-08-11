This folder contains the test of module 2 in Huang 2014.

#####Intention#####
The original module 2 decides what kind of institution pair in set C can be selected into
set D. However, the original version of module has been performing poorly where many institutions
with apparent differences were classified together.

We guess that this can be strongly related to the 'SubOrganization' segment for many different institutions
can own exactly the same 'SubOrganization' such as 'Dept Chem/Math'. This phenomenon is extremely common
in universities which are the main targets for IND. Not to mention the confusing judgemeng criteria without any 
theoretical explanation or experiments about the use of geographic segments 'State/City/PostalCode'.

As a result, in the first version of module 2 modification, we've simply ignored the 'SubOrganization' segment and 
use only the geographic information (i.e., State, City, PostalCode).

#####Method#####
1. Ignore the 'SubOganization' segment and use only the geographic information (i.e., State, City, PostalCode'). Whenever a institution pair in set C of a author block 
has a or more shared geographic segments, they would be classified into the set D of the author block.

2. Since many institutions with similar names can located in the same state, I've tried to combine the three geographic segments, 
with each same segment contributing 0.5 score. The final score can be 0.0/0.5/1.0/1.5 depending on have many same segments the 
institution pair has, yet the result is far from ideal. Due to the high absence rate of the three segments in the WoS database, many 
institution pairs have been missed causing a extremely low recall rate.

3. How about incorporating the 'SubOrganization' segment in the 'Score System' and make the same 'SubOrg' contribute 0.5 
score as well!

4. 
4.1 We must notice that the 'Secondary information segments' including (SubOrganiztaion, State, City, PostalCode) represent
information with different accuracy. For example, two institutions in set C with the same valid PostalCodes are much more likely 
to be the same institution compared to those with any same the other three segments. We can come to the conclusion that the 
reliability of the segments: PostalCode > City > State > SubOrg. As a result, we should compare the segment with higher reliability first
if they have!!! To achieve this target, we can adjust the comparing order of the segments and the score contribution of each segment!!!
(1) If institution pair has valid PostalCode segments, put it in set D if the PostalCodes are exactly the same. Otherwise, compare 
the rest of the segments. (Detailed progress in iPad GoodNotes!!!)

#####Result#####
1. With the improved module 2, we can ensure that the institution pair are geographically related
(from the same state as least). The ridiculous errors in the original version have almost vanished. The whole 
result seems to be much more acceptable than before.

2. The improvement of module 2 (screening of set D) has obviously reduced the proportion of
misclassification, so the errors brought by rule 2 can be effectively averted. So there is now less 
reason to exclude rule 2.

3. The 3rd method gives consideration to both recall and precision, much more institutions are brought
into the ISS groups compared with method 2. However, some obviouly different institutions have been 
misclassified into the same ISS.



