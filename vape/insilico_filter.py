import re
import os

vep_internal_pred_re = re.compile(r'\(\d(\.\d+)?\)') 
# for removing numbers in brackets at end of PolyPhen, SIFT and Condel VEP 
# annotations

class InSilicoFilter(object):
    ''' 
        Stores in silico prediction formats for VEP and indicates 
        whether a given variant consequence should be filtered on the 
        basis of the options provided on initialization. Data on the in 
        silico formats recognised are stored in the text file 
        "data/vep_insilico_pred.tsv"

    '''
    
    
    def __init__(self, programs, filter_unpredicted=False, 
                 keep_if_any_damaging=False):
        ''' 
            Initialize with a list of program names to use as filters.

            Args:
                programs:   A list of in silico prediction programs to 
                            use for filtering. These must be present in 
                            the VEP annotations of a VcfRecord as added 
                            either directly by VEP or via the dbNSFP VEP 
                            plugin. You may also optionally specify 
                            score criteria for filtering as in the the 
                            following examples:
                                                FATHMM_pred=D
                                                MutationTaster_pred=A
                                                MetaSVM_rankscore=0.8
            
                            Or you may just provide the program names 
                            and the default 'damaging' prediction values 
                            will be used, as listed in the file
                            "data/vep_insilico_pred.tsv". 

                            The filter() function, which must be 
                            provided with dict of VEP consequences to 
                            values, will return False if ALL of the 
                            programs provided here contain appropriate
                            prediction values or have no prediction.
                            This behaviour can be modified with the 
                            keep_if_any_damaging/filter_unpredicted
                            arguments.

                filter_unpredicted: 
                            The default behaviour is to ignore a program
                            if there is no prediction given (i.e. the 
                            score/pred is empty). That is, if there are 
                            no predictions for any of the programs 
                            filter() will return False, while if 
                            predictions are missing for only some, 
                            filtering will proceed as normal, ignoring 
                            those programs with missing predictions. If 
                            this argument is set to True, filter() will
                            return True if any program does not have a
                            prediction/score.

                keep_if_any_damaging:
                            If set to True, filter() will return False
                            if ANY of the given programs has a 
                            matching prediction/score unless 
                            'filter_unpredicted' is True and a 
                            prediction/score is missing for any program.

        '''

        self.filter_unpredicted = filter_unpredicted
        self.keep_if_any_damaging = keep_if_any_damaging
        self.pred_filters = {}
        self.score_filters = {}
        default_progs = {}
        case_insensitive = {}
        self.lower_more_damaging = set()
        pred_file = os.path.join(os.path.dirname(__file__), "data", 
                                 "vep_insilico_pred.tsv")
        with open(pred_file, encoding='UTF-8') as insilico_d:
            for line in insilico_d:
                if line.startswith('#'):
                    continue
                cols = line.rstrip().split('\t')
                case_insensitive[cols[0].lower()] = cols[0]
                if cols[0] in default_progs:
                    if cols[2] in default_progs[cols[0]]:
                        default_progs[cols[0]][cols[2]].append(cols[1])
                    elif cols[2] != 'score' :
                        default_progs[cols[0]][cols[2]] = [cols[1]]
                    else:
                        raise Exception("Error in data/vep_insilico_pred.tsv:"+
                                        " Should only have one entry for " + 
                                        "score prediction '{}'".format(cols[0])
                                        )
                else:
                    if cols[2] != 'score':
                        default_progs[cols[0]] = {'type' : 'pred'}
                        default_progs[cols[0]][cols[2]] = [cols[1]]
                    else:
                        default_progs[cols[0]] = {'type' : 'score', 
                                                  'default' : float(cols[1])}
                if len(cols) >= 4:
                    if cols[3] == 'lower=damaging':
                        self.lower_more_damaging.add(cols[0])
        for prog in programs:
            split = prog.split('=')
            pred = None
            if len(split) > 1:
                prog = split[0]
                pred = split[1]
            if prog.lower() in case_insensitive:
                prog = case_insensitive[prog.lower()]
            else:
                raise Exception("ERROR: in silico prediction program '{}' "
                                .format(prog) + "not recognised.")
            if pred is not None:
                if default_progs[prog]['type'] == 'score':
                    try:
                        score = float(pred)
                        self.score_filters[prog] = score
                    except ValueError:
                        raise Exception("ERROR: {} score must be numeric. " 
                                        .format(prog) + "Could not convert " +
                                        "value '{}' to a number.".format(pred))
                elif (pred in default_progs[prog]['default'] or 
                     pred in default_progs[prog]['valid']):
                    if prog in self.pred_filters[prog]:
                        self.pred_filters[prog].add(pred)
                    else:
                        self.pred_filters[prog] = set(pred)
                else:
                    raise Exception("ERROR: score '{}' not " .format(pred) +
                                    "recognised as valid for in silico " + 
                                    "prediction program '{}' ".format(prog))
            else:            
                if default_progs[prog]['type'] == 'score':
                    score = float(default_progs[prog]['default'])
                    self.score_filters[prog] = score
                else:
                    self.pred_filters[prog] = default_progs[prog]['default']

    def filter(self, csq):
        ''' 
            Returns False if prediction matches filters for given 
            consequence, otherwise returns True.
        
            Args:
                csq: dict of VEP consequence fields to values, as 
                     provided by the CSQ property of a VcfRecord object.

        '''
        
        for prog in self.pred_filters:
            if csq[prog] != '':
                do_filter = True
                for p in csq[prog].split('&'):
                    p = vep_internal_pred_re.sub('', p)
                    if p in self.pred_filters[prog]: #matches - don't filter
                        do_filter = False
                        break
                if self.keep_if_any_damaging and not do_filter: #matched
                    return False
                elif do_filter:                #haven't matched - filter
                    return True
            elif self.filter_unpredicted:
                    return True
        for prog in self.score_filters:
            if csq[prog] == '':
                if self.filter_unpredicted:
                    return True
            else:
                do_filter = True
                for p in csq[prog].split('&'):
                    try:
                        score = float(p)
                    except ValueError: 
                        continue
                    if prog in self.lower_more_damaging:
                        if score <= self.score_filters[prog]: #
                            do_filter = False
                            break
                    else:
                        if score >= self.score_filters[prog]: #
                            do_filter = False
                            break
                if self.keep_if_any_damaging and not do_filter:
                    return False
                elif do_filter:
                    return True #score not over threshold - filter
        return False

