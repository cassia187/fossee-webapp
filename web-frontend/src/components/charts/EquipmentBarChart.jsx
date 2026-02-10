import { Bar } from "react-chartjs-2";

function EquipmentBarChart({
  names = [],
  flows = [],
  pressures = [],
  temps = [],
}) {
  const data = {
    labels: names,
    datasets: [
      { label: "Flow", data: flows, backgroundColor: "#3498db" },
      { label: "Pressure", data: pressures, backgroundColor: "#e74c3c" },
      { label: "Temp", data: temps, backgroundColor: "#f1c40f" },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Equipment-wise Performance",
          font: {size: 18}
      },
    },
    scales: {
      x: { title: { display: true, text: "Equipment Name" } },
      y: { title: { display: true, text: "Value" } },
    },
  };

  return (
    <div style={{ height: "350px" }}>
      <Bar data={data} options={options} />
    </div>
  );
}

export default EquipmentBarChart;
