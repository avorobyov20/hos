pwd
ls -la
ls -la app

echo "" >> ../versions.txt  # создаем файл, если его не существовало
ver=`head -1 app/version.toml`  # извлекаем первую строку из toml
sed -i "/^\s*$ver\s*$/d" ../versions.txt  # удаляем все вхождения этой строки из versions.txt
echo $ver >> ../versions.txt  # и добавляем ее в конец, теперь строка будет только в одном экземпляре
sed -i '/^\s*$/d' ../versions.txt  # удаляем из файла пустые и пробельные строки

echo 'master' > lastversions.txt
tail -n3 ../versions.txt >> lastversions.txt
sed -i 's/"/'""'/g' lastversions.txt # удаляем двойные кавычки
tac lastversions.txt > ../lastversions.txt
csvlines=$(tr '\n' ',' < ../lastversions.txt | sed 's/,$/\n/')
rm ../lastversions.txt
rm lastversions.txt

csvlines=$(echo $csvlines | sed "s/,version=/,/g")
echo $(echo $csvlines | sed "s/version=/release=/") > params.file

csvlines=$(tr '\n' ',' < deploy_hosts.list | sed 's/,$/\n/')
echo "server_ip="$csvlines >> params.file
mv params.file ../params.file
cat ../params.file
