// Symulator Lądowania Rakiety - Frontend JavaScript

let selectedPlanet = "ksiezyc";
let planets = {};
let charts = {};

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
	loadPlanets();
	initSliders();
	initLaunchButton();
	initCharts();
});

// Load planets from API
async function loadPlanets() {
	try {
		const response = await fetch("/api/planety");
		planets = await response.json();
		renderPlanetGrid();
		updatePlanetInfo();
	} catch (error) {
		console.error("Błąd ładowania planet:", error);
	}
}

// Render planet selection grid
function renderPlanetGrid() {
	const grid = document.getElementById("planet-grid");
	grid.innerHTML = "";

	for (const [key, planet] of Object.entries(planets)) {
		const btn = document.createElement("button");
		btn.className = `planet-btn ${key === selectedPlanet ? "active" : ""}`;
		btn.innerHTML = `
            <div class="planet-name">${planet.nazwa}</div>
            <div class="planet-gravity">${planet.grawitacja.toFixed(2)} m/s²</div>
        `;
		btn.onclick = () => selectPlanet(key);
		grid.appendChild(btn);
	}
}

// Select planet
function selectPlanet(key) {
	selectedPlanet = key;
	document.querySelectorAll(".planet-btn").forEach((btn) => btn.classList.remove("active"));
	event.currentTarget.classList.add("active");
	updatePlanetInfo();
}

// Update planet info text
function updatePlanetInfo() {
	const info = document.getElementById("planet-info");
	const planet = planets[selectedPlanet];
	if (planet) {
		info.textContent = `${planet.opis} | Grawitacja: ${planet.grawitacja.toFixed(2)} m/s²`;
	}
}

// Initialize sliders
function initSliders() {
	const sliders = [
		{ id: "wysokosc", unit: "m" },
		{ id: "predkosc_y", unit: "m/s" },
		{ id: "masa_paliwa", unit: "kg" },
		{ id: "masa_rakiety", unit: "kg" },
		{ id: "moc_silnika", unit: "N" },
	];

	sliders.forEach(({ id, unit }) => {
		const slider = document.getElementById(id);
		const valueSpan = document.getElementById(`${id}-value`);

		slider.addEventListener("input", () => {
			valueSpan.textContent = `${slider.value} ${unit}`;
		});
	});
}

// Initialize launch button
function initLaunchButton() {
	const btn = document.getElementById("launch-btn");
	btn.addEventListener("click", runSimulation);
}

// Initialize charts
function initCharts() {
	const chartConfig = {
		responsive: true,
		maintainAspectRatio: true,
		plugins: {
			legend: {
				display: false,
			},
		},
		scales: {
			x: {
				grid: { color: "rgba(255,255,255,0.1)" },
				ticks: { color: "#9ca3af" },
			},
			y: {
				grid: { color: "rgba(255,255,255,0.1)" },
				ticks: { color: "#9ca3af" },
			},
		},
	};

	// Altitude chart
	charts.altitude = new Chart(document.getElementById("chart-altitude"), {
		type: "line",
		data: {
			labels: [],
			datasets: [
				{
					data: [],
					borderColor: "#10b981",
					backgroundColor: "rgba(16, 185, 129, 0.2)",
					fill: true,
					tension: 0.3,
				},
			],
		},
		options: {
			...chartConfig,
			scales: {
				...chartConfig.scales,
				x: { ...chartConfig.scales.x, title: { display: true, text: "Czas [s]", color: "#9ca3af" } },
				y: { ...chartConfig.scales.y, title: { display: true, text: "Wysokość [m]", color: "#9ca3af" }, min: 0 },
			},
		},
	});

	// Velocity chart
	charts.velocity = new Chart(document.getElementById("chart-velocity"), {
		type: "line",
		data: {
			labels: [],
			datasets: [
				{
					data: [],
					borderColor: "#f59e0b",
					backgroundColor: "rgba(245, 158, 11, 0.2)",
					fill: true,
					tension: 0.3,
				},
			],
		},
		options: {
			...chartConfig,
			scales: {
				...chartConfig.scales,
				x: { ...chartConfig.scales.x, title: { display: true, text: "Czas [s]", color: "#9ca3af" } },
				y: { ...chartConfig.scales.y, title: { display: true, text: "Prędkość [m/s]", color: "#9ca3af" } },
			},
		},
	});

	// Thrust chart
	charts.thrust = new Chart(document.getElementById("chart-thrust"), {
		type: "line",
		data: {
			labels: [],
			datasets: [
				{
					data: [],
					borderColor: "#ef4444",
					backgroundColor: "rgba(239, 68, 68, 0.2)",
					fill: true,
					tension: 0.3,
				},
			],
		},
		options: {
			...chartConfig,
			scales: {
				...chartConfig.scales,
				x: { ...chartConfig.scales.x, title: { display: true, text: "Czas [s]", color: "#9ca3af" } },
				y: { ...chartConfig.scales.y, title: { display: true, text: "Ciąg [N]", color: "#9ca3af" }, min: 0 },
			},
		},
	});

	// Fuel chart
	charts.fuel = new Chart(document.getElementById("chart-fuel"), {
		type: "line",
		data: {
			labels: [],
			datasets: [
				{
					data: [],
					borderColor: "#8b5cf6",
					backgroundColor: "rgba(139, 92, 246, 0.2)",
					fill: true,
					tension: 0.3,
				},
			],
		},
		options: {
			...chartConfig,
			scales: {
				...chartConfig.scales,
				x: { ...chartConfig.scales.x, title: { display: true, text: "Czas [s]", color: "#9ca3af" } },
				y: { ...chartConfig.scales.y, title: { display: true, text: "Paliwo [kg]", color: "#9ca3af" }, min: 0 },
			},
		},
	});
}

