const API_BASE = "http://127.0.0.1:5000";

let allFilteredStays = [];
let selectedStayId = null;
let shortlistedIds = [];

// Offline fallback dataset in case index.html is opened directly without running Flask
const FALLBACK_STAYS = [
  {
    id: 1,
    name: "Scholar's Haven Co-Living PG",
    type: "PG",
    city: "Bengaluru",
    address: "14th Main, Koramangala 4th Block, Bengaluru",
    daily_cost: 650,
    deposit: 5000,
    rating: 4.7,
    reviews_count: 142,
    max_persons: 2,
    food_included: true,
    wifi: true,
    gym: true,
    laundry: true,
    security: true,
    study_room: true,
    lat: 12.9352,
    lng: 77.6245,
    images: [
      "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
      "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
      "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800"
    ],
    description: "Student & intern PG with dedicated study room, high-speed Wi-Fi, and homestyle meals.",
    reviews: [{ user: "Ananya R.", rating: 5, comment: "Zero hidden charges and instant deposit refund." }],
    attractions: [
      { name: "Cubbon Park", distance: "5.2 km", lat: 12.9763, lng: 77.5929 },
      { name: "Forum Nexus Mall", distance: "1.1 km", lat: 12.9345, lng: 77.6113 }
    ]
  },
  {
    id: 2,
    name: "Backpackers Nest Social Hostel",
    type: "Hostel",
    city: "Bengaluru",
    address: "22 Church Street, Ashok Nagar, Bengaluru",
    daily_cost: 520,
    deposit: 1000,
    rating: 4.6,
    reviews_count: 218,
    max_persons: 4,
    food_included: false,
    wifi: true,
    gym: false,
    laundry: true,
    security: true,
    study_room: true,
    lat: 12.9749,
    lng: 77.6074,
    images: [
      "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800",
      "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800",
      "https://images.unsplash.com/photo-1520277739336-7bf67edfa768?w=800"
    ],
    description: "Social hostel right on Church Street with coworking lounge and locker beds.",
    reviews: [{ user: "Rohan S.", rating: 4.7, comment: "2 mins from metro and very low deposit!" }],
    attractions: [
      { name: "MG Road Metro", distance: "0.3 km", lat: 12.9756, lng: 77.6066 },
      { name: "Cubbon Park", distance: "1.2 km", lat: 12.9763, lng: 77.5929 }
    ]
  }
];

function formatINR(num) {
  return "₹" + Number(num || 0).toLocaleString("en-IN");
}

function getFilterState() {
  const activeTypeBtn = document.querySelector("#typePills .pill.active");
  return {
    destination: document.getElementById("destinationInput").value.trim(),
    checkin: document.getElementById("checkinInput").value,
    duration: Math.max(1, parseInt(document.getElementById("durationInput").value, 10) || 7),
    budget: Math.max(500, parseInt(document.getElementById("budgetInput").value, 10) || 15000),
    type: activeTypeBtn ? activeTypeBtn.dataset.type : "All",
    max_price: parseInt(document.getElementById("maxPriceRange").value, 10),
    max_persons: document.getElementById("sharingSelect").value,
    food_included: document.getElementById("filterFood").checked,
    wifi: document.getElementById("filterWifi").checked,
    gym: document.getElementById("filterGym").checked,
    laundry: document.getElementById("filterLaundry").checked,
    security: document.getElementById("filterSecurity").checked,
    study_room: document.getElementById("filterStudy").checked
  };
}

function computeBudgetClient(stay, duration, userBudget) {
  const accommodation_total = stay.daily_cost * duration;
  const food_total = (stay.food_included ? 120 : 350) * duration;
  const transport_total = 150 * duration;
  const actual_expense = accommodation_total + food_total + transport_total;
  const refundable_deposit = stay.deposit;
  const upfront_amount = actual_expense + refundable_deposit;
  return {
    duration_days: duration,
    accommodation_total,
    food_total,
    transport_total,
    actual_expense,
    refundable_deposit,
    upfront_amount,
    within_budget: upfront_amount <= userBudget,
    difference: userBudget - upfront_amount
  };
}

async function fetchAndRenderStays() {
  const state = getFilterState();
  const params = new URLSearchParams({
    destination: state.destination,
    type: state.type,
    max_price: state.max_price,
    max_persons: state.max_persons,
    food_included: state.food_included,
    wifi: state.wifi,
    gym: state.gym,
    laundry: state.laundry,
    security: state.security,
    study_room: state.study_room,
    duration: state.duration,
    budget: state.budget
  });

  try {
    const res = await fetch(`${API_BASE}/api/stays?${params.toString()}`);
    if (!res.ok) throw new Error("Backend unavailable");
    const data = await res.json();
    allFilteredStays = data.stays;
  } catch (err) {
    // Graceful client-side filtering fallback if opened directly as file://
    allFilteredStays = FALLBACK_STAYS.filter((s) => {
      if (state.destination && !s.city.toLowerCase().includes(state.destination.toLowerCase())) return false;
      if (state.type !== "All" && s.type !== state.type) return false;
      if (s.daily_cost > state.max_price) return false;
      return true;
    }).map((s) => ({
      ...s,
      budget_breakdown: computeBudgetClient(s, state.duration, state.budget)
    }));
  }

  if (!allFilteredStays.some((s) => s.id === selectedStayId)) {
    selectedStayId = allFilteredStays.length ? allFilteredStays[0].id : null;
  }

  renderCards();
  updateBudgetDashboard();
  renderComparison();
}

