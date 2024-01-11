import warnings
from mwk_traceback import compact_warn, super_compact_warn

warnings.formatwarning = compact_warn

warnings.warn('This is warning', DeprecationWarning)

warnings.formatwarning = super_compact_warn

warnings.warn('This is another warning', UserWarning)
