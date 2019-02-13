# VASE

This is a program for Variant Annotation, Segregation and Exclusion for
family or cohort based rare-disease sequencing studies.

## INTRODUCTION

VASE can be used to filter VCF files based on allele frequency data, functional
consequences from VEP, presence/absence of variants in cases vs controls and 
inheritance patterns within families. It is designed primarily for use in rare
disease cohort or familial studies.

In order to make the most of the functions VASE provides, you will require a 
multi-sample, [VEP](https://github.com/Ensembl/ensembl-vep) annotated VCF. In 
order to confidently identify variants segregating within families consistent 
with dominant/recessive/de novo inheritance patterns, your VCF should have been
made by calling all of your samples simultaneously (e.g. using the [GATK 
joint-calling workflow](https://gatkforums.broadinstitute.org/gatk/discussion/3893/calling-variants-on-cohorts-of-samples-using-the-haplotypecaller-in-gvcf-mode)).

Detailed instructions and examples to follow in the VASE
[wiki](https://github.com/gantzgraf/vase/wiki).

## INSTALLATION

VASE requires python3. It has been tested with python 3.5 and 3.6. The modules 
'pysam' and 'parse_vcf' from pypi are required and should be installed for you 
if following the instructions below. You may also wish to install biopython, 
which is required if you want to write directly to bgzipped output.

To install the vase script to $HOME/.local/bin (or possibly on Mac OS
/Users/david/Library/Python/3.\*/bin/) the simplest way is to use pip:

    pip3 install git+git://github.com/gantzgraf/vase.git --user

To install system-wide remove the --user flag and ensure you have root 
priveleges (e.g. using sudo).

Alternatively, you may first clone this repository:

    git clone https://github.com/gantzgraf/vase.git

Alternatively use the 'Clone or download' button above. From the newly created 
vase directory you may install either by running the setup.py script as 
follows:

    python3 setup.py install --user

or by using pip, if installed:

    pip3 install . --user

If you have root privileges you can install system wide as follows:

    sudo python3 setup.py install

or:

    sudo pip3 install .

## USAGE/OPTIONS

    
    usage: vase -i VCF [-o OUTPUT] [-r REPORT_PREFIX]
                [-burden_counts BURDEN_COUNTS] [-gnomad_burden] [-v QUAL]
                [-p | --keep_filters KEEP_FILTERS [KEEP_FILTERS ...]]
                [--exclude_filters EXCLUDE_FILTERS [EXCLUDE_FILTERS ...]]
                [-t TYPE [TYPE ...]] [-max_alts MAX_ALT_ALLELES] [-af AF]
                [-min_af MIN_AF] [-ac AC] [-min_ac MIN_AC] [-c [CSQ [CSQ ...]]]
                [--canonical] [--flagged_features]
                [--biotypes BIOTYPE [BIOTYPE ...]]
                [--feature_blacklist FEATURE_BLACKLIST]
                [-m MISSENSE_FILTERS [MISSENSE_FILTERS ...]]
                [--filter_unpredicted] [--keep_if_any_damaging] [--no_vep_freq]
                [--vep_af VEP_AF [VEP_AF ...]] [--region REGION [REGION ...] |
                --bed BED | --gene_bed BED] [--cadd_files FILE [FILE ...]]
                [-cadd_dir DIR] [--cadd_phred FLOAT] [--cadd_raw FLOAT]
                [-d VCF [VCF ...]] [-g VCF [VCF ...]]
                [--vcf_filter VCF,ID[,INFO_FIELD ...] [VCF,ID[,INFO_FIELD ...]
                ...]] [--dng_vcf DNG_VCF [DNG_VCF ...]] [-f FREQ]
                [--min_freq MIN_FREQ] [-b dbSNP_build] [--max_build dbSNP_build]
                [--filter_known] [--filter_novel] [--clinvar_path]
                [-ignore_existing] [--cases SAMPLE_ID [SAMPLE_ID ...]]
                [--controls SAMPLE_ID [SAMPLE_ID ...]] [-ped PED] [-gq GQ]
                [-dp DP] [-het_ab AB] [-hom_ab AB] [-con_gq CONTROL_GQ]
                [-con_dp CONTROL_DP] [-con_het_ab AB] [-con_hom_ab AB]
                [-con_ref_ab AB] [--n_cases N_CASES] [--n_controls N_CONTROLS]
                [--biallelic] [--de_novo] [--dominant]
                [--min_families MIN_FAMILIES]
                [--singleton_recessive SAMPLE_ID [SAMPLE_ID ...]]
                [--singleton_dominant SAMPLE_ID [SAMPLE_ID ...]]
                [--seg_controls SAMPLE_ID [SAMPLE_ID ...]] [--prog_interval N]
                [--log_progress] [--quiet] [--debug] [-h]

    Variant annotation, segregation and exclusion.

    Required Arguments:
      -i VCF, --input VCF   Input VCF filename
                            

    Output Arguments:
      -o OUTPUT, --output OUTPUT
                            Filename for VCF output. If this ends in .gz or
                            .bgz the output will be BGZIP compressed.
                            Default = STDOUT
                            
      -r REPORT_PREFIX, --report_prefix REPORT_PREFIX
                            Prefix for segregation summary report output
                            files. If either --biallelic, --de_novo or
                            --dominant options are in effect this option will
                            write summaries for segregating variants to files
                            with the respective suffixes of
                            '_recessive.report.tsv', '_de_novo.report.tsv' and
                            '_dominant.report.tsv'.
                            
      -burden_counts BURDEN_COUNTS, --burden_counts BURDEN_COUNTS
                            File for outputting 'burden counts' per
                            transcript. If specified, the number of alleles
                            passing specified filters will be counted for
                            each transcript identified. Requires your VCF
                            input to be annotated with Ensembl's VEP. Note,
                            that if --cases or --controls are specified when
                            using this argument, variants will not be filtered
                            on presence in cases/controls; instead counts will
                            be written for cases and controls to this file.
                            
      -gnomad_burden, --gnomad_burden
                            If using --burden_counts, use this flag to
                            indicate that the input is from gnomAD and should
                            be parsed per population.
                            

    Annotation File Arguments:
      --cadd_files FILE [FILE ...], -cadd_files FILE [FILE ...]
                            One or more tabix indexed CADD annotation files
                            (such as those found at
                            http://cadd.gs.washington.edu/download). Variants
                            in your input that match any scored variant in
                            these files will have the CADD RawScore and PHRED
                            values added to the INFO field, one per ALT
                            allele. Alleles/variants can be filtered on these
                            scores using the --cadd_phred or --cadd_raw
                            options.
                            
      -cadd_dir DIR, --cadd_directory DIR
                            Directory containing one or more tabix indexed
                            CADD annotation files to be used as above. Only
                            files with '.gz' or '.bgz' extensions will be
                            included.
                            
      --cadd_phred FLOAT, -cadd_phred FLOAT
                            CADD PHRED score cutoff. Variants with a CADD
                            PHRED score below this value will be filtered.
                            Only used with annotations from files supplied to
                            --cadd_files or --cadd_dir arguments or a
                            pre-annotated CADD_PHRED_score INFO field. To
                            filter on CADD scores annotated using the VEP
                            dbNSFP plugin use the --missense_filters option.
                            
      --cadd_raw FLOAT, -cadd_raw FLOAT
                            CADD RawScore cutoff. Variants with a CADD
                            RawScore below this value will be filtered.
                            Only used with annotations from files supplied to
                            --cadd_files or --cadd_dir arguments or a
                            pre-annotated CADD_raw_score INFO field. To filter
                            on CADD scores annotated using the VEP dbNSFP
                            plugin use the --missense_filters option.
                            
      -d VCF [VCF ...], --dbsnp VCF [VCF ...], --clinvar VCF [VCF ...]
                            dbSNP or ClinVar VCF file for variant
                            annotating/filtering
                            
      -g VCF [VCF ...], --gnomad VCF [VCF ...], --exac VCF [VCF ...]
                            gnomAD/ExAC file for variant annotating/filtering
                            using population allele frequencies
                            
      --vcf_filter VCF,ID[,INFO_FIELD ...] [VCF,ID[,INFO_FIELD ...] ...], -vcf_filter VCF,ID[,INFO_FIELD ...] [VCF,ID[,INFO_FIELD ...] ...]
                            VCF file(s) and name(s) to use in INFO fields
                            for frequency annotation and/or filtering. Each
                            file and its associated annotation ID should be
                            given in pairs separated with commas. INFO fields
                            will be added to your output for the AN and AF
                            fields with the field names of VASE_<ID>_AN and
                            VASE_<ID>_AF. If --freq or --min_freq arguments
                            are set then matching variants in your input will
                            be filtered using AF values found in these files.
                            
                            You may also add additonal INFO fields to extract
                            and annotate your matching variants with by
                            including additional comma-separated fields after
                            the ID.
                            
      --dng_vcf DNG_VCF [DNG_VCF ...]
                            One or more VCFs created by DeNovoGear for adding
                            PP_DNM and PP_NULL fields to sample calls.
                            
      -f FREQ, --freq FREQ, --max_freq FREQ
                            Allele frequency cutoff (between 0 and 1). Used
                            for extenal allele frequency sources such as
                            --dbsnp or --gnomad files. Alleles/variants with
                            an allele frequency equal to or greater than
                            this value in these sources will be filtered
                            from your input. VEP annotated allele frequencies
                            will also be used for filtering if '--csq' option
                            is used (VEP v90 or higher required). This can be
                            disabled with the --no_vep_freq option.
                            
      --min_freq MIN_FREQ, -min_freq MIN_FREQ
                            Minimum allele frequency cutoff (between 0 and 1).
                            Used for extenal allele frequency sources such as
                            --dbsnp or --gnomad files. Alleles/variants with
                            a frequency lower than this value will be filtered.
                            VEP annotated allele frequencies will also be used
                            for filtering if '--csq' option is used (VEP v90
                            or higher required). This can be disabled with the
                            --no_vep_freq option.
                            
      -b dbSNP_build, --build dbSNP_build
                            dbSNP build version cutoff. For use with --dbsnp
                            files. Alleles/variants present in this dbSNP
                            build or earlier will be filtered from input.
                            from your input.
                            
      --max_build dbSNP_build, -max_build dbSNP_build
                            Maximum dbSNP build version cutoff. For use with
                            --dbsnp files. Alleles/variants present in dbSNP
                            builds later than this version will be filtered.
                            
      --filter_known, -filter_known
                            Filter any allele/variant present in any of the
                            files supplied to --gnomad, --dbsnp or
                            --vcf_filter arguments, or if using '--csq' if any
                            allele frequency is recorded for any of VEP's AF
                            annotations.
                            
      --filter_novel, -filter_novel
                            Filter any allele/variant NOT present in
                            any of the files supplied to --gnomad or --dbsnp or
                            --vcf_filter arguments, or if using '--csq' if no
                            allele frequency is recorded for any of VEP's AF
                            annotations.
                            
      --clinvar_path, -path
                            Retain variants with ClinVar 'likely pathogenic'
                            or 'pathogenic' flags regardless of frequency or
                            other settings provided to other Annotation File
                            Arguments. This requires one of the files
                            provided to --dbsnp to have CLNSIG annotations
                            from ClinVar.
                            
      -ignore_existing, --ignore_existing_annotations
                            Ignore previously added annotations from
                            dbSNP/gnomAD/CADD files that may be present in the
                            input VCF. Default behaviour is to use these
                            annotations for filtering if present and the
                            relevant arguments (e.g. --freq) are given.
                            

    Variant Filtering Arguments:
      Arguments for filtering based on variant features

      -v QUAL, --variant_quality QUAL
                            Minimum variant quality score ('QUAL' field).
                            Variants with a QUAL score below this value will be
                            filtered/ignored.
                            
      -p, --pass_filters    Only keep variants that have passed filters
                            (i.e. FILTER field must be "PASS")
                            
      --keep_filters KEEP_FILTERS [KEEP_FILTERS ...]
                            Only keep variants that have these FILTER Fields.
                            Can not be used with --pass_filters but you can
                            use 'pass' as one of your arguments here to retain
                            variants that pass filters in addition to variants
                            with a FILTER Field matching the values specified.
                            If multiple filter annotations are given for a
                            variant all must match one of these fields or it
                            will be filtered.
                            
      --exclude_filters EXCLUDE_FILTERS [EXCLUDE_FILTERS ...]
                            Filter variants that have these FILTER Fields.
                            If multiple filter annotations are given for a
                            variant it will be excluded if any match one of
                            the given fields.
                            
      -t TYPE [TYPE ...], --var_types TYPE [TYPE ...]
                            Keep variants of the following type(s). Valid
                            types are 'SNV' (single nucleotide variants),
                            'MNV' (multi-nucleotide variants excluding
                            indels), 'INSERTION' (insertions or duplications
                            relative to the reference), 'DELETION' (deletions
                            relative to the reference), 'INDEL' (shorthand for
                            both insertions and deletions) and 'SV'
                            (structural variants). If a site is multiallelic
                            it will be retained if any ALT allele matches one
                            of these types, but per-allele filtering for
                            segregation filtering will only consider ALT
                            alleles of the appropriate types.
                            
      -max_alts MAX_ALT_ALLELES, --max_alt_alleles MAX_ALT_ALLELES
                            Filter variants at sites with more than this
                            many ALT alleles. For example, using
                            '--max_alt_alleles 1' would retain biallelic sites
                            only.
                            
      -af AF, --af AF       Maximum AF value in input VCF. Any allele with an
                            AF > than this value will be filtered.
                            
      -min_af MIN_AF, --min_af MIN_AF
                            Minimum AF value in input VCF. Any allele with an
                            AF < than this value will be filtered.
                            
      -ac AC, --ac AC       Maximum AC value in input VCF. Any allele with an
                            AC > than this value will be filtered.
                            
      -min_ac MIN_AC, --min_ac MIN_AC
                            Minimum AC value in input VCF. Any allele with an
                            AC < than this value will be filtered.
                            
      -c [CSQ [CSQ ...]], --csq [CSQ [CSQ ...]]
                            One or more VEP consequence classes to retain.
                            Variants which do not result in one of these VEP
                            consequence classes will be filtered. If this
                            option is used with no values then the following
                            default classes will be used:
                            
                                              TFBS_ablation
                                              TFBS_amplification
                                              inframe_deletion
                                              inframe_insertion
                                              frameshift_variant
                                              initiator_codon_variant
                                              missense_variant
                                              protein_altering_variant
                                              regulatory_region_ablation
                                              regulatory_region_amplification
                                              splice_acceptor_variant
                                              splice_donor_variant
                                              start_lost
                                              stop_gained
                                              stop_lost
                                              transcript_ablation
                                              transcript_amplification
                            
                            You may also pass the value "default" in order to
                            include these default classes in addition to other
                            specified classes. Alternatively, you may specify
                            'all' to include all consequence types if, for
                            example, you want to filter on other VEP
                            annotations (e.g. allele frequency or biotype)
                            irrespective of consequence.
                            
                            Note, that using the --csq option automaticaally
                            turns on biotype filtering (see the --biotype
                            option below).
                            
      --canonical, -canonical
                            When used in conjunction with --csq argument,
                            ignore consequences for non-canonical transcripts.
                            
      --flagged_features, -flagged_features
                            When used in conjunction with --csq argument,
                            ignore consequences for flagged
                            transcripts/features (i.e. with a non-empty
                            'FLAGS' CSQ field).
                            
      --biotypes BIOTYPE [BIOTYPE ...], -biotypes BIOTYPE [BIOTYPE ...]
                            When used in conjunction with --csq argument,
                            ignore consequences in biotypes other than those
                            specified here. By default only consequences in
                            features with the following biotypes are
                            considered:
                            
                                        3prime_overlapping_ncrna
                                        antisense
                                        CTCF_binding_site
                                        enhancer
                                        IG_C_gene
                                        IG_D_gene
                                        IG_J_gene
                                        IG_V_gene
                                        lincRNA
                                        miRNA
                                        misc_RNA
                                        Mt_rRNA
                                        Mt_tRNA
                                        open_chromatin_region
                                        polymorphic_pseudogene
                                        processed_transcript
                                        promoter
                                        promoter_flanking_region
                                        protein_coding
                                        rRNA
                                        sense_intronic
                                        sense_overlapping
                                        snoRNA
                                        snRNA
                                        TF_binding_site
                                        translated_processed_pseudogene
                                        TR_C_gene
                                        TR_D_gene
                                        TR_J_gene
                                        TR_V_gene
                            
                            Use this argument to specify one or more biotypes
                            to consider instead of those listed above. You may
                            also include the value 'default' in your list to
                            include the default values listed above in
                            addition to others provided to this argument.
                            Alternatively you may use the value 'all' to
                            disable filtering on biotypes.
                            
      --feature_blacklist FEATURE_BLACKLIST, --blacklist FEATURE_BLACKLIST
                            A file containing a list of Features (e.g. Ensembl
                            transcript IDs) to ignore. These must correspond
                            to the IDs in the 'Feature' field annotated by
                            VEP.
                            
      -m MISSENSE_FILTERS [MISSENSE_FILTERS ...], --missense_filters MISSENSE_FILTERS [MISSENSE_FILTERS ...]
                            A list of in silico prediction programs to use
                            for filtering missense variants (must be used in
                            conjunction with --csq argument). The programs
                            provided her must have been annotated on the
                            input VCF file either directly by VEP or via the
                            dbNSFP VEP plugin. Recognised program names and
                            default 'damaging' values are provided in the
                            "data/vep_insilico_pred.tsv" file.
                            
                            You may optionally specify score criteria for
                            filtering as in the the following examples:
                            
                                FATHMM_pred=D
                                MutationTaster_pred=A
                                MetaSVM_rankscore=0.8
                            
                            Or you may just provide the program names
                            and the default 'damaging' prediction values
                            will be used, as listed in the file
                            "vase/data/vep_insilico_pred.tsv".
                            
                            By default, a missense consequence is filtered
                            unless each of the programs listed here have an
                            appropriate or missing prediction/score. This
                            behaviour can be changed using the
                            --filter_unpredicted or --keep_if_any_damaging
                            flags.
                            
      --filter_unpredicted, -filter_unpredicted
                            For use in conjunction with --missense_filters.
                            The default behaviour when using
                            --missense_filters is to ignore a program if
                            there is no prediction given (i.e. the score/pred
                            is empty). That is, if there are no predictions
                            for any of the programs annotating a missense
                            consequence, it will not be filtered, while if
                            predictions are missing for only some, filtering
                            will proceed as normal with the other programs. If
                            this option is given, missense variants will be
                            filtered if any program does not have a
                            prediction/score.
                            
      --keep_if_any_damaging, -keep_if_any_damaging
                            For use in conjunction with --missense_filters.
                            If this option is provided, a missense consequence
                            is only filtered if ALL of the programs provided
                            to --missense_filters do not have an appropriate
                            prediction/score - that is, the missense
                            consequence will be retained if ANY of the given
                            programs has an appropriate value for the
                            prediction/score. This behaviour is overridden by
                            '--filter_unpredicted' when a prediction/score is
                            missing for any program.
                            
      --no_vep_freq, -no_vep_freq
                            Use this option if you want to ignore VEP
                            annotated allele frequencies when using --freq and
                            --csq options.
                            
      --vep_af VEP_AF [VEP_AF ...], -vep_af VEP_AF [VEP_AF ...]
                            One or more VEP allele frequency annotations to
                            use for frequency filtering. Default is to use the
                            following (assuming --csq and --freq or --min_freq
                            arguments are in effect):
                            
                                            MAX_AF
                                            AFR_AF
                                            AMR_AF
                                            EAS_AF
                                            EUR_AF
                                            SAS_AF
                                            AA_AF
                                            EA_AF
                                            gnomAD_AF
                                            gnomAD_AFR_AF
                                            gnomAD_AMR_AF
                                            gnomAD_ASJ_AF
                                            gnomAD_EAS_AF
                                            gnomAD_FIN_AF
                                            gnomAD_NFE_AF
                                            gnomAD_OTH_AF
                                            gnomAD_SAS_AF
                                            gnomADg_AF_AFR
                                            gnomADg_AF_AMR
                                            gnomADg_AF_ASJ
                                            gnomADg_AF_EAS
                                            gnomADg_AF_FIN
                                            gnomADg_AF_NFE
                                            gnomADg_AF_OTH
                            

    Region Filtering Arguments:
      Arguments for filtering variants on genomic regions. These arguments are mutually exclusive.

      --region REGION [REGION ...]
                            Only include variants overlapping these intervals
                            (in the format chr1:1000-2000).
                            
      --bed BED             Only include variants overlapping the intervals in
                            the provided BED file.
                            
      --gene_bed BED        Only include variants overlapping the intervals in
                            the provided BED file and with a VEP annotation
                            for the provided gene/transcript/protein
                            identifiers. The fourth column of the provided BED
                            file should contain gene symbols and/or Ensembl
                            gene/transcript/protein identifiers (multiple IDs
                            should be separated with '/' characters.
                            Requires input to be annotated with VEP.
                            

    Sample Based Filtering Arguments:
      Arguments for filtering variants based on presence/absence in samples and/or
      inheritance patterns

      --cases SAMPLE_ID [SAMPLE_ID ...], -cases SAMPLE_ID [SAMPLE_ID ...]
                            One or more sample IDs to treat as cases. Default
                            behaviour is to retain variants/alleles present in
                            all of these samples as long as they are not
                            present in any sample specified using the
                            '--controls' option. This behaviour can be
                            adjusted using other options detailed below.
                            
      --controls SAMPLE_ID [SAMPLE_ID ...], -controls SAMPLE_ID [SAMPLE_ID ...]
                            One or more sample IDs to treat as controls.
                            Default behaviour is to filter variants/alleles
                            present in any of these samples. This behaviour
                            can be adjusted using other options detailed
                            below.
                            
      -ped PED, --ped PED   A ped file containing information about samples in
                            your VCF for use for filtering on affectation
                            status and inheritance patterns.
                            
                            A PED file is a white-space (space or tab)
                            delimited file with the first six mandatory
                            columns:
                            
                                 Family ID
                                 Individual ID
                                 Paternal ID
                                 Maternal ID
                                 Sex (1=male; 2=female; other=unknown)
                                 Phenotype
                            
                            Affection status should be coded:
                            
                                -9 missing
                                 0 missing
                                 1 unaffected
                                 2 affected
                            
                            All individuals of interest, including parents,
                            should be specified in this file so that
                            affectation status can be read and dominant versus
                            recessive/de novo inheritance models can be
                            inferred.
                            
      -gq GQ, --gq GQ       Minimum genotype quality score threshold. Sample
                            genotype calls with a score lower than this
                            threshold will be treated as no-calls.
                            Default = 20.
                            
      -dp DP, --dp DP       Minimum genotype depth threshold. Sample genotype
                            calls with a read depth lower than this threshold
                            will be treated as no-calls. Default = 0.
                            
      -het_ab AB, --het_ab AB
                            Minimum genotype allele balance for heterozygous
                            genotypes. Heterozygous sample genotype calls
                            with a ratio of the alternate allele vs total
                            depth lower than this threshold will be treated as
                            no-calls. Default = 0.
                            
      -hom_ab AB, --hom_ab AB
                            Minimum genotype allele balance for homozygous
                            genotypes. Homozygous sample genotype calls
                            with a ratio of the alternate allele vs total
                            depth lower than this threshold will be treated as
                            no-calls. Default = 0.
                            
      -con_gq CONTROL_GQ, --control_gq CONTROL_GQ
                            Minimum genotype quality score threshold for
                            parents/unaffecteds/controls when filtering
                            variants. Defaults to the same value as --gq but
                            you may wish to set this to a lower value if, for
                            example, you require less evidence from
                            controls/unaffected in order to filter a variant
                            or from parental genotype calls when confirming
                            a potential de novo variant.
                            
      -con_dp CONTROL_DP, --control_dp CONTROL_DP
                            Minimum depth threshold for
                            parents/unaffecteds/controls when filtering
                            variants. Defaults to the same value as --dp but
                            you may wish to set this to a lower value if, for
                            example, you require less evidence from
                            controls/unaffected in order to filter a variant
                            or from parental genotype calls when confirming
                            a potential de novo variant.
                            
      -con_het_ab AB, --control_het_ab AB
                            Minimum genotype allele balance for heterozygous
                            genotypes. Heterozygous sample genotype calls
                            with a ratio of the alternate allele vs total
                            depth lower than this threshold will be treated as
                            no-calls. Defaults to the same as --het_ab but
                            you may wish to set this to a lower value if, for
                            example, you require less evidence from
                            controls/unaffected in order to filter a variant.
                            
      -con_hom_ab AB, --control_hom_ab AB
                            Minimum genotype allele balance for homozygous
                            genotypes. Homozygous sample genotype calls
                            with a ratio of the alternate allele vs total
                            depth lower than this threshold will be treated as
                            no-calls. Defaults to the same as --hom_ab but
                            you may wish to set this to a lower value if, for
                            example, you require less evidence from
                            controls/unaffected in order to filter a variant.
                            
      -con_ref_ab AB, --control_max_ref_ab AB
                            Maximum genotype allele balance for
                            parents/unaffecteds/controls with reference (0/0)
                            genotypes when filtering variants. If you wish to
                            count/exclude variants where controls/unaffecteds
                            are called as homozygous reference but still have a
                            low proportion of ALT alleles specify a suitable
                            cutoff here.
                            
      --n_cases N_CASES, -n_cases N_CASES
                            Instead of requiring a variant to be present in
                            ALL samples specified by --cases, require at least
                            this many cases.
                            
      --n_controls N_CONTROLS, -n_controls N_CONTROLS
                            Instead of filtering an allele/variant if present
                            in ANY sample specified by --controls, require at
                            least this many controls to carry a variant before
                            it is filtered.
                            
      --biallelic, -biallelic, --recessive
                            Identify variants matching a recessive inheritance
                            pattern in cases present in the PED file specified
                            by the --ped argument. Input must be VEP
                            annotated. If the --csq argument is given, only
                            variants/alleles resulting in the given functional
                            consequences will be used to identify qualifying
                            variants/alleles, otherwise the default set of
                            VEP consequences (see --csq argument for details)
                            will be used.
                            
      --de_novo, -de_novo   Idenfify apparent de novo variants in cases
                            present in the PED file specified by the --ped
                            argument. This requires that at least one
                            parent-child trio exists in the given PED file.
                            
      --dominant, -dominant
                            Idenfify variants segregating in manner matching
                            dominant inheritance in cases present in the PED
                            file specified by the --ped argument.
                            
      --min_families MIN_FAMILIES, -min_families MIN_FAMILIES
                            Minimum number of families (or unrelated samples)
                            required to contain a qualifying dominant/de novo
                            or biallelic combination of variants in a feature
                            before they are output. Default = 1.
                            
      --singleton_recessive SAMPLE_ID [SAMPLE_ID ...], -singleton_recessive SAMPLE_ID [SAMPLE_ID ...]
                            One or more samples to treat as unrelated
                            individuals and identify variants matching a
                            recessive inheritance pattern.
                            
      --singleton_dominant SAMPLE_ID [SAMPLE_ID ...], -singleton_dominant SAMPLE_ID [SAMPLE_ID ...]
                            One or more samples to treat as unrelated
                            individuals and identify variants matching a
                            dominant inheritance pattern.
                            
      --seg_controls SAMPLE_ID [SAMPLE_ID ...], -seg_controls SAMPLE_ID [SAMPLE_ID ...]
                            One or more sample IDs to treat as controls for
                            segregation analysis only. Useful if you want to
                            specify controls to use for rejecting compound
                            heterozygous combinations of variants or
                            homozygous variants when using --biallelic option.
                            Unlike the --controls option, alleles/variants
                            present in these samples will only be used for
                            filtering when looking at inheritance patterns in
                            families present in a PED file or samples
                            specified with --singleton_recessive or
                            --singleton_dominant options. This option is not
                            necessary if your unaffected samples are already
                            present in your PED file specified with --ped.
                            

    Help/Logging Arguments:
      --prog_interval N, -prog_interval N
                            Report progress information every N variants.
                            Default=1000.
                            
      --log_progress, -log_progress
                            Use logging output for progress rather than wiping
                            progress line after each update.
                            
      --quiet               Do not output progress information to STDERR.
                            
      --debug               Output debugging information to STDERR.
                            
      -h, --help            Show this help message and exit
                        

## AUTHOR

Written by David A. Parry at the University of Edinburgh. 

## COPYRIGHT AND LICENSE

MIT License

Copyright (c) 2017 David A. Parry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



