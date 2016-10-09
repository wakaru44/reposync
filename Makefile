# A simple makefile to make things simpler

help:
	@echo "Troposphere code to generate a personal workstation in the cloud";
	@echo "";
	@echo "bump           - Bump the version file";
	@echo "todo           - show the TO DO's and tasks";
	@echo "updaterepos    - get a list of repos to download in workspace";
	@echo "";


bump:
	python -c "fh=open('version.md');c=fh.readline();n=map(lambda x: int(x),c.split('.'));print '.'.join(map(str, [n[0],n[1],n[2]+1]))"

todo:
	grep  -r "TODO:" * --exclude-dir ENV --exclude-dir env --exclude-dir env2 --exclude Makefile

updaterepos:
	bash tool_list_all_repos.sh && python tool_combine_repos.py | tee .ansible/repolist
