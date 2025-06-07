
import sys
from interpreter import Interpreter
from utils import *

def main():
    """
    Entry point for the RPAL lexical analyzer and parser.

    Reads the file name from the command line arguments and reads the file.

    Returns: None
    """

    # initialize args
    args = sys.argv
    file_name, switch = init_args(args)
        
    # Read the file "file_name"
    program = read_file(file_name)
  
    interpreter = Interpreter(program, switch)
    interpreter.interpret()
    print(interpreter.get_result(switch))
    return

if __name__ == "__main__":
    main()