# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-05 21:02:50
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-05 21:08:40

from math import sqrt

scope = {}
exec('sqrt = 1', scope)
print(len(scope))
print(sqrt(4))
print(scope.keys())
girls = ['alice', 'bernice', 'clarice', 'Abigail', 'Ada', 'Adela', 'Adelaide', 'Afra', 'Agatha', 'Agnes', 'Alberta', 'Alexia', 'Alice', 'Alma', 'Althea', 'Alva', 'Amanda', 'Amelia', 'Amy', 'Anastasia', 'Andrea', 'Angela', 'Ann', 'Anna', 'Annabelle', 'Antonia', 'April', 'Arabela', 'Arlene', 'Astrid', 'Atalanta', 'Athena', 'Audrey', 'Aurora', 'Barbara', 'Beatrice', 'Belinda', 'Bella', 'Belle', 'Bernice', 'Bertha', 'Beryl', 'Bess', 'Betsy', 'Betty', 'Beulah',
         'Beverly', 'Blanche', 'Bblythe', 'Bonnie', 'Breenda', 'Bridget', 'Brook', 'Camille', 'Candance', 'Candice', 'Cara', 'Carol', 'Caroline', 'Catherine', 'Cathy', 'Cecilia', 'Celeste', 'Charlotte', 'Cherry', 'Cheryl', 'Chloe', 'Christine', 'Claire', 'Clara', 'Clementine', 'Constance', 'Cora', 'Coral', 'Cornelia', 'Crystal', 'Cynthia', 'Daisy', 'Dale', 'Dana', 'Daphne', 'Darlene', 'Dawn', 'Debby', 'Deborah', 'Deirdre', 'Delia', 'Denise', 'Diana', 'Dinah']
boys = ['chirs', 'arnoid', 'bob']
letterGirls = {}
for gril in girls:
    letterGirls.setdefault(gril[0].lower(), []).append(gril)
print(letterGirls)