// Run simulation
async function runSimulation() {
	const btn = document.getElementById("launch-btn");
	const status = document.getElementById("status");

	// Disable button and show loading
	btn.disabled = true;
	btn.innerHTML = '<span class="loading"></span> Symulacja w toku...';

	status.className = "status status-running";
	status.textContent = "Symulacja w toku...";

	// Gather parameters
	const params = {
		planeta: selectedPlanet,
		wysokosc: document.getElementById("wysokosc").value,
		predkosc_y: document.getElementById("predkosc_y").value,

		masa_paliwa: document.getElementById("masa_paliwa").value,
		masa_rakiety: document.getElementById("masa_rakiety").value,
		moc_silnika: document.getElementById("moc_silnika").value,
	};

	try {
		const response = await fetch("/api/symulacja", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(params),
		});

		const result = await response.json();

		if (result.sukces) {
			status.className = "status status-success";
			status.textContent = "SUKCES! Rakieta wyladowala bezpiecznie!";
		} else {
			status.className = "status status-failure";
			let msg = "NIEPOWODZENIE: " + result.komunikat;
			if (result.porada) {
				msg += "\n\n" + result.porada;
			}
			status.textContent = msg;
			status.style.whiteSpace = "pre-wrap";
		}

		updateStats(result);
		updateCharts(result);
	} catch (error) {
		status.className = "status status-failure";
		status.textContent = "Błąd połączenia z serwerem";
		console.error("Błąd:", error);
	}

	// Re-enable button
	btn.disabled = false;
	btn.innerHTML = "Uruchom Symulację";
}

// Update statistics
function updateStats(result) {
	document.getElementById("stat-czas").textContent = result.czas_symulacji ? `${result.czas_symulacji.toFixed(1)} s` : "-";

	if (result.stan_koncowy) {
		document.getElementById("stat-predkosc").textContent = `${Math.abs(result.stan_koncowy.vy).toFixed(2)} m/s`;
		document.getElementById("stat-paliwo").textContent = `${result.stan_koncowy.masa_paliwa.toFixed(1)} kg`;

		// Oblicz zużyte paliwo
		const paliwoStart = result.parametry.masa_paliwa;
		const paliwoKoniec = result.stan_koncowy.masa_paliwa;
		const zuzycie = paliwoStart - paliwoKoniec;
		document.getElementById("stat-zuzycie").textContent = `${zuzycie.toFixed(1)} kg`;
	}
}

// Update charts with simulation data
function updateCharts(result) {
	if (!result.historia) return;

	const historia = result.historia;
	const timeLabels = historia.czas.map((t) => t.toFixed(1));

	// Zniszcz stare wykresy i utwórz nowe
	Object.values(charts).forEach((chart) => chart.destroy());
	initCharts();

	// Altitude
	charts.altitude.data.labels = timeLabels;
	charts.altitude.data.datasets[0].data = historia.y;
	charts.altitude.update();

	// Velocity
	charts.velocity.data.labels = timeLabels;
	charts.velocity.data.datasets[0].data = historia.vy;
	charts.velocity.update();

	// Thrust
	charts.thrust.data.labels = timeLabels;
	charts.thrust.data.datasets[0].data = historia.cieg;
	charts.thrust.update();

	// Fuel
	charts.fuel.data.labels = timeLabels;
	charts.fuel.data.datasets[0].data = historia.masa_paliwa;
	charts.fuel.update();
}
