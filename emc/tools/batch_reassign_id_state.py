from pathlib import Path

min_new_id = 807
min_old_id = 797
diff = min_new_id - min_old_id

import re

for i in Path("history/states").iterdir():
	m = re.match(r"([0-9]+)-(.+)", i.name)
	assert m is not None
	if int(m.group(1)) < min_old_id or int(m.group(1)) >= min_new_id:
		continue
		
	new_name = f"{int(m.group(1))+diff}-{m.group(2)}"
	print(f'mv "{i}" "{i.parent / new_name}"')