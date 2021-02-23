import commands
import subproject_3

# Read command line arguments
args = commands.init_params()

# Call the function and return result
commands.output(subproject_3.create_table())
