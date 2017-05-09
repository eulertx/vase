import sys
sys.path.insert(0, '')
from vape.parse_vcf.parse_vcf import * 


class dbSnpFilter(object):
    ''' 
        An object that filters VCF records based on variant data in a 
        dbSNP VCF file.
    '''
    
    def __init__(self, dbsnp_vcf, freq=None, min_freq=None, build=None, 
                 min_build=None, clinvar_path=False):
        ''' 
            Initialize object with a dbSNP VCF file and optional filtering 
            arguments.
        '''

        self.vcf = VcfReader(dbsnp_vcf)
        self.freq_fields = {}
        self.build_fields = {}
        self.clinvar_fields = {}
        self.get_dbsnp_annot_fields()
        self.freq = freq
        self.min_freq = min_freq
        self.build = build
        self.min_build = min_build
        self.clinvar_path = clinvar_path
        if self.freq is not None and self.min_freq is not None:
            if self.freq > self.min_freq:
                raise Exception("freq argument can not be greater than " +
                                "min_freq argument")
            if self.build > self.min_build:
                raise Exception("build argument can not be greater than " +
                                "min_build argument")

    def annotate_and_filter_record(self, record):
        start = record.POS
        end = record.SPAN
        self.vcf.set_region(record.CHROM, start - 1, end)
        filter_alleles = []
        keep_alleles = []
        annotations = []
        hits = list(s for s in self.vcf.parser)
        all_annots = set() #all fields added - may not be present for every ALT
        for i in range(len(record.DECOMPOSED_ALLELES)):
            filt,keep,annot = self._compare_snp_values(
                                            record.DECOMPOSED_ALLELES[i], hits)
            filter_alleles.append(filt)
            keep_alleles.append(keep)
            annotations.append(annot)
            all_annots.update(annot.keys())
        info_to_add = {}
        for f in all_annots:
            info_to_add[f] = []
            for i in range(len(record.DECOMPOSED_ALLELES)):
                if f in annotations[i]:
                    info_to_add[f].append(annotations[i][f])
                else:
                    info_to_add[f].append('.')
        if info_to_add:
            record.addInfoFields(info_to_add)
        return filter_alleles,keep_alleles

    def _compare_snp_values(self, alt_allele, snp_list):
        do_filter = False #only flag indicating should be filtered
        do_keep = False #flag to indicate that should be kept, for overriding 
                        #do_filter in downstream applications 
        annot = {}
        matched = False
        for snp in snp_list:
            for i in range(len(snp.DECOMPOSED_ALLELES)):
                if alt_allele == snp.DECOMPOSED_ALLELES[i]:
                    #no point attempting to use snp.parsed_info_fields() for 
                    #these fields as they are not set to appropriate types
                    matched = True
                    for f in self.freq_fields:
                        if f not in snp.INFO_FIELDS: continue
                        if f == 'CAF':
                            val = snp.INFO_FIELDS[f].split(',')[i+1]
                            annot[f] = val
                            if self.freq is not None:
                                try:
                                    if int(val) >= self.freq:
                                        do_filter = True
                                except ValueError: 
                                    pass 
                            if self.min_freq is not None:
                                try:
                                    if int(val) < self.min_freq:
                                        do_filter = True
                                except ValueError: 
                                    pass
                        elif (f == 'COMMON' and 
                              len(snp.DECOMPOSED_ALLELES) == 1):
                            #COMMON=1 indicates > 1% in 1000 genomes but does 
                            #not indicate which allele(s) if multiple ALTs
                            annot[f] = snp.INFO_FIELDS[f]
                            if self.freq is not None and self.freq <= 0.01:
                                if snp.INFO_FIELDS[f] == '1': 
                                    do_filter = True
                            if (self.min_freq is not None 
                                and self.min_freq <= 0.01
                            ):
                                if snp.INFO_FIELDS[f] == '0': 
                                    do_filter = True
                        elif (f == 'G5A' or f == 'G5' and
                              len(snp.DECOMPOSED_ALLELES) == 1):
                            #FLAGS: >=5% in 1kg or >=5% in pop from 1kg
                            annot[f] = 1
                            if self.freq is not None and self.freq <= 0.05:
                                if snp.INFO_FIELDS[f]: do_filter = True
                            if (self.min_freq is not None 
                             and self.min_freq <= 0.05):
                                if snp.INFO_FIELDS[f]: do_filter = False
                                
                    if 'CLNALLE' in snp.INFO_FIELDS:
                        #the clinvar annotations are done in a non-standard 
                        #way, giving indexes of relevant alleles in CLNALLE 
                        #and keeping other annotations in the same order
                        if (i + 1) in clinvars['CLNALLE']:
                            j = clinvars['CLNALLE'].index(i+1)
                            for f in self.clinvar_fields:
                                if f == 'CLNALLE': continue
                                annot[f] = clinvars[f].split(",")[j] 
                                if self.clinvar_path and f == 'CLNSIG':
                                    if ([i for i in ['4', '5'] if i 
                                                           in sig.split('|')]):
                                        #keep anything with path or likely labl
                                        do_filter = False
                                        do_keep = True
                if matched: break
            if matched: break #bail out on first matching SNP

        return (do_filter, do_keep, annot)
                        


    def get_dbsnp_annot_fields(self):
        '''
            Returns a dict of INFO field names to dicts of 'Type', 'Number'
            and 'Description' as found in the VCF metadata for known dbSNP 
            INFO field names.
        '''

        freq_fields = ["CAF", "G5A", "G5", "COMMON"]
        clinvar_fields = ["CLNSIG", "CLNALLE", "CLNDBN", "CLNDSDBID",
                          "CLNHGVS", "GENEINFO"] 
        build = ["dbSNPBuildID"]
        for f in freq_fields:
            if f in self.vcf.metadata['INFO']:
                self.freq_fields[f] = self.vcf.metadata['INFO'][f][-1]
        for f in clinvar_fields:
            if f in self.vcf.metadata['INFO']:
                self.clinvar_fields[f] = self.vcf.metadata['INFO'][f][-1]
        for f in build:
            if f in self.vcf.metadata['INFO']:
                self.build_fields[f] = self.vcf.metadata['INFO'][f][-1]


