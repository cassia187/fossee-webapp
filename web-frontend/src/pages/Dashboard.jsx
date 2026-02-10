import { useEffect, useState, useRef } from "react";
import API from "../services/api";
import { Bar } from "react-chartjs-2";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

import "../components/charts/chartSetup";
import PieChart from "../components/charts/PieChart";
import BarChart from "../components/charts/BarChart";
import ScatterChart from "../components/charts/ScatterChart";
import Histogram from "../components/charts/Histogram";
import EquipmentBarChart from "../components/charts/EquipmentBarChart";

function Dashboard() {
  const [datasets, setDatasets] = useState([]);
  const [selected, setSelected] = useState(null);
  const [user, setUser] = useState("");
  const [distribution, setDistribution] = useState([]);
  const [rawData, setRawData] = useState(null);
  const [selectedEquipment, setSelectedEquipment] = useState(null);

  const reportRef = useRef();
  const fileInputRef = useRef(null);


  useEffect(() => {
    fetchProfile();
    fetchDatasets();
  }, []);

  const fetchProfile = async () => {
    const res = await API.get("api/profile/");
    setUser(res.data.user.username);
  };

  const fetchDatasets = async () => {
    const res = await API.get("api/datasets/");
    setDatasets(res.data || []);
  };

  const fetchCharts = async (id) => {
    setSelected(id);
    const dist = await API.get(`api/datasets/${id}/type_distribution/`);
    const raw = await API.get(`api/datasets/${id}/raw/`);
    setDistribution(dist.data.distribution || []);
    setRawData(raw.data || null);
    setSelectedEquipment(null);
  };

  /* ---------------- HISTOGRAM ---------------- */

  const buildHistogram = (temps = [], names = []) => {
  const bins = {};

  temps.forEach((t, i) => {
    const bucketStart = Math.floor(t / 10) * 10;
    const key = `${bucketStart}-${bucketStart + 9}°C`;

    if (!bins[key]) {
      bins[key] = { count: 0, items: [] };
    }

    bins[key].count += 1;
    bins[key].items.push(names[i]);
  });

  return {
    labels: Object.keys(bins),
    counts: Object.values(bins).map(b => b.count),
    items: Object.values(bins).map(b => b.items),
  };
};


  const histogram = rawData
  ? buildHistogram(rawData.temperatures, rawData.names)
  : { labels: [], counts: [], items: [] };


  /* ---------------- EQUIPMENT ARRAYS ---------------- */

  const equipmentNames = rawData?.names || [];
  const equipmentFlows = rawData?.flowrates || [];
  const equipmentPressures = rawData?.pressures || [];
  const equipmentTemps = rawData?.temperatures || [];

  /* ---------------- TYPE AVERAGES ---------------- */

  const averagesByType = rawData?.types
    ? rawData.types.reduce((acc, type, i) => {
        if (!acc[type]) acc[type] = { f: [], p: [], t: [] };
        acc[type].f.push(rawData.flowrates[i]);
        acc[type].p.push(rawData.pressures[i]);
        acc[type].t.push(rawData.temperatures[i]);
        return acc;
      }, {})
    : {};

  const barLabels = Object.keys(averagesByType);

  const avgFlow = barLabels.map((l) => {
    const arr = averagesByType[l].f;
    return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  });

  const avgPressure = barLabels.map((l) => {
    const arr = averagesByType[l].p;
    return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  });

  const avgTemp = barLabels.map((l) => {
    const arr = averagesByType[l].t;
    return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  });

  /* ---------------- SCATTER ---------------- */

  const scatterPoints = rawData?.flowrates
    ? rawData.flowrates.map((f, i) => ({
        x: f,
        y: rawData.pressures[i],
        name: rawData.names[i],
        type: rawData.types[i],
      }))
    : [];

  /* ---------------- PDF ---------------- */

  const downloadPDF = async () => {
  const canvas = await html2canvas(reportRef.current, {
    scale: 3,
    useCORS: true,
  });

  const imgData = canvas.toDataURL("image/png");
  const pdf = new jsPDF("p", "mm", "a4");

  const pageWidth = 210;
  const pageHeight = 297;
  const imgWidth = 190;
  const imgHeight = (canvas.height * imgWidth) / canvas.width;

  let heightLeft = imgHeight;
  let position = 10;

  pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
  heightLeft -= pageHeight;

  while (heightLeft > 0) {
    position = heightLeft - imgHeight;
    pdf.addPage();
    pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
    heightLeft -= pageHeight;
  }

  pdf.save("equipment_report.pdf");
};


  const handleFileChange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    await API.post("api/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    alert("Upload successful");
    fetchDatasets();   // refresh list
  } catch (err) {
    console.error(err);
    alert("Upload failed");
  }
};

  const handleLogout = async () => {
  try {
    await API.post("api/logout/");
  } catch (e) {
    console.warn("Logout API failed, clearing anyway");
  }

  localStorage.removeItem("token");
  window.location.href = "/";
};


  return (
    <div className="dashboard">
      <div className="topbar">
        <span>Welcome, {user}</span>
          <button
    className="btn"
    onClick={handleLogout}
  >
    Logout
  </button>
      </div>

      <div className="body">
        {/* ---------- SIDEBAR ---------- */}
        <div className="sidebar">

  <button
    className="btn"
    onClick={() => fileInputRef.current.click()}
  >
    Upload
  </button>
            <input
  type="file"
  ref={fileInputRef}
  style={{ display: "none" }}
  onChange={handleFileChange}
/>
  <button
    className="btn"
    onClick={async () => {
      if (!selected) return alert("Select dataset first");
      await API.delete(`api/datasets/${selected}/delete/`);
      setRawData(null);
      fetchDatasets();
    }}
  >
    Delete
  </button>

  <input
    type="file"
    hidden
    ref={fileInputRef}
    onChange={handleFileChange}
  />

  <div className="dataset-list">
    {datasets.map((d) => (
      <div
        key={d.id}
        className={selected === d.id ? "active" : ""}
        onClick={() => fetchCharts(d.id)}
      >
        {d.filename}
      </div>
    ))}
  </div>

</div>


        {/* ---------- MAIN ---------- */}
        <div className="main">
          <button className="download-btn" onClick={downloadPDF}>
            Download PDF
          </button>

          {rawData && (
            <div className="chart-grid">
              <div className="chart-box">
                <div className="chart-title">
                  Equipment Type Distribution
                </div>
                <PieChart data={distribution} />
              </div>

              <div className="chart-box">
                <div className="chart-title">Average Metrics by Type</div>
                <BarChart
                  labels={barLabels}
                  flow={avgFlow}
                  pressure={avgPressure}
                  temp={avgTemp}
                />
              </div>

              <div className="chart-box">
                <div className="chart-title">Flow vs Pressure</div>
                <ScatterChart points={scatterPoints} />
              </div>

              <div className="chart-box">
                <div className="chart-title">Temperature Distribution</div>
                <Histogram
                  bins={histogram.labels}
                  counts={histogram.counts}
                  items={histogram.items}
                />
              </div>

              <div className="chart-box">
                <div className="chart-title">All Equipment Comparison</div>
                <EquipmentBarChart
                  names={equipmentNames}
                  flows={equipmentFlows}
                  pressures={equipmentPressures}
                  temps={equipmentTemps}
                />
              </div>

              {selectedEquipment !== null && (
                <div className="equipment-card">
                  <div className="chart-title">
                    {rawData.names[selectedEquipment]}
                  </div>
                  <Bar
                    data={{
                      labels: ["Flow", "Pressure", "Temp"],
                      datasets: [
                        {
                          label: rawData.names[selectedEquipment],
                          data: [
                            rawData.flowrates[selectedEquipment],
                            rawData.pressures[selectedEquipment],
                            rawData.temperatures[selectedEquipment],
                          ],
                          backgroundColor: [
                            "#4e73df",
                            "#e74a3b",
                            "#f6c23e",
                          ],
                        },
                      ],
                    }}
                    options={{ responsive: true }}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
        {/* ---------- HIDDEN PDF REPORT ---------- */}
<div
  ref={reportRef}
  style={{
    position: "absolute",
    left: "-9999px",
    top: 0,
    width: "1000px",
    background: "white",
    padding: "30px",
  }}
>
  <h1>Equipment Analytics Report</h1>
  <p>User: {user}</p>
  <p>Date: {new Date().toLocaleString()}</p>

  {rawData && (
    <>
      <h2>Summary Statistics</h2>

      <p>Total Equipment: {equipmentNames.length}</p>

      <p>
        Average Flow:{" "}
        {(
          equipmentFlows.reduce((a, b) => a + b, 0) /
          (equipmentFlows.length || 1)
        ).toFixed(2)}
      </p>

      <p>
        Average Pressure:{" "}
        {(
          equipmentPressures.reduce((a, b) => a + b, 0) /
          (equipmentPressures.length || 1)
        ).toFixed(2)}
      </p>

      <p>
        Average Temperature:{" "}
        {(
          equipmentTemps.reduce((a, b) => a + b, 0) /
          (equipmentTemps.length || 1)
        ).toFixed(2)}
      </p>

      <h2>Charts</h2>

      <div style={{ height: 300 }}>
        <PieChart data={distribution} />
      </div>

      <div style={{ height: 300 }}>
        <BarChart
          labels={barLabels}
          flow={avgFlow}
          pressure={avgPressure}
          temp={avgTemp}
        />
      </div>

      <div style={{ height: 300 }}>
        <ScatterChart points={scatterPoints} />
      </div>

      <div style={{ height: 300 }}>
        <Histogram
          bins={histogram.labels}
          counts={histogram.counts}
        />
      </div>
    </>
  )}
</div>

    </div>
  );
}

export default Dashboard;
