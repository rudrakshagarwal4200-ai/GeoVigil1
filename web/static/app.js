let currentActiveProjectId = null;

document.addEventListener("DOMContentLoaded", () => {
  fetchStatus();
  fetchCouncil();
  fetchLogs();
  fetchMemory();
  setInterval(fetchStatus, 4000);
  setInterval(fetchLogs, 5000);
  setInterval(fetchMemory, 6000);
});

async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    document.getElementById("activeModelLabel").innerText = `Model: ${data.active_model}`;
    document.getElementById("statAgentsSpawned").innerText = data.total_agents_spawned;
    document.getElementById("statProjectsCompleted").innerText = data.total_projects_completed;
    document.getElementById("statCouncilSeats").innerText = `${data.council_seats_count} Seats`;
  } catch (err) {
    console.error("Error fetching status:", err);
  }
}

async function fetchCouncil() {
  try {
    const res = await fetch("/api/council");
    const data = await res.json();
    const container = document.getElementById("councilSeatsContainer");
    container.innerHTML = "";
    data.seats.forEach(s => {
      const card = document.createElement("div");
      card.className = `council-seat-card ${s.is_senior_leader ? "leader" : ""}`;
      card.innerHTML = `
        <div class="seat-name">${s.member_name} ${s.is_senior_leader ? "👑" : ""}</div>
        <div class="seat-role">${s.specialty}</div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error("Error fetching council seats:", err);
  }
}

async function submitObjective() {
  const prompt = document.getElementById("promptInput").value.trim();
  if (!prompt) {
    alert("Please provide an objective prompt.");
    return;
  }
  const explicitCountVal = document.getElementById("explicitCountInput").value;
  const explicitCount = explicitCountVal ? parseInt(explicitCountVal) : null;
  const isNovel = document.getElementById("noveltyCheck").checked;

  const btn = document.getElementById("btnSubmitObjective");
  btn.innerText = "Dispatching through CEO & Council...";
  btn.disabled = true;

  try {
    const res = await fetch("/api/objectives", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt: prompt,
        explicit_agent_count: explicitCount,
        force_new_capability: isNovel
      })
    });
    const data = await res.json();
    currentActiveProjectId = data.project_id;

    // Render Project Details
    document.getElementById("projectStatusBadge").innerText = data.status;
    document.getElementById("projectStatusBadge").className = "badge badge-gold";
    document.getElementById("projectDetails").innerHTML = `
      <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 6px;">
        <p><strong>Project:</strong> ${data.project_name} (<code>${data.project_id}</code>)</p>
        <p><strong>CEO Synthesized Intent:</strong> ${data.ceo_intent}</p>
        <p><strong>Council Consensus:</strong> ${data.council_consensus} (Deadlock Breaker: ${data.senior_leader_ruled ? "YES" : "NO"})</p>
        <p><strong>DOOM Workforce:</strong> ${data.staffing.total_agents} agents (${data.staffing.orchestrators} Orchestrators, ${data.staffing.reviewers} Reviewers, ${data.staffing.managers} Managers, ${data.staffing.workers} Workers)</p>
        <p><strong>Tri-Orchestrator Certification:</strong> ${data.tri_orchestrator_certified ? "VERIFIED & SIGNED OFF" : "PENDING"}</p>
        <p style="margin-top: 8px; color: #38bdf8;"><strong>Awaiting Human Verdict:</strong> Review deliverables and click Accept or Reject below.</p>
      </div>
    `;
    document.getElementById("reviewActions").classList.remove("hidden");
    fetchStatus();
    fetchLogs();
  } catch (err) {
    alert("Failed to submit objective: " + err.message);
  } finally {
    btn.innerText = "Dispatch Objective to CEO";
    btn.disabled = false;
  }
}

async function reviewProject(accept) {
  if (!currentActiveProjectId) return;
  const feedback = accept ? "" : prompt("Enter revision instructions for the project team:");
  if (!accept && feedback === null) return; // User cancelled prompt

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_id: currentActiveProjectId,
        accept: accept,
        feedback: feedback || ""
      })
    });
    const data = await res.json();
    alert(data.message);

    if (accept) {
      document.getElementById("projectStatusBadge").innerText = "DISSOLVED (KNOWLEDGE SAVED)";
      document.getElementById("projectStatusBadge").className = "badge badge-blue";
      document.getElementById("reviewActions").classList.add("hidden");
      currentActiveProjectId = null;
    } else {
      document.getElementById("projectStatusBadge").innerText = `REVISION ROUND ${data.revision_count}`;
    }
    fetchStatus();
    fetchLogs();
    fetchMemory();
  } catch (err) {
    alert("Review action failed: " + err.message);
  }
}

async function fetchLogs() {
  try {
    const res = await fetch("/api/logs");
    const data = await res.json();
    const container = document.getElementById("reviewerLogs");
    if (data.length === 0) return;
    container.innerHTML = "";
    data.forEach(log => {
      const div = document.createElement("div");
      let cls = "log-info";
      if (log.severity === "MINOR_WARN") cls = "log-warn";
      if (log.severity === "SERIOUS_HALT") cls = "log-halt";
      div.className = `log-entry ${cls}`;
      div.innerHTML = `[${log.severity}] ${log.details} ${log.rollback_executed ? "<b>[ROLLED BACK TO " + log.rollback_milestone + "]</b>" : ""}`;
      container.appendChild(div);
    });
  } catch (err) {
    console.error("Error fetching reviewer logs:", err);
  }
}

async function fetchMemory() {
  try {
    const res = await fetch("/api/memory");
    const data = await res.json();
    const container = document.getElementById("memoryContainer");
    if (data.length === 0) return;
    container.innerHTML = "";
    data.forEach(m => {
      const div = document.createElement("div");
      div.style.marginBottom = "10px";
      div.style.padding = "8px";
      div.style.background = "rgba(255,255,255,0.02)";
      div.style.borderRadius = "4px";
      div.innerHTML = `
        <div style="color: #d4af37; font-weight: bold;">Project: ${m.project_id}</div>
        <div><strong>Objective:</strong> ${m.objective_summary}</div>
        <div style="font-size: 0.75rem; color: #8b9bb4;"><strong>Decisions:</strong> ${m.decisions}</div>
      `;
      container.appendChild(div);
    });
  } catch (err) {
    console.error("Error fetching memory:", err);
  }
}

function openModelModal() {
  document.getElementById("modelModal").classList.remove("hidden");
}

function closeModelModal() {
  document.getElementById("modelModal").classList.add("hidden");
}

async function confirmModelSwitch() {
  const modelName = document.getElementById("modelSelect").value;
  try {
    const res = await fetch("/api/model", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_name: modelName })
    });
    const data = await res.json();
    alert(data.message);
    closeModelModal();
    fetchStatus();
  } catch (err) {
    alert("Failed to switch model: " + err.message);
  }
}
