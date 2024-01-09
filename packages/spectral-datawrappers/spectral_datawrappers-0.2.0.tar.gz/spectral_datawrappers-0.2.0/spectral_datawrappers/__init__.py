# from .data_wrapper_a import DataWrapperA
from spectral_datawrappers.credit_scoring.credit_scoring_wrapper import CreditScoringWrapper

AVAILABLE_WRAPPERS = {
    #    'service_a': DataWrapperA,
    'credit_scoring': CreditScoringWrapper
}
