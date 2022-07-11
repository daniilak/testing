from lib import *

create_tmp_folders()

try:
    Path("res").mkdir(parents=True, exist_ok=True)
except Exception as e:
    print_error(e)

for i in range(1, 51):
    make_archive(str(i))

