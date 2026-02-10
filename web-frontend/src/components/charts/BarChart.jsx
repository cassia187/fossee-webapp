import { Bar } from "react-chartjs-2";

function BarChart({ labels = [], flow = [], pressure = [], temp = [] }) {
  const data = {
    labels,
    datasets: [
      {
        label: "Flowrate",
        data: flow,
        backgroundColor: "#4e73df",
      },
      {
        label: "Pressure",
        data: pressure,
        backgroundColor: "#e74a3b",
      },
      {
        label: "Temperature",
        data: temp,
        backgroundColor: "#f6c23e",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Average Flow / Pressure / Temperature by Equipment Type",
          font: { size: 18}
      },
      legend: { position: "top" },
    },
    scales: {
      x: {
        title: { display: true, text: "Equipment Type" },
      },
      y: {
        title: { display: true, text: "Average Value" },
      },
    },
  };

  return (
    <div style={{ height: "350px" }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default BarChart;
