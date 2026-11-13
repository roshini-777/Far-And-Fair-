let activeLeafletMap = null;

function renderStayMap(stay) {
  const mapContainer = document.getElementById("stayMap");
  if (!mapContainer || typeof L === "undefined") return;

  if (activeLeafletMap) {
    activeLeafletMap.remove();
    activeLeafletMap = null;
  }

  activeLeafletMap = L.map("stayMap").setView([stay.lat, stay.lng], 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(activeLeafletMap);

  // Main Accommodation Marker (Red)
  const stayIcon = L.divIcon({
    className: "custom-pin",
    html: '<div style="background:#dc2626;color:#fff;padding:4px 8px;border-radius:8px;font-weight:700;font-size:11px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.3);">🏠 Stay</div>',
    iconSize: [60, 26],
    iconAnchor: [30, 13]
  });

  L.marker([stay.lat, stay.lng], { icon: stayIcon })
    .addTo(activeLeafletMap)
    .bindPopup(`<strong>${stay.name}</strong><br>${stay.address}`)
    .openPopup();

  // Nearby Sightseeing & Attractions Markers (Blue)
  const bounds = [[stay.lat, stay.lng]];
  (stay.attractions || []).forEach((spot) => {
    const spotIcon = L.divIcon({
      className: "custom-pin",
      html: '<div style="background:#1e40af;color:#fff;padding:3px 7px;border-radius:8px;font-weight:600;font-size:10px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.25);">📍 Spot</div>',
      iconSize: [55, 22],
      iconAnchor: [27, 11]
    });

    L.marker([spot.lat, spot.lng], { icon: spotIcon })
      .addTo(activeLeafletMap)
      .bindPopup(`<strong>${spot.name}</strong><br>Distance: ${spot.distance}`);

    bounds.push([spot.lat, spot.lng]);
  });

  if (bounds.length > 1) {
    activeLeafletMap.fitBounds(bounds, { padding: [35, 35] });
  }

  setTimeout(() => {
    activeLeafletMap.invalidateSize();
  }, 150);
}
