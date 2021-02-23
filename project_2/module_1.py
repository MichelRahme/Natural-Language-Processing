import commands
import subproject_1

# Read command line arguments
args = commands.init_params()
# Set necessary variables. This variable contains the path to the Reuters folder passed in as a parameter when calling
path = args.path

# Call the function and return result
commands.output(subproject_1.process_files(path))