function updateBudgetDashboard() {
  const state = getFilterState();
  const stay = allFilteredStays.find((s) => s.id === selectedStayId);

  if (!stay) {
    document.getElementById("selectedStayTitle").textContent = "No Matching Stays";
    document.getElementById("selectedStayMeta").textContent = "Try widening your filters or budget.";
    ["dashRent", "dashFood", "dashTransport", "dashActual", "dashDeposit", "dashUpfront"].forEach((id) => {
      document.getElementById(id).textContent = "₹0";
    });
    return;
  }

  const b = stay.budget_breakdown || computeBudgetClient(stay, state.duration, state.budget);

  document.getElementById("selectedStayTitle").textContent = stay.name;
  document.getElementById("selectedStayMeta").textContent = `${stay.type} • ${stay.city} • Max ${stay.max_persons} person(s)/room`;
  document.getElementById("dashDays").textContent = b.duration_days;
  document.getElementById("dashRent").textContent = formatINR(b.accommodation_total);
  document.getElementById("dashFood").textContent = formatINR(b.food_total);
  document.getElementById("dashTransport").textContent = formatINR(b.transport_total);
  document.getElementById("dashActual").textContent = formatINR(b.actual_expense);
  document.getElementById("dashDeposit").textContent = formatINR(b.refundable_deposit);
  document.getElementById("dashUpfront").textContent = formatINR(b.upfront_amount);

  const upfrontBox = document.getElementById("upfrontBox");
  const statusEl = document.getElementById("budgetStatusText");

  if (b.within_budget) {
    upfrontBox.classList.remove("over-budget");
    statusEl.textContent = `✅ Fits your ${formatINR(state.budget)} budget! You keep ${formatINR(b.difference)} spare upfront (plus ${formatINR(b.refundable_deposit)} back at checkout).`;
  } else {
    upfrontBox.classList.add("over-budget");
    statusEl.textContent = `⚠️ Exceeds ${formatINR(state.budget)} upfront budget by ${formatINR(Math.abs(b.difference))} (includes ${formatINR(b.refundable_deposit)} refundable deposit).`;
  }
}

function renderCards() {
  const grid = document.getElementById("cardsGrid");
  document.getElementById("resultsHeading").textContent = `Available Stays (${allFilteredStays.length})`;

  if (!allFilteredStays.length) {
    grid.innerHTML = `<div class="comparison-empty" style="grid-column:1/-1;">No stays match your exact filters. Click <strong>Reset All</strong> to view all properties.</div>`;
    return;
  }

  grid.innerHTML = allFilteredStays
    .map((stay) => {
      const isSelected = stay.id === selectedStayId;
      const isCompared = shortlistedIds.includes(stay.id);

      return `
      <article class="stay-card ${isSelected ? "active-preview" : ""}" data-id="${stay.id}">
        <div class="card-img-wrap">
          <img src="${stay.images[0]}" alt="${stay.name}" loading="lazy" />
          <span class="type-badge">${stay.type}</span>
          <span class="rating-badge">⭐ ${stay.rating} (${stay.reviews_count})</span>
        </div>
        <div class="card-body">
          <h3 class="card-title">${stay.name}</h3>
          <p class="card-loc">📍 ${stay.city} • Max ${stay.max_persons} sharing</p>
          <div class="card-tags">
            <span class="mini-tag">${stay.food_included ? "🍽️ Food Included" : "🍳 Self-Dining"}</span>
            ${stay.wifi ? '<span class="mini-tag">📶 Wi-Fi</span>' : ""}
            ${stay.study_room ? '<span class="mini-tag">📚 Study Room</span>' : ""}
            ${stay.security ? '<span class="mini-tag">🛡️ 24/7 Security</span>' : ""}
          </div>
          <div class="card-pricing">
            <div class="daily-price">
              <strong>${formatINR(stay.daily_cost)}</strong><span>/day</span>
            </div>
            <span class="deposit-pill">Deposit: ${formatINR(stay.deposit)}</span>
          </div>
          <div class="card-actions">
            <button type="button" class="card-btn preview-btn ${isSelected ? "selected" : ""}" data-id="${stay.id}">
              ${isSelected ? "✓ In Budget Box" : "Calculate Budget"}
            </button>
            <button type="button" class="card-btn compare-btn ${isCompared ? "selected" : ""}" data-id="${stay.id}">
              ${isCompared ? "✓ Shortlisted" : "+ Compare"}
            </button>
          </div>
        </div>
      </article>
    `;
    })
    .join("");
}

