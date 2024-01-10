from methamplicons.extract_data import ExtractData
import pandas as pd
from collections import defaultdict
import operator

class ExtractMeth(ExtractData):
    """
    This class inherits from ExtractData 
    """

    def __init__(self):
        super().__init__()
        self.threshold = 0.01

    def get_cpg_positions(self, refseq, fwd_pos, rvs_pos):
        pos=list()
        refseq_len = len(refseq)
        for i,nuc in enumerate(refseq):
            if nuc == 'C' and i < refseq_len - 1:
                if refseq[i+1] == 'G':
                    if i>fwd_pos and i<rvs_pos: #exclude primers
                        pos.append(i)
        #print(f"CpG positions from the function are: {pos}")
        return(pos)
    
    #combine with above function to reduce redundancy
    def get_non_cpg_positions(self, refseq, fwd_pos, rvs_pos):
        pos=list()
        refseq_len = len(refseq)
        for i,nuc in enumerate(refseq):
            if nuc == 'C' and i < refseq_len - 1:
                if not(refseq[i+1] == 'G'):
                    if i>fwd_pos and i<rvs_pos: #exclude primers
                        pos.append(i)
        #print(f"CpG positions from the function are: {pos}")
        return(pos)

    def set_threshold(self, threshold): 
        self.threshold = threshold
    
    #replaces the function get_all_reads
    def get_all_reads(self, file, fwd_primer, rev_primer, printout = True): 
        """
        From the output directory, go into merged and read all files that end with extended.fastq
        Also use the appended "region"/gene name to then get the refseq for that gene
        """
        epiallele_counts_region = {}

        # get the string between _ and .extendedFrags.fastq for the amplicon name
        region = file[:-len(".extendedFrags.fastq")]
        region = region.split("_")[-1]
            #create a dictionary for the epiallele counts for the region
            
        # read in the merged reads for the region - for a given sample, from its fastq file
        merged_reads = self.read_fastq(file)

        for read in merged_reads.keys():
            read_seq = merged_reads[read][0]
            try:
                start_pos = read_seq.find(fwd_primer[0:10])
                # search for the last 10 characters of the reverse primer
                end_pos = read_seq.find(rev_primer[-10:]) + 10
                extracted_sequence = read_seq[start_pos:end_pos]
                if start_pos == -1 | end_pos == -1: 
                    continue
            
            #should avoid use of continue
            except: 
                continue

            #print(read_seq)
            if extracted_sequence in epiallele_counts_region.keys(): 
                #should you be using a default dict here
                epiallele_counts_region[extracted_sequence] += 1
            else: 
                epiallele_counts_region[extracted_sequence] = 1

        before_thresh = len(epiallele_counts_region)

        # now need to add logic to remove reads lower than threshold flag

        #get the total counts, sum all values in dict - will be for specific epiallele
        total_seq_count = sum(epiallele_counts_region.values())
        thresh_count = self.threshold * total_seq_count

        if printout:
            print(f"self.threshold is {self.threshold} \n threshold read count is {thresh_count}")

        delete_seqs = [] # as we cannot delete while iterating

        below_thresh_total = 0 
        for extracted_seq, count in epiallele_counts_region.items():
            if count < thresh_count:
                delete_seqs.append(extracted_seq)
                below_thresh_total += count
        
        #delete all sequences with count lower than threshold
        for seq in delete_seqs:
            del epiallele_counts_region[seq]

        if printout:
            print(f"{len(epiallele_counts_region)} sequences remain of original {before_thresh} and their counts are:")
        
            if len(epiallele_counts_region) < 20:
                print(sorted(epiallele_counts_region.values()))
            else:
                print(print(sorted(epiallele_counts_region.values())[-20:]))
                    
        return epiallele_counts_region, below_thresh_total
    
    def get_efficiency_vals(self, allele_counts, refseq, fwd, rev):

        num_ts_obs = 0
        only_dud_seqs = True

        # rather than look at CpG sites, we want to look at non-CpG Cs
        # from the reference sequence 
        # and see if a T is present in the reads 
        pos=self.get_non_cpg_positions(refseq, fwd, rev)
        # counter for total expected non CpG Cs
        exp_ts = 0
        # the number of non CpG Cs in one seq 
        non_cpg_ts_ref = len(pos)

        useable_reads = 0 
        nonuseable_reads = 0
        
        for seq in allele_counts.keys():
            #should not count "dud" reads
            if (len(seq) == len(refseq)):
                only_dud_seqs = False
                # will include this sequence unless it has a sub of C or T to A or G
                include_seq = True
                non_cpg_cs = ""
                for i,nuc in enumerate(seq):
                    # if i is in non_cpg C positions list
                    # and the nucleotide actually is a C or T
                    if i in pos and nuc in "CT":
                        non_cpg_cs += nuc
                    elif i in pos and nuc in "AGN":
                        include_seq = False
                if include_seq:
                    count = allele_counts[seq]
                    # no need for condition if len(non_cpg_cs) == non_cpg_ts_ref:
                    num_ts_obs += non_cpg_cs.count("T") * count
                    exp_ts += non_cpg_ts_ref * count
                    useable_reads += count
                else:
                    count = allele_counts[seq]
                    nonuseable_reads += count

        if allele_counts == {}:
            exp_ts = "Empty"
        elif only_dud_seqs:
            exp_ts = "Badseqs"

        return num_ts_obs, exp_ts, useable_reads, non_cpg_ts_ref
            

    def count_alleles(self, allele_counts, refseq, fwd, rev): 
        #instantiate new dictionary
        alleles = defaultdict(int)
        
        # count total number of reads
        reads_n = sum(allele_counts.values())
        #print(f"The total number of reads was {reads_n}")
        
        # get CpG positions
        pos=self.get_cpg_positions(refseq, fwd, rev)
        #print(f"The cpg positions given that fwd is {fwd} and rev is {rev} are: {pos}")
        
        # amplicon length for 1st filter
        refseq_len=len(refseq)
        #print(f"refseq:\n{refseq}")
        
        filt_for_length = 0 
        filt_for_CpG_AG = 0 

        for seq,val in allele_counts.items():
            #1st and 2nd filters: exclude all indels, and minimum freq
            #print(f"seq: \n{seq}\nrefseq: \n{refseq}")
            if (len(seq) == refseq_len): #& (val > min_reads): 
                allele=""
                for i,nuc in enumerate(seq):
                    if i in pos:
                        allele+=nuc
                testseq=set(allele)
                #3rd filter, for any errors in the positions of interest
                if 'A' not in testseq and 'G' not in testseq: 
                    # this also works to either initialise a count for an allele 
                    # such as CTCT - this is agnostic to the other bases of the read
                    alleles[allele]+=val
                else: 
                    #print("One of the CpG sites had an A or G")
                    filt_for_CpG_AG += val
            else: 
                #print(f"Length of sequence = {len(seq)}, Length of refseq = {refseq_len}")
                #print(f"Number of reads = {val}, Minimum reads was {min_reads}")
                filt_for_length += val

        # Sort by number of reads supporting the allele
        alleles_sort = sorted(alleles.items(), key=operator.itemgetter(1), reverse=True)

        # Total number of reads after filtering
        filtered_reads=sum(alleles.values())

        return(alleles_sort,filtered_reads, filt_for_length, filt_for_CpG_AG, reads_n)

    def group_alleles_by_meCpG (alleles_sort):
        d_group = defaultdict(int)
        for allele,count in alleles_sort:
            d_group[allele.count("C")] +=count
        return(d_group)

    def convert_to_df (self, alleles_sort, refseq, fwd, rev, filtered_reads,freq_min):
        #alleles_sort,refseq, fwd, rev, filtered_reads,freq_min
        # get CpG positions
        pos=self.get_cpg_positions(refseq, fwd, rev)
        df=pd.DataFrame()
        df_counts=pd.DataFrame()
        for allele, val in alleles_sort:
            freq=(val/filtered_reads*100)
            if freq >= freq_min: #Frequency cut-offs
                nuc_list = list(allele)
                nuc_list.insert(0,allele)
                row=pd.DataFrame(nuc_list).T
                row.columns=("seq",*pos)
                df= df.append(row,ignore_index=True)
                allele_counts = [allele, freq, val]
                row_counts=pd.DataFrame(allele_counts).T
                row_counts.columns=("seq","freq", "val")
                df_counts = df_counts.append(row_counts,ignore_index=True)

        df_melt = df.melt(id_vars = "seq")
        df_melt_merged = pd.merge(df_melt, df_counts, on="seq")
    
        return(df_melt_merged)

    def calculate_meth_fraction(self, alleles_s, refseq, fwd, rev, include_unmeth_alleles=True):

        methylated_counts = defaultdict(int)
        methylated_fraction = defaultdict(int)

        totalreads = 0
        for allele,val in alleles_s:
            if include_unmeth_alleles or any('C' == nuc for nuc in allele):
                totalreads += val
                for i,nuc in enumerate(allele):
                    if nuc == 'C':
                        methylated_counts[i]+=val
                    elif nuc == 'T':
                        # this should fix it so that if several of the positions are always unmethylated, they are still included with a zero count
                        methylated_counts[i]+=0
                    # else - do nothing at the moment - site will be NA if there are no C or T - will be considered invalid
        
        # this considers the case where all positions are 0 but not some positions being 0                  
        if not methylated_counts:
            pos=self.get_cpg_positions(refseq, fwd, rev)
            for i,p in enumerate(pos):
                methylated_counts[i]=0

        for i,methcount in methylated_counts.items():
            if totalreads == 0:
                methylated_fraction[i] = 0
            else:
                methfrac = methcount/totalreads
                methylated_fraction[i] = methfrac

        df = pd.DataFrame.from_dict(methylated_fraction, orient = "index")
        
        return(df)

    def calculate_meth_fraction_min(self, alleles_sort, refseq, fwd, rev, filtered_reads, freq_min):
        methylated_counts = defaultdict(int)
        methylated_fraction = defaultdict(int)
        
        pos=self.get_cpg_positions(refseq, fwd, rev)
        

        val_sum=0
        for allele, val in alleles_sort:
            freq=(val/filtered_reads*100)
            if freq < freq_min: #Frequency cut-offs and second filter, for any errors in the positions of interest
                val_sum+=val
                for i,nuc in enumerate(allele):
                    if nuc == 'C':
                        methylated_counts[pos[i]]+=val
                    else:
                        methylated_counts[pos[i]]+=0
                        
        for i,methcount in methylated_counts.items():
            methfrac = methcount/val_sum
            methylated_fraction[i] = methfrac

        if not methylated_counts:
            for i,p in enumerate(pos):
                methylated_fraction[i]=0
        
        df = pd.DataFrame.from_dict(methylated_fraction, orient = "index")
        df.reset_index(level=0, inplace=True)
        df.columns = ['variable', 'shade']
        df['value'] = 'below_min'
        df['seq'] = 'below_min'
        df['freq'] = (val_sum/filtered_reads*100)
        df['val'] = val_sum
            
        return(df)
    
    def parse_name(self, sname): 
        if "_parse_" in sname: 
            new_name = sname.split("_parse_")[0]
        elif "all_lanes" in sname:
            new_name = sname.split("_all_lanes_")[0]
        else:
            new_name = sname

        return new_name

    
    






    
