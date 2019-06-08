declare -a arr=("A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z")
for i in "${arr[@]}"
do
   echo "$i"
   convert "$i"/* +append "$i".png
   # or do whatever with individual element of the array
done