function renderComparison() {
  document.getElementById("compareCount").textContent = shortlistedIds.length;
  const container = document.getElementById("comparisonContainer");
  const state = getFilterState();

  const items = allFilteredStays.filter((s) => shortlistedIds.includes(s.id));
  if (!items.length) {
    container.className = "comparison-empty";
    container.innerHTML = `No stays shortlisted yet. Click <strong>"+ Compare"</strong> on 2 or 3 accommodation cards above.`;
    return;
  }

  container.className = "";
  const rows = [
    { label: "Stay Type & City", fn: (s) => `${s.type} — ${s.city}` },
    { label: "Daily Rent", fn: (s) => `<strong>${formatINR(s.daily_cost)}/day</strong>` },
    { label: `Actual Spending (${state.duration}d)`, fn: (s) => formatINR((s.budget_breakdown || computeBudgetClient(s, state.duration, state.budget)).actual_expense) },
    { label: "Refundable Deposit", fn: (s) => formatINR(s.deposit) },
    { label: "Total Upfront Cash", fn: (s) => `<strong>${formatINR((s.budget_breakdown || computeBudgetClient(s, state.duration, state.budget)).upfront_amount)}</strong>` },
    { label: "Max Occupancy", fn: (s) => `${s.max_persons} Person(s) / room` },
    { label: "Food Facility", fn: (s) => (s.food_included ? "✅ Meals Included" : "❌ Not Included") },
    { label: "Amenities", fn: (s) => [s.wifi && "Wi-Fi", s.gym && "Gym", s.laundry && "Laundry", s.security && "24/7 Security", s.study_room && "Study Room"].filter(Boolean).join(", ") },
    { label: "Rating", fn: (s) => `⭐ ${s.rating} (${s.reviews_count} reviews)` }
  ];

  container.innerHTML = `
    <div style="overflow-x:auto;">
      <table class="compare-table">
        <thead>
          <tr>
            <th>Feature</th>
            ${items.map((s) => `<th>${s.name}</th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (r) => `
            <tr>
              <th>${r.label}</th>
              ${items.map((s) => `<td>${r.fn(s)}</td>`).join("")}
            </tr>
          `
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function openStayModal(stay) {
  const state = getFilterState();
  const b = stay.budget_breakdown || computeBudgetClient(stay, state.duration, state.budget);

  const modalBody = document.getElementById("modalBody");
  modalBody.innerHTML = `
    <span class="budget-tag">${stay.type} • ⭐ ${stay.rating} (${stay.reviews_count} Reviews)</span>
    <h2>${stay.name}</h2>
    <p style="color:var(--muted);margin-top:4px;">📍 ${stay.address}</p>

    <div class="gallery-grid">
      <img src="${stay.images[0]}" alt="${stay.name}" />
      <div class="gallery-side">
        <img src="${stay.images[1] || stay.images[0]}" alt="${stay.name}" />
        <img src="${stay.images[2] || stay.images[0]}" alt="${stay.name}" />
      </div>
    </div>

    <div class="detail-grid">
      <div>
        <h3>About This Stay</h3>
        <p style="margin:8px 0 14px;color:#334155;">${stay.description}</p>

        <h4>Room &amp; Deposit Policy</h4>
        <ul class="attractions-list">
          <li><span>Daily Rent</span><strong>${formatINR(stay.daily_cost)} / day</strong></li>
          <li><span>Max Persons Per Room</span><strong>${stay.max_persons} Person(s)</strong></li>
          <li><span>Refundable Security Deposit</span><strong>${formatINR(stay.deposit)} (100% Refundable)</strong></li>
          <li><span>Upfront Cash for ${state.duration} Days</span><strong>${formatINR(b.upfront_amount)}</strong></li>
        </ul>

        <h4 style="margin-top:16px;">Included Amenities</h4>
        <div class="card-tags" style="margin-top:8px;">
          <span class="mini-tag">${stay.food_included ? "✅ Food Included" : "❌ Self-Dining"}</span>
          <span class="mini-tag">${stay.wifi ? "✅ Wi-Fi" : "❌ No Wi-Fi"}</span>
          <span class="mini-tag">${stay.gym ? "✅ Gym" : "❌ No Gym"}</span>
          <span class="mini-tag">${stay.laundry ? "✅ Laundry" : "❌ No Laundry"}</span>
          <span class="mini-tag">${stay.security ? "✅ 24/7 Security" : "❌ Basic Security"}</span>
          <span class="mini-tag">${stay.study_room ? "✅ Study Room" : "❌ No Study Room"}</span>
        </div>

        <h4 style="margin-top:16px;">Verified Guest Reviews</h4>
        ${(stay.reviews || [])
          .map(
            (rev) => `
          <div class="review-item">
            <strong>${rev.user}</strong> • ⭐ ${rev.rating}<br/>
            <span>${rev.comment}</span>
          </div>
        `
          )
          .join("")}
      </div>

      <div>
        <h3>Location &amp; Nearby Attractions</h3>
        <p style="font-size:0.8rem;color:var(--muted);">Red pin: Accommodation • Blue pins: Sightseeing &amp; transit spots</p>
        <div id="stayMap"></div>
        <ul class="attractions-list">
          ${(stay.attractions || [])
            .map(
              (spot) => `
            <li><span>📍 ${spot.name}</span><strong>${spot.distance}</strong></li>
          `
            )
            .join("")}
        </ul>
      </div>
    </div>
  `;

  document.getElementById("detailModal").classList.remove("hidden");
  renderStayMap(stay);
}

// EVENT LISTENERS
document.addEventListener("DOMContentLoaded", () => {
  const tomorrow = new Date(Date.now() + 86400000).toISOString().split("T")[0];
  document.getElementById("checkinInput").value = tomorrow;

  document.getElementById("searchForm").addEventListener("submit", (e) => {
    e.preventDefault();
    fetchAndRenderStays();
  });

  ["durationInput", "budgetInput"].forEach((id) => {
    document.getElementById(id).addEventListener("input", fetchAndRenderStays);
  });

  document.querySelectorAll("#typePills .pill").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#typePills .pill").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      fetchAndRenderStays();
    });
  });

  const priceRange = document.getElementById("maxPriceRange");
  priceRange.addEventListener("input", () => {
    document.getElementById("maxPriceLabel").textContent = formatINR(priceRange.value);
    fetchAndRenderStays();
  });

  document.getElementById("sharingSelect").addEventListener("change", fetchAndRenderStays);

  ["filterFood", "filterWifi", "filterGym", "filterLaundry", "filterSecurity", "filterStudy"].forEach((id) => {
    document.getElementById(id).addEventListener("change", fetchAndRenderStays);
  });

  document.getElementById("resetFiltersBtn").addEventListener("click", () => {
    document.getElementById("destinationInput").value = "";
    document.querySelectorAll("#typePills .pill").forEach((b) => b.classList.remove("active"));
    document.querySelector('#typePills .pill[data-type="All"]').classList.add("active");
    priceRange.value = 2500;
    document.getElementById("maxPriceLabel").textContent = "₹2,500";
    document.getElementById("sharingSelect").value = "";
    ["filterFood", "filterWifi", "filterGym", "filterLaundry", "filterSecurity", "filterStudy"].forEach((id) => {
      document.getElementById(id).checked = false;
    });
    fetchAndRenderStays();
  });

  document.getElementById("cardsGrid").addEventListener("click", (e) => {
    const previewBtn = e.target.closest(".preview-btn");
    if (previewBtn) {
      e.stopPropagation();
      selectedStayId = parseInt(previewBtn.dataset.id, 10);
      renderCards();
      updateBudgetDashboard();
      return;
    }

    const compareBtn = e.target.closest(".compare-btn");
    if (compareBtn) {
      e.stopPropagation();
      const id = parseInt(compareBtn.dataset.id, 10);
      if (shortlistedIds.includes(id)) {
        shortlistedIds = shortlistedIds.filter((x) => x !== id);
      } else if (shortlistedIds.length < 3) {
        shortlistedIds.push(id);
      } else {
        alert("You can compare up to 3 stays at a time.");
      }
      renderCards();
      renderComparison();
      return;
    }

    const card = e.target.closest(".stay-card");
    if (card) {
      const id = parseInt(card.dataset.id, 10);
      selectedStayId = id;
      renderCards();
      updateBudgetDashboard();
      const stay = allFilteredStays.find((s) => s.id === id);
      if (stay) openStayModal(stay);
    }
  });

  document.getElementById("closeModalBtn").addEventListener("click", () => {
    document.getElementById("detailModal").classList.add("hidden");
  });

  document.getElementById("detailModal").addEventListener("click", (e) => {
    if (e.target.id === "detailModal") {
      document.getElementById("detailModal").classList.add("hidden");
    }
  });

  document.getElementById("scrollCompareBtn").addEventListener("click", () => {
    document.getElementById("comparisonSection").scrollIntoView({ behavior: "smooth" });
  });

  document.getElementById("clearCompareBtn").addEventListener("click", () => {
    shortlistedIds = [];
    renderCards();
    renderComparison();
  });

  fetchAndRenderStays();
});
