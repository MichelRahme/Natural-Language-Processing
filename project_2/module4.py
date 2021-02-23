import commands
import subproject_2

# Read command line arguments
args = commands.init_params()

# Set necessary variables. These variables contain the queries
query = args.query
path = args.path
input_file = args.input_file

# Call the function and return result
commands.output(subproject_2.query_processor(input_file, path, query))
