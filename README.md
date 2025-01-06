# **Gibsembler**
<p style = 'text-indent: 40 px;'><div style = 'text-align: center;'><i>This is a program for division of a DNA plasmid into sequences that are optimized for Gibson Assembly.</i></div></p>

**Purpose:** for some biological applications there is a need to divide some theoretical or existing DNA plasmid into multiple shorter sequences that are also optimized for downstream work. In this case, the program is intended to divide a given plasmid into sequences that are optimized for further Gibson assembly application.

### **Gibson Assembly method**

**Biological background:** Often, in laboratories that are working with DNA fragments and their sequences there is a need to combine those descrete DNA sequences into one bigger construct. For example, if we want to observe some visually undetectable protein of interest expressed by a cell culture, than we can fuse this protein to another protein that is detectable, like GFP. For this, a DNA sequence encoding GFP is placed into the genime in a specific place. So, there is a need in methods making it simple to link DNA sequences, and one of the methods that available today called Gibson Assembly.

**The method:** the Gibson mix contains 3 type of enzymes and appropriate buffers: DNA polymerase, exonuclease and DNA ligase. The DNA fragments that are introduced to the soultion contain an overlap between each adjusent fragments. In that way, the exonuclease will digest the nucleotides within this overlaps, therefore inducing anealing beetween homologues overlap sequences. Then, after the overlaps anealed, DNA polymerase would complete the sequences downstream to the overlaps. Finally, DNA ligase ligates the nick between the overlaps and the elongated sequence.

 By this method in is possible to link up to 15 different seqences together in a one-step reaction in one tube (best case scenario). However, preparations and optimisations are needed to perform efficient Gibson Assembly.

 **Some of those optimisations:**
 - The length of the overlap region should be 20-25 bp.
 - Appropriate percentage of GC content within the overlap sequence
 - Usually high complexity within the all of the seqeunces (or high nucleotide diversity, low number of repeating sequences)
 - Good combination of the number of fragments joined in a single reaction and their lengths.

 ### **The Program**
- The Gibsembler accepts .ape files, which are files for the plasmid editor "A Plasmid Editor" or simply ApE.
- The file should contain the sequence of the plasmid that the user wants to divide into fragments that are suitable for Gibson Assembly.
- The user may use the default profile for the division or define manually what are the settings (ike average sequence length, overlap length and more)
- Then, the main part of the code would seek and compare for a division of the plasmid, with respect to the settings.
- The program would display in some way the division for the user, offer to the user to change the settings to create another division.
- Finally, the sequences would be saved, so the user can continue to work with them.
- Maybe, the program would also automatically form an order to some website offering primer and DNA sequence orders.