
set title 'Change in key lookup time as more nodes are disabled'
set xlabel 'Average time per lookup (s)'
set ylabel 'Trial'
set key left

f1(x) = m1*x + b1
fit f1(x) '0_train.dat' via m1,b1

f2(x) = m2*x + b2
fit f2(x) '5_train.dat' via m2,b2

f3(x) = m3*x + b3
fit f3(x) '10_train.dat' via m3,b3

f4(x) = m4*x + b4
fit f4(x) '15_train.dat' via m4,b4

f5(x) = m5*x + b5
fit f5(x) '20_train.dat' via m5,b5

f6(x) = m6*x + b6
fit f6(x) '25_train.dat' via m6,b6

plot '0_train.dat' title 'remove zero nodes per trial', f1(x) title 'Model fit', '5_train.dat' title 'remove five nodes per trial', f2(x) title 'Model fit',  '10_train.dat' title 'remove ten nodes per trial', f3(x) title 'Model fit', '15_train.dat' title 'remove fifteen nodes per trial', f4(x) title 'Model fit', '20_train.dat' title 'remove twenty nodes per trial', f5(x) title 'Model fit', '25_train.dat' title 'remove twenty-five nodes per trial', f6(x)title 'Model fit'

#set term eps



