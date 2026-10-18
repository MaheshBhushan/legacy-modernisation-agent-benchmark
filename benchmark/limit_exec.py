"""Set child resource limits before exec without a threaded preexec callback."""

import os
import resource
import sys

resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
os.execvp(sys.argv[1], sys.argv[1:])
