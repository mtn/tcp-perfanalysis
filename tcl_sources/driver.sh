is=( 4_1 5_1 6_1 7_1 8_1 )
js=( 4_2 5_2 6_2 7_2 8_2 )
for idx in "${!is[@]}"; do
  i=${is[$idx]}
  j=${js[$idx]}
  paste "$i.txt" "$j.txt" >"$i.$j.txt"
done
# declare -a implementation_pairs=(
#     ["Reno"]="Reno"
#     ["Newreno"]="Reno"
#     ["Vegas"]="Vegas"
#     ["Newreno"]="Vegas"
# )

# for i in "${!implementation[@]}"; do
#     j=${implemention[$i]}
#     echo $j and $i
# done
# declare -A pairs=( [4_1]=4_2 [5_1]=5_2 [6_1]=6_2 [7_1]=7_2 [8_1]=8_2 )
# for i in "${!pairs[@]}"; do
#   j=${pairs[$i]}
#   paste "$i.txt" "$j.txt" >"${i}.${j}.txt"
# done
