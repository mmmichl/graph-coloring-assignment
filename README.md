# Graph Coloring Assignment for University Assignment


## Parameter Optimization

Install https://github.com/sfalkner/SpySMAC

command:
```
../../venv-smac3/bin/python ../SMAC3/scripts/smac --scenario scenario-5.txt --verbose_level DEBUG
```

### test run 1
failed, as all runs are timeouts?!

```
2018-06-11 07:57:44:DEBUG:smac.tae.execute_ta_run_old.ExecuteTARunOld:Stderr:
2018-06-11 07:57:44:DEBUG:smac.tae.execute_ta_run_old.ExecuteTARunOld:Return: Status: <StatusType.TIMEOUT: 2>, cost: 9000.000000, time: 900.000000, additional: {}
2018-06-11 07:57:44:DEBUG:smac.intensification.intensification.Intensifier:Add run of challenger
2018-06-11 07:57:44:DEBUG:smac.intensification.intensification.Intensifier:Budget exhausted; Return incumbent
2018-06-11 07:57:44:DEBUG:root:Remaining budget: -57.787612 (wallclock), inf (ta costs), 386.000000 (target runs)
2018-06-11 07:57:44:DEBUG:smac.stats.stats.Stats:Saving stats to smac3-output_2018-06-11_00:56:46_230015/run_1/stats.json
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:##########################################################
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:Statistics:
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:#Incumbent changed: 0
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:#Target algorithm runs: 114 / 500.0
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:Used wallclock time: 25257.80 / 25200.00 sec
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:Used target algorithm runtime: 122222234610.00 / inf sec
2018-06-11 07:57:44:DEBUG:smac.stats.stats.Stats:Debug Statistics:
2018-06-11 07:57:44:DEBUG:smac.stats.stats.Stats:Average Configurations per Intensify: 2.00
2018-06-11 07:57:44:DEBUG:smac.stats.stats.Stats:Exponential Moving Average of Configurations per Intensify: 2.00
2018-06-11 07:57:44:INFO:smac.stats.stats.Stats:##########################################################
2018-06-11 07:57:44:INFO:smac.facade.smac_facade.SMAC:Final Incumbent: Configuration:
  -A, Value: 10
  -alpha, Value: 0.6
  -p-max, Value: 1000
```

## Graph kategories

### tiny

data/myciel3.col
data/myciel4.col
data/myciel5.col
data/myciel6.col

### small (random graphs)

data/DSJC125.1.col
data/DSJC125.5.col
data/DSJC250.1.col
data/DSJC250.5.col
data/DSJR500.1.col
data/DSJR500.1c.col
data/DSJR500.5.col

### medium (leighton graphs)

data/le450_15a.col
data/le450_15b.col
data/le450_25a.col
data/le450_25b.col
data/le450_5a.col
data/le450_5b.col

### big (flat graphs

data/flat1000_50_0.col
data/flat1000_60_0.col
data/flat1000_76_0.col



### k-color targets (< 1 min)

data/DSJC125.1.col 	6 (5)
data/DSJC125.5.col 	18 (17)
data/flat1000_50_0.col 	100+
data/flat1000_60_0.col 	100+
data/flat300_20_0.col 	62 (61)
data/flat300_28_0.col 	53 (52)
data/le450_15b.col 	27 (26)
data/le450_25b.col 	33 (32)



data/DSJC125.1.col 	    6
data/DSJC125.5.col 	    25
data/DSJC250.1.col 	    13
data/DSJC250.5.col 	    48
data/DSJR500.1.col 	    14
data/DSJR500.1c.col 	100+
data/DSJR500.5.col 	    100+
data/flat1000_50_0.col 	100+
data/flat1000_60_0.col 	100+
data/flat1000_76_0.col 	100+
data/le450_15a.col 	    28
data/le450_15b.col 	    27
data/le450_25a.col 	    33
data/le450_25b.col 	    33
data/le450_5a.col 	    13
data/le450_5b.col 	    15
data/myciel3.col        4
data/myciel4.col        5
data/myciel5.col 	    5
data/myciel6.col 	    6



### graph descriptions

random graphs: dsjcX.Y
flat graphs: flatX.Y
Leighton graphs: leX.Y
two families of random geometrical graphs: dsjrX.Y and rX.Y




.....................................................................................................................................................