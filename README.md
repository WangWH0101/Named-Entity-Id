# Named Entity Identification
     Accurately identify the institution names, solving STM (Single to multiple) problems

# Problem Description
Many institutions have more than one names in public data. For example, *University of California Berkeley* has several names including 
*UC Berkeley*, *UCB* and *Univ of Calif Berkeley* etc. It's now very common that institution ranking based on their research output (e.g., publications) has been an important judgement standard (e.g., QS World University Rankings). As a result, named entity identification has become an essential step before any further related work.

# Method implemented in the study
Due to the chaos and volume of the original data, a ruled-based disambiguation method was raised to carry out named entity identification through the following methods.
- Find candidates with similar author names.
- Remove frequency based stops words (e.g., university, ltd., etc.) and punctuation in institution names.
- Measure the similarity of name pairs (e.g., Levenshtein-Jaro Winkler Distance).
- Combine multidimensional information to judge the similarity.
- Frequency based screening to find potential institution name pair.
- Combine all potential name in one set.
> Specific code is in the folder of the 
