import Traffic as tf
import pandas as pd

trafficDataSet = pd.read_csv("D:\\AI_HW\\CHW1\\traffic_4weeks_clean.csv")
days = 5
times = 12

tf.ucs(trafficDataSet, times, days)
tf.a_star(trafficDataSet, times, days)