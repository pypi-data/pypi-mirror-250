# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.manip namespace
"""

import sys as _sys

from tensorflow.python.ops.gen_array_ops import batch_to_space_nd # line: 343
from tensorflow.python.ops.gen_array_ops import reverse_v2 as reverse # line: 9140
from tensorflow.python.ops.gen_array_ops import scatter_nd # line: 9276
from tensorflow.python.ops.gen_array_ops import space_to_batch_nd # line: 10076
from tensorflow.python.ops.gen_array_ops import tile # line: 11970
from tensorflow.python.ops.array_ops import gather_nd # line: 5122
from tensorflow.python.ops.array_ops import reshape # line: 63
from tensorflow.python.ops.manip_ops import roll # line: 27

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "manip", public_apis=None, deprecation=False,
      has_lite=False)
