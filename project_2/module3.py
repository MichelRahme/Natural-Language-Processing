import commands
import subproject_1

# Read command line arguments
args = commands.init_params()

# Call the function and return result
commands.output(subproject_1.postings_list(args.input_file))