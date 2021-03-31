QCODES = r"\/Q[A-Z]{4}\/"

D_IZE = r"D\)[ \-A-Z0-9\n]*E\)"

MESSAGE = r"[\s\S]*CREATED"

MRLC = r"(?:RWY|RUNWAY) *[0-9]{2}[LRC]*(?:\/[0-9]{2}[LRC]*)* *(?:CLOSED|CLSD)"

FAAH = STAH = FALC = ATCA = SPAH = ACAH = AECA = r"(?:(?:[A-Z]{3})|(?:[0-9]{2}))[\-\/A-Z0-9 ,]{0,24}:*(?: [0-9\-]*)*(?:[ \n,]*[0-9: ]{4,5}-[0-9: ]{4,5})+"

PIAU = r"(?:ILS[A-Z0-9 ]*(?:RWY[0-9RLC ]{2,3})*(?: CAT [I]{1,3}[AB]*)*[A-Z0-9,\/ ]*(?:SUSPENDED|NOT AVBL))|(?:NOT AVAILABLE:\nILS[A-Z0-9 ]*RWY[0-9RLC ]{2,3}(?: CAT [I]{1,3}[AB]*)*)"

ICCT = r"(?:ILS|INSTRUMENT LANDING SYSTEM)[\) A-Z]* RWY[ 0-9RLC]* (?:OPERATING )*(?:ON TEST)*"

ICAS = ISAS = IGAS = ILAS = IUAS = r"(?:ILS\)*(?:[ A-Z]{4})* (?:GP )*(?:LOC )*(?:CAT [I\/AB]* )*(?:FOR )*RWY[ 0-9RLC\/]*)|(?:RWY[ 0-9RCL:\/]*ILS)"

FIAU = r".*"

