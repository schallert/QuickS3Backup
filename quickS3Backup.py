import sys, os
try:
	import simplejson as json
except:
	import json
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket

# Configure S3 authentication
config = json.load(open('config.json'))
key_id = config['aws']['AWS_ACCESS_KEY_ID']
secret_key = config['aws']['AWS_SECRET_ACCESS_KEY']
db_bucket_name = config['aws']['BACKUP_BUCKET']

# Function to check that we are given input files
def checkFilesExist(sysarg_array):
	if len(sysarg_array) > 0:
		return sysarg_array
	else:
		sys.exit('File names not provided')

# Construct the prefix (i.e. S3 folder) for the key, and input files
# from command line accordingly
if sys.argv[1] == '-p':
	folder_prefix = sys.argv[2]
	input_files = checkFilesExist(sys.argv[3:])
else:
	folder_prefix = None
	input_files = checkFilesExist(sys.argv[1:])

# Make sure we are given files that actually exist
for f in input_files:
	try:
		open(f)
	except IOError:
		sys.exit('Could not access file: ' + f)

# Create the S3 connection
s3conn = S3Connection(key_id, secret_key)

# Check if there's already a bucket for the desired bucket name
if not db_bucket_name in [b.name for b in s3conn.get_all_buckets()]:
	db_bucket = s3conn.create_bucket(db_bucket_name)
else:
	db_bucket = s3conn.get_bucket(db_bucket_name)

# Callback function to print percentage
# It's super janky, I know. I'll work on it
def cbf(trans, total):
	percent = int((float(trans)/total) * 100)
	if percent == 0:
		sys.stdout.write('[')
		for i in xrange(50):
			sys.stdout.write(' ')
		sys.stdout.write(']\n ')
		sys.stdout.flush()
	elif (trans/total) == 1:
		print '='
	else:
		sys.stdout.write('=')
		sys.stdout.flush()

# Send the files to the server
for file_to_send in input_files:
	file_path = os.path.join(os.getcwd(), file_to_send)
	key = Key(db_bucket)
	# Only append the actual filename, we dont want to send the whole path
	file_name = os.path.basename(file_to_send)
	# Prepend the folder prefix we defined if necessary
	key.key = folder_prefix + '/' + file_name if folder_prefix else file_name
	# Actually send the file, set our callback and number of times to call it
	key.set_contents_from_filename(file_path, cb=cbf, num_cb=50)
	key.close()