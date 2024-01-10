import os
try:
    from numba import njit
except ImportError:
    pass
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
class lo:
    '''
    Looping mathematical operations
    '''
    def find_multiplier(start: float, toi: float, outputstr: bool) -> float:
        '''
        Starts from inputted value `start` and returns multiplier to arrive to `toi` from `start`
        '''
        mult = 0
        out = 0
        while not out >= toi:
            mult += 0.01
            out = start * mult
        offset = start * mult - toi
        ostr = f'Multiplier to reach {toi} from {start} is about {mult}.\nOffset is {offset}.\nExact multiplier is impossible to find due to INSANE wait time'
        if outputstr:
            return ostr
        else:
            return mult
    def find_multiplier_o(start: float, toi: float, outputstr: bool) -> float:
        '''
        Same as `find_multiplier()` but finds offset instead
        '''
        mult = 0
        out = 0
        while not out >= toi:
            mult += 0.01
            out = start * mult
        offset = start * mult - toi
        ostr = f'Multiplier to reach {toi} from {start} is about {mult}.\nOffset is {offset}.\nExact multiplier is impossible to find due to INSANE wait time'
        if outputstr:
            return ostr
        else:
            return offset

class o():
    '''
    Mathematical operations
    '''
    def tan(x: float) -> float:
        import math
        return math.tan(x)

    def pi(digits: int) -> float:
        import os
        try:
            from mpmath import mp
        except ImportError:
            os.system('pip install mpmath')

        mp.dps = digits
        return mp.pi
    
    def pow(y1: float, y2: float) -> float:
        import math
        return math.pow(y1, y2)

class utilities():
    def quietinput(prompt: str) -> str:
        import contextlib
        import io
        import os
        import sys
        import warnings
        import msvcrt
        def unix_nechoinput(prompt='Password: ', stream=None):
            """Prompt for a password, with echo turned off.
            Args:
              prompt: Written on stream to ask for the input.  Default: 'Password: '
              stream: A writable file object to display the prompt.  Defaults to
                      the tty.  If no tty is available defaults to sys.stderr.
            Returns:
              The seKr3t input.
            Raises:
              EOFError: If our input tty or stdin was closed.
              nechoinputWarning: When we were unable to turn echo off on the input.
            Always restores terminal settings before returning.
            """
            passwd = None
            with contextlib.ExitStack() as stack:
                try:
                    # Always try reading and writing directly on the tty first.
                    fd = os.open('/dev/tty', os.O_RDWR|os.O_NOCTTY)
                    tty = io.FileIO(fd, 'w+')
                    stack.enter_context(tty)
                    input = io.TextIOWrapper(tty)
                    stack.enter_context(input)
                    if not stream:
                        stream = input
                except OSError:
                    # If that fails, see if stdin can be controlled.
                    stack.close()
                    try:
                        fd = sys.stdin.fileno()
                    except (AttributeError, ValueError):
                        fd = None
                        passwd = fallback_nechoinput(prompt, stream)
                    input = sys.stdin
                    if not stream:
                        stream = sys.stderr
                if fd is not None:
                    try:
                        old = termios.tcgetattr(fd)     # a copy to save
                        new = old[:]
                        new[3] &= ~termios.ECHO  # 3 == 'lflags'
                        tcsetattr_flags = termios.TCSAFLUSH
                        if hasattr(termios, 'TCSASOFT'):
                            tcsetattr_flags |= termios.TCSASOFT
                        try:
                            termios.tcsetattr(fd, tcsetattr_flags, new)
                            passwd = _raw_input(prompt, stream, input=input)
                        finally:
                            termios.tcsetattr(fd, tcsetattr_flags, old)
                            stream.flush()  # issue7208
                    except termios.error:
                        if passwd is not None:
                            # _raw_input succeeded.  The final tcsetattr failed.  Reraise
                            # instead of leaving the terminal in an unknown state.
                            raise
                        # We can't control the tty or stdin.  Give up and use normal IO.
                        # fallback_nechoinput() raises an appropriate warning.
                        if stream is not input:
                            # clean up unused file objects before blocking
                            stack.close()
                        passwd = fallback_nechoinput(prompt, stream)
                stream.write('\n')
                return passwd
            
        def win_nechoinput(prompt='Password: ', stream=None):
            """Prompt for password with echo off, using Windows getwch()."""
            if sys.stdin is not sys.__stdin__:
                return fallback_nechoinput(prompt, stream)
            for c in prompt:
                msvcrt.putwch(c)
            pw = ""
            while 1:
                c = msvcrt.getwch()
                if c == '\r' or c == '\n':
                    break
                if c == '\003':
                    raise KeyboardInterrupt
                if c == '\b':
                    pw = pw[:-1]
                else:
                    pw = pw + c
            msvcrt.putwch('\r')
            msvcrt.putwch('\n')
            return pw
        
        def fallback_nechoinput(prompt='Password: ', stream=None):
            warnings.warn("Can not control echo on the terminal.", nechoinputWarning,
                          stacklevel=2)
            if not stream:
                stream = sys.stderr
            print("Warning: Password input may be echoed.", file=stream)
            return _raw_input(prompt, stream)
        
        def _raw_input(prompt="", stream=None, input=None):
            # This doesn't save the string in the GNU readline history.
            if not stream:
                stream = sys.stderr
            if not input:
                input = sys.stdin
            prompt = str(prompt)
            if prompt:
                try:
                    stream.write(prompt)
                except UnicodeEncodeError:
                    # Use replace error handler to get as much as possible printed.
                    prompt = prompt.encode(stream.encoding, 'replace')
                    prompt = prompt.decode(stream.encoding)
                    stream.write(prompt)
                stream.flush()
            # NOTE: The Python C API calls flockfile() (and unlock) during readline.
            line = input.readline()
            if not line:
                raise EOFError
            if line[-1] == '\n':
                line = line[:-1]
            return line
        if os.name == 'nt':
            return win_nechoinput(prompt.replace(':', '(this is quiet input dont worry about no output):'))
        else:
            return unix_nechoinput(prompt.replace(':', '(this is quiet input dont worry about no output):'))
