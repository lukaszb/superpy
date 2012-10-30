
if !has('python')
    echo "Error: Required vim compiled with +python support"
    finish
endif

function! SuperpySuper()

python << EOF
import os
import vim
import sys

for p in vim.eval('&runtimepath').split(','):
        sys.path.append(os.path.join(p, 'plugin'))

import superpy
superpy.get_super()
EOF

endfunction

command! -nargs=0 SuperpySuper call SuperpySuper()

