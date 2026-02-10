import { Bar } from "react-chartjs-2";

function Histogram({ bins = [], counts = [], items = [] }) {
  const data = {
    labels: bins,
    datasets: [
      {
        label: "Frequency",
        data: counts,
        backgroundColor: "#8e44ad",
        borderRadius: 6,
      },
    ],
  };

  const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: "Temperature Frequency Distribution",
      font: { size: 18 },
    },
    tooltip: {
      callbacks: {
        // first line
        label: (ctx) => `Count: ${ctx.raw}`,

        // second line (equipment names)
        afterLabel: (ctx) => {
          const idx = ctx.dataIndex;
          const names = items?.[idx] || [];
          if (!names.length) return "Equipment: None";
          return `Equipment: ${names.join(", ")}`;
        },
      },
    },
    legend: {
      display: true,
      position: "top",
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "Temperature Range (°C)",
      },
    },
    y: {
      title: {
        display: true,
        text: "Frequency",
      },
      beginAtZero: true,
      ticks: {
        precision: 0, // no decimals
      },
    },
  },
};


  return (
    <div style={{ height: "300px", width: "100%" }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default Histogram;
