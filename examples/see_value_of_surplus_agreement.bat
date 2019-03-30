
echo off
echo Without surplus agreement between ZEHUT and KAHOL-LAVAN
py -3 -m main --predict --num-iterations 100000 --conf-json config\default-2019-30-03.json
echo ======
echo With surplus agreement between ZEHUT and KAHOL-LAVAN
py -3 -m main --predict --num-iterations 100000 --conf-json config\surplus_agreement_counterfactual-2019-30-13.json
