from vase.annotation_filter import AnnotationFilter


class InfoFilter(AnnotationFilter):
    '''
        A class for filtering on given INFO fields in a VCF
    '''

    def __init__(self, vcf, filters):
        '''
            Args:
                vcf:    VcfReader object from vase

                filters:
                        iterable of tuples of field names, operands and
                        values for filtering.

        '''
        super().__init__(vcf=vcf, field='info', filters=filters)
