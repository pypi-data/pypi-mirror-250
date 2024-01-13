__version__ = '0.6.0'
__author__ = 'Mitchell Lisle'
__email__ = 'm.lisle90@gmail.com'

from queueplus.aioqueue import AioQueue, BloomFilterQueue, DataT, TypedAioQueue
from queueplus.violations import DiscardOnViolation, RaiseOnViolation, ViolationStrategy
