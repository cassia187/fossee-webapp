import { Scatter } from "react-chartjs-2";
import { typeColors } from "./colors";

function ScatterChart({ points = [] }) {
  // GROUP BY TYPE SAFELY
  const groups = points.reduce((acc, p) => {
    const t = p.type || "Unknown";
    if (!acc[t]) acc[t] = [];
    acc[t].push({ x: p.x, y: p.y, name: p.name });
    return acc;
  }, {});

  const datasets = Object.keys(groups).map((type) => ({
    label: type,
    data: groups[type],
    backgroundColor: typeColors[type] || "#3b82f6",
  }));

  const data = { datasets };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: "Flowrate vs Pressure by Equipment",
          font: {size: 18}
      },
      tooltip: {
        callbacks: {
          label: (ctx) => {
            const p = ctx.raw;
            return `${p.name} | Flow: ${p.x}, Pressure: ${p.y}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: "Flowrate" },
      },
      y: {
        title: { display: true, text: "Pressure" },
      },
    },
  };

  return (
    <div style={{ height: "350px" }}>
      <Scatter data={data} options={options} />
    </div>
  );
}

export default ScatterChart;
