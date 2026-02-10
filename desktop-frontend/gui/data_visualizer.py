import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure



class DataVisualizer:
    def __init__(self, figure):
        self.figure = figure

    def clear(self):
        self.figure.clear()

    def create_dashboard(self, dataset_details, distribution):
        self.clear()
        # Create gird
        grid_size = self.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        equipment_data = dataset_details.get('equipment', [])

        # if equipment data is not there
        if not equipment_data:
            axis = self.figure.add_subplot(111)
            axis.text(0.5, 0.5, 'No equipment data to show', ha='center', va='center', fontsize=14)
            axis.axis('off')
            return

        axis1 = self.figure.add_subplot(grid_size[0, 0])
        self.plot_type_distribution(axis1, distribution)

        axis2 = self.figure.add_subplot(grid_size[0, 1])
        self.plot_avg_by_type(axis2, equipment_data)

        axis3 = self.figure.add_subplot(grid_size[1, 0])
        self.plot_flowrate_vs_pressure(axis3, equipment_data)

        axis4 = self.figure.add_subplot(grid_size[1, 1])
        self.plot_temperature_distribution(axis4, equipment_data)

        filename = dataset_details.get('filename', 'Dataset')
        self.figure.suptitle(f"Equipment Analysis Dashboard - {filename}", fontsize=14, fontweight='bold')

    def plot_type_distribution(self, axis, distribution):
        if not distribution or 'distribution' not in distribution:
            axis.text(0.5, 0.5, 'No distribution to show', ha='center', va='center')
            axis.axis('off')
            return

        dist = distribution['distribution']
        types = [d['equipment_type'] for d in dist]
        counts = [d['count'] for d in dist]

        # cm = colormap
        colors = plt.cm.Set3(range(len(types)))
        wedges, texts, autotexts = axis.pie(counts, labels=types, colors=colors, autopct='%1.1f%%',
                                            startangle=90, shadow=True)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        axis.set_title('Equipment Type Distribution', fontweight='bold', fontsize=11)


    def plot_avg_by_type(self, axis, equipment_data):
        type_stats = {}
        for equipment in equipment_data:
            eq_type = equipment.get('equipment_type', 'Unknown')
            if eq_type not in type_stats:
                type_stats[eq_type] = {
                    'flowrates': [],
                    'pressures': [],
                    'temperatures': []
                }
            type_stats[eq_type]['flowrates'].append(equipment.get('flowrate', 0))
            type_stats[eq_type]['pressures'].append(equipment.get('pressure', 0))
            type_stats[eq_type]['temperatures'].append(equipment.get('temperature', 0))

        types = list(type_stats.keys())
        avg_flowrates = [np.mean(type_stats[t]['flowrates']) for t in types]
        avg_pressures = [np.mean(type_stats[t]['pressures']) for t in types]
        avg_temperatures = [np.mean(type_stats[t]['temperatures']) for t in types]

        x = np.arange(len(types))
        width = 0.3

        # TODO: encapsulate below duplicate code in future
        bars1 = axis.bar(x - width, avg_flowrates, width, label="Flowrate", color="#3498db")
        bars2 = axis.bar(x, avg_pressures, width, label="Pressure", color="#e74c3c")
        bars3 = axis.bar(x + width, avg_temperatures, width, label="Temperature", color="#f39c12")

        axis.set_xlabel('Equipment Type', fontweight='bold')
        axis.set_ylabel('Average Value', fontweight='bold')
        axis.set_title('Average Parameters by Type', fontweight='bold', fontsize=11)
        axis.set_xticks(x)
        axis.set_xticklabels(types, rotation=45, ha='right', fontsize=9)
        axis.legend(fontsize=8)
        axis.grid(axis='y', alpha=0.3)
        axis.set_xscale('linear')
        axis.set_yscale('linear')

    def plot_flowrate_vs_pressure(self, axis, equipment_data):
        type_data = {}

        for equipment in equipment_data:
            eq_type = equipment.get('equipment_type', 'Unknown')
            if eq_type not in type_data:
                type_data[eq_type] = {
                    'flowrates': [],
                    'pressures': [],
                }
            type_data[eq_type]['flowrates'].append(equipment.get('flowrate', 0))
            type_data[eq_type]['pressures'].append(equipment.get('pressure', 0))

        colors = plt.cm.Set2(range(len(type_data)))

        for x, (eq_type, data) in enumerate(type_data.items()):
            axis.scatter(data['flowrates'], data['pressures'],
                         label=eq_type, color=colors[x],
                         s=100, alpha=0.6, edgecolors='black', linewidths=0.5)

        axis.set_xlabel('Flowrate', fontweight='bold')
        axis.set_ylabel('Pressure', fontweight='bold')
        axis.set_title('Flowrate vs. Pressure by type', fontweight='bold', fontsize=11)
        axis.legend(fontsize=8, loc='best')
        axis.grid(axis='y', alpha=0.3)
        axis.set_xscale('linear')
        axis.set_yscale('linear')

    def plot_temperature_distribution(self, axis, equipment_data):

        temperatures = [equipment.get('temperature', 0) for equipment in equipment_data]
        # Reject if no variance in temps
        if not temperatures or len(set(temperatures)) <= 1:
            axis.text(0.5, 0.5, "Not enough temperature variation",
                      ha="center", va="center")
            axis.axis("off")
            return

    #    histogram
        n, bins, patches = axis.hist(temperatures, bins=8, color='#2ecc71',
                                     alpha=0.7, edgecolor='black')

        cm = plt.cm.RdYlGn_r

        # Used to prevent infinity error
        min_t = min(temperatures)
        max_t = max(temperatures)

        if min_t == max_t:
            max_t += 1
        norm = plt.Normalize(vmin=min_t, vmax=max_t)

        for i, patch in enumerate(patches):
            patch.set_facecolor(cm(norm(bins[i])))

        axis.set_xlabel('Temperature', fontweight='bold')
        axis.set_ylabel('Frequency', fontweight='bold')
        axis.set_title('Temperature Distribution', fontweight='bold', fontsize=11)
        axis.grid(axis='y', alpha=0.3)

    #     avg line
        if len(temperatures) == 0:
            return

        avg_temp = np.mean(temperatures)

        axis.axvline(avg_temp, color='red', linestyle='--', linewidth=2,
                     label=f'Average: {avg_temp:.1f}')
        axis.legend(fontsize=8)
        axis.set_xscale('linear')
        axis.set_yscale('linear')

    def create_detailed_view(self, dataset_details):
        self.clear()
        equipment_data = dataset_details.get('equipment_data', [])

        if not equipment_data:
            axis = self.figure.add_subplot(111)
            axis.text(0.5, 0.5, 'No equipment data available',
                      ha='center', va='center', fontsize=14)
            axis.axis('off')
            return

        axis = self.figure.add_subplot(111)

        names = [eq.get('name', 'Unknown') for eq in equipment_data]
        flowrates = [eq.get('flowrate', 0) for eq in equipment_data]
        pressures = [eq.get('pressure', 0) for eq in equipment_data]
        temperatures = [eq.get('temperature', 0) for eq in equipment_data]

        x = np.arange(len(names))
        width = 0.25

        bars1 = axis.bar(x - width, flowrates, width, label="Flowrate", color="#3498db")
        bars2 = axis.bar(x, pressures, width, label="Pressure", color="#e74c3c")
        bars3 = axis.bar(x + width, temperatures, width, label="Temperature", color="#f39c12")

        axis.set_xlabel('Equipment Type', fontweight='bold')
        axis.set_ylabel('Value', fontweight='bold')
        axis.set_title(f'Equipment Parameters - {dataset_details.get("filename", "dataset")}',
                       fontweight='bold', fontsize=11)
        axis.set_xticks(x)
        axis.set_xticklabels(names, rotation=45, ha='right')
        axis.legend()
        axis.grid(axis='y', alpha=0.3)

        # self.figure.tight_layout() doesnt leave space for title
        self.figure.tight_layout(rect=[0, 0.03, 1, 0.95])

    def create_statistics_summary(self, dataset_details):
        self.clear()
        axis = self.figure.add_subplot(111)
        axis.axis('off')

        stats_text = f"""
        Dataset Statistics Summary
        {'=' * 50}
        Filename: {dataset_details.get('filename', 'N/A')}
        Total Equipment: {dataset_details.get('total_count', 0)}
        
        Average Values:
        ───────────────
        Flowrate:     {dataset_details.get('avg_flowrate', 0):.2f}
        Pressure:     {dataset_details.get('avg_pressure', 0):.2f}
        Temperature:  {dataset_details.get('avg_temperature', 0):.2f}
        
        Uploaded: {dataset_details.get('uploaded_at', 'N/A')}
        """

        axis.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
                  verticalalignment='center', bbox=dict(boxstyle='round',facecolor="wheat", alpha=0.5))
