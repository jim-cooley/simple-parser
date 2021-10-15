#
# state & token values
#
from statedef import ST
from tokens import TK

tkVal = {
    ST.MAIN: 'st_main',
    ST.IDNT: 'st_ident',
    ST.INT:  'st_int',
    ST.FLOT: 'st_float',
    ST.WHT:  'st_white',
    ST.SCMT: 'st_scmtx',
    ST.SQOT: 'st_sqts',
    ST.DQOT: 'st_dqts',
    ST.CMCT: 'st_ccmtx',
    ST.SLSH: 'st_slshs',
    ST.STAR: 'st_stars',
    ST.PMCT: 'st_pmtx',
    ST.SQT1: 'st_psqt1',
    ST.SQT2: 'st_psqt2',
    ST.SQT3: 'st_psqt3',
    ST.SQT4: 'st_psqt4',
    ST.GTR2: 'st_2gtr',
    ST.LSS2: 'st_2lss',

    TK.WHT: 'tk_white',
    TK.IDNT: 'tk_ident',
    TK.INT: 'tk_int',
    TK.FLOT: 'tk_float',
    TK.STR: 'tk_str',
    TK.USCR: 'tk_uscr',
    TK.SEMI: 'tk_semi',
    TK.COMA: 'tk_coma',
    TK.DOT: 'tk_dot',
    TK.COLN: 'tk_coln',
    TK.MNUS: 'tk_mnus',
    TK.PLUS: 'tk_plus',
    TK.STAR: 'tk_star',
    TK.SLSH: 'tk_slsh',
    TK.BSLH: 'tk_bslsh',
    TK.PCT: 'tk_pct',
    TK.EXPN: 'tk_expn',
    TK.EQLS: 'tk_eqls',
    TK.LBS: 'tk_lbs',
    TK.QUOT: 'tk_quot',
    TK.EXCL: 'tk_exclm',
    TK.QSTN: 'tk_qstn',
    TK.AMPS: 'tk_amps',
    TK.DLRS: 'tk_dlrs',
    TK.ATS: 'tk_ats',
    TK.BAR: 'tk_bar',
    TK.GTR: 'tk_gtr',
    TK.LESS: 'tk_less',
    TK.LBRC: 'tk_lbrc',
    TK.RBRC: 'tk_rbrc',
    TK.LPRN: 'tk_lprn',
    TK.RPRN: 'tk_rprn',
    TK.LBRK: 'tk_lbrk',
    TK.RBRK: 'tk_rbrk',
    TK.TLDE: 'tk_tlde',

    TK.LBAR: 'tk_lbar',  # <|
    TK.RBAR: 'tk_rbar',  # >|
    TK.GTR2: 'tk_2gtr',  # >>
    TK.GTE: 'tk_gte',  # >=
    TK.LSS2: 'tk_2lss',  # <<
    TK.LTE: 'tk_lte',  # <=
    TK.NEQ: 'tk_nte',  # !=
    TK.EQEQ: 'tk_eqeq',  # ==
    TK.BAR2: 'tk_bar2',  # ||
    TK.AMP2: 'tk_amp2',  # &&
    TK.TIME: 'tk_time',
    TK.DUR: 'tk_dur',  # 1s, m, d, w, m, ...

    TK.BUY: 'tk_buy',
    TK.SELL: 'tk_sell',
    TK.SIGNAL: 'tk_signal',
    TK.AND: 'tk_and',
    TK.OR: 'tk_or',

    TK.ERR: 'tk_error',
    TK.INVALID: 'tk_invalid',

    TK.EOF: 'tk_eof',
}
