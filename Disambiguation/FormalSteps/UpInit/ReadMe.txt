The method used by Huang(2014) has shown a big defect that is the lack of interpretability of candidate screening. 
They chose to find the candidates in author blocks where addresses with the same abbreviated surnames (Keith Swift->Keith S) in a same author block.

Although this approach can utilize the extra information (i.e., author name) and effectively decrease the number of candidates which can substantially raise the time cost of calculation (O(n)=(n-1)!), 
the coverage is still very doubtful.

After many attempts, a law has emerged that most names of a same institution (STM) have the same Capital Letter Combination (CLC).
For example, "University of California Irvine" can have several different spellings, including:
'Univ Calif Irvine'\\'UCI'\\'UC Irvine'\\...
All major spellings have the same CLC which is 'UCI'!

As a result of which, I decide to group the candidates accoding to their CLC (e.g., first three/two/... capital initials).

Based on this idea, the new candidates searching method and improved screening method of Huang(2014) are combined to carry out IND.

Besides address information of a wider time period can be taken advantage of for this method asks for no connection between author and address.
