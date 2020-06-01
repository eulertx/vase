vase -i ex1.vcf --af 0.4 --ac 5 --info_filters 'FS < 1' 'DB = True' | python3 ../utils/vcf2vars.py  -  > expected_outputs/test_info_filters.txt

vase -i ex1.vcf --max_alt 1 --keep_filters VQSRTrancheSNP99.90to99.95 | python3 ../utils/vcf2vars.py -  > expected_outputs/test_alts_filters.txt

vase -i ex1.vcf --csq | ../utils/vcf2vars.py - > expected_outputs/test_csq.txt

vase -i ex1.vcf --impact HIGH | ../utils/vcf2vars.py - > expected_outputs/test_impact.txt

vase -i ex1.vcf  --var_type INDEL --pass  --max_alt 1 | ../utils/vcf2vars.py > expected_outputs/test_vartype.txt

vase -i ex1.vcf --ped test.ped  --de_novo | ../utils/vcf2vars.py > expected_outputs/test_de_novo.txt

vase -i ex1.vcf --ped test.ped  --de_novo --max_alt 1  | ../utils/vcf2vars.py > expected_outputs/test_de_novo2.txt

vase -i ex1.vcf --ped test.ped  --de_novo --het_ab 0.25 --max_alt 1  | ../utils/vcf2vars.py > expected_outputs/test_de_novo3.txt

vase -i ex1.vcf --ped test.ped  --biallelic  --csq | ../utils/vcf2vars.py > expected_outputs/test_biallelic.txt

vase -i ex1.vcf --ped test.ped  --biallelic --impact HIGH MODERATE | ../utils/vcf2vars.py > expected_outputs/test_biallelic2.txt

vase -i ex1.vcf --ped test.ped  --biallelic --impact HIGH  | ../utils/vcf2vars.py > expected_outputs/test_biallelic3.txt

vase --ped test2.ped -i ex1.vcf --dominant --csq | ../utils/vcf2vars.py > expected_outputs/test_dominant.txt

vase -i ex1.vcf --cases Sample3 Sample2 --controls Sample1 | ../utils/vcf2vars.py > expected_outputs/test_case_control