for i in `ls -1 *.truss`
do
	python3 main.py `i` -v &
done
