import { Pie } from "react-chartjs-2";
import { fallbackColors } from "./colors";

function PieChart({ data = [] }) {
  const labels = data.map(d => d.equipment_type || "Unknown");
  const counts = data.map(d => d.count || 0);

  const chartData = {
    labels,
    datasets: [
      {
        data: counts,
        backgroundColor: fallbackColors,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Equipment Type Distribution",
        font: { size: 18 },
      },
      legend: { position: "top" },
      tooltip: {
        callbacks: {
          label: (ctx) => {
            return `${ctx.label}: ${ctx.raw}`;
          },
        },
      },
    },
  };

  return (
    <div style={{ height: "300px" }}>
      <Pie data={chartData} options={options} />
    </div>
  );
}

export default PieChart;
