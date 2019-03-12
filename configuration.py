
# Number based upon linear trend from 2013&2015 elections
NUM_LEGAL_VOTERS = 5500000

# Percents, based on random internet polls. updated at 2019-03-01
# https://www.israelhayom.co.il/article/637177
CANDIDATES = {
    "KAHOL_LAVAN": 18.6,
    "LIKUD": 13.7,
    "HABAIT_HAYEHUDI": 4.9,
    "HAYAMIN_HAHADASH": 4.2,
    "MERETZ": 3.5,
    "HAAVODA": 3.5,
    "YAHADUT_HATORA": 3.5,
    "TAAL_HADASH": 3.5,
    "SHAS": 2.8,
    "ZEHUT": 2.1,
    "KULANU": 2.1,
    "GESHER": 1.4,
    "YISRAEL_BEITENU": 1.4,
    "RAAM_BALAD": 0.7,
    "PETEK_LAVAN": 2.1, # Based upon percent in 2013 & 2015
    None: 30, # non-voting. Based upon voting percent in 2013 & 2015
}

# Speculation
SURPLUS_AGREEMENT = [
    ("KAHOL_LAVAN", "HAAVODA"),
    ("LIKUD", "HABAIT_HAYEHUDI"),
    ("HAYAMIN_HAHADASH", "ZEHUT"),
    ("MERETZ", "TAAL_HADASH"),
    ("YAHADUT_HATORA", "SHAS"),
    ("KULANU", "GESHER"),
    ("YISRAEL_BEITENU",),
    ("RAAM_BALAD",),
]
