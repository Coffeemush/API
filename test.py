import matplotlib.pyplot as plt
from datetime import datetime, timedelta

processed_data = [{'value': 24.134882499346823, 'time': '2022-11-02T07:35:58.401000'}, {'value': 14.82142001645127, 'time': '2022-11-02T06:35:58.401000'}, {'value': 12.744544421256546, 'time': '2022-11-02T05:35:58.401000'}, {'value': 28.576427675219392, 'time': '2022-11-02T04:35:58.401000'}, {'value': 20.83838368419518, 'time': '2022-11-02T03:35:58.401000'}, {'value': 27.894060691260243, 'time': '2022-11-02T02:35:58.401000'}, {'value': 21.120166971147864, 'time': '2022-11-02T01:35:58.401000'}, {'value': 15.865306803851952, 'time': '2022-11-02T00:35:58.401000'}, {'value': 19.499065474395806, 'time': '2022-11-01T23:35:58.401000'}, {'value': 28.10292770469235, 'time': '2022-11-01T22:35:58.401000'}, {'value': 23.91221881871156, 'time': '2022-11-01T21:35:58.401000'}, {'value': 15.316199614442406, 'time': '2022-11-01T20:35:58.401000'}, {'value': 15.748212534573543, 'time': '2022-11-01T19:35:58.401000'}, {'value': 19.492149962799992, 'time': '2022-11-01T18:35:58.401000'}, {'value': 20.5173755964213, 'time': '2022-11-01T17:35:58.401000'}, {'value': 25.89180577238764, 'time': '2022-11-01T16:35:58.401000'}, {'value': 12.936598623979004, 'time': '2022-11-01T15:35:58.401000'}]
values = [entry['value'] for entry in processed_data]
times = [datetime.fromisoformat(entry['time']) for entry in processed_data]

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(times, values, marker='o', linestyle='-', color='b')

# Format the plot
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Sensor Data Over Time')
plt.xticks(rotation=45)
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig('.debug/sensor_data_plot.png')