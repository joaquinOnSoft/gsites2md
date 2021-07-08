# /bin/bash
for i in `find $1 -type f`
do
    output=`echo $i | cut -d? -f1`
    if [ $i != $output ]
    then
        mv $i $ouput
    else
        echo "Skiping $i"
    fi
done