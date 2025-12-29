const API_BASE = "http://localhost:5000"; // change later
const DEMO_MODE = true; // set false when backend is ready

// ---------- helpers ----------
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);
const fmtMoney = (n) => (n == null || n === "" ? "—" : `$${Number(n).toFixed(2)}`);
const fmtDate = (d) => new Date(d + "T00:00:00").toLocaleDateString();

function toast(msg, type="info"){
  const el = document.createElement("div");
  el.className = "notice";
  el.style.position = "fixed";
  el.style.right = "18px";
  el.style.bottom = "18px";
  el.style.maxWidth = "420px";
  el.style.zIndex = "9999";
  el.style.borderColor = type==="bad" ? "rgba(255,79,109,.35)" : "rgba(79,140,255,.25)";
  el.style.background = type==="bad" ? "rgba(255,79,109,.12)" : "rgba(79,140,255,.10)";
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(()=> el.remove(), 2600);
}

// ---------- demo storage ----------
const demo = {
  getUser(){ return JSON.parse(localStorage.getItem("demo_user") || "null"); },
  setUser(u){ localStorage.setItem("demo_user", JSON.stringify(u)); },
  logout(){ localStorage.removeItem("demo_user"); },

  getVehicles(){
    return JSON.parse(localStorage.getItem("demo_vehicles") || "[]");
  },
  setVehicles(v){ localStorage.setItem("demo_vehicles", JSON.stringify(v)); },

  getServiceTypes(){
    const k = "demo_service_types";
    let t = JSON.parse(localStorage.getItem(k) || "null");
    if(!t){
      t = [
        {service_type_id: 1, service_type_name:"Oil Change", service_type_default_interval_miles: 5000, service_type_default_interval_days: 180},
        {service_type_id: 2, service_type_name:"Tire Rotation", service_type_default_interval_miles: 6000, service_type_default_interval_days: 365},
        {service_type_id: 3, service_type_name:"Brake Inspection", service_type_default_interval_miles: 12000, service_type_default_interval_days: 365},
      ];
      localStorage.setItem(k, JSON.stringify(t));
    }
    return t;
  },

  getRecords(){
    return JSON.parse(localStorage.getItem("demo_records") || "[]");
  },
  setRecords(r){ localStorage.setItem("demo_records", JSON.stringify(r)); }
};

// ---------- auth (demo + api) ----------
async function apiLogin(email, password){
  if(DEMO_MODE){
    const u = { user_id: 1, user_email: email, user_name: email.split("@")[0] };
    demo.setUser(u);
    return u;
  }
  const res = await fetch(`${API_BASE}/auth/login`, {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ user_email: email, user_password: password })
  });
  if(!res.ok) throw new Error("Login failed");
  return res.json();
}

async function apiRegister(name, email, password){
  if(DEMO_MODE){
    const u = { user_id: 1, user_email: email, user_name: name || email.split("@")[0] };
    demo.setUser(u);
    return u;
  }
  const res = await fetch(`${API_BASE}/auth/register`, {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ user_name:name, user_email:email, user_password:password })
  });
  if(!res.ok) throw new Error("Register failed");
  return res.json();
}

function requireAuth(){
  const u = demo.getUser();
  if(!u){
    window.location.href = "index.html";
    return null;
  }
  return u;
}

function logout(){
  demo.logout();
  window.location.href = "index.html";
}

// ---------- vehicles ----------
function listVehicles(){
  return demo.getVehicles().sort((a,b)=> (b.vee_stamped||"").localeCompare(a.vee_stamped||""));
}
function addVehicle(v){
  const vehicles = demo.getVehicles();
  const nextId = (vehicles.reduce((m,x)=>Math.max(m, x.vee_id||0),0) + 1);
  vehicles.push({ ...v, vee_id: nextId, vee_stamped: new Date().toISOString() });
  demo.setVehicles(vehicles);
  return nextId;
}
function updateVehicle(id, patch){
  const vehicles = demo.getVehicles().map(v => v.vee_id===id ? ({...v, ...patch}) : v);
  demo.setVehicles(vehicles);
}
function deleteVehicle(id){
  demo.setVehicles(demo.getVehicles().filter(v => v.vee_id!==id));
  // delete its records too
  demo.setRecords(demo.getRecords().filter(r => r.vee_id!==id));
}

// ---------- service records ----------
function listRecordsForVehicle(vee_id){
  return demo.getRecords()
    .filter(r=> r.vee_id===vee_id)
    .sort((a,b)=> (b.service_record_date).localeCompare(a.service_record_date));
}
function addRecord(rec){
  const records = demo.getRecords();
  const nextId = (records.reduce((m,x)=>Math.max(m, x.service_record_id||0),0) + 1);
  records.push({ ...rec, service_record_id: nextId, created_at: new Date().toISOString() });
  demo.setRecords(records);
}
function deleteRecord(id){
  demo.setRecords(demo.getRecords().filter(r => r.service_record_id!==id));
}

// ---------- computed: due status ----------
function computeDue(vee, records, serviceTypes){
  // For each service type: find latest record mileage/date; compute remaining miles/days
  const now = new Date();
  const items = serviceTypes.map(st => {
    const latest = records.find(r => r.service_type_id === st.service_type_id) || null;
    let milesLeft = null;
    let daysLeft = null;

    if(st.service_type_default_interval_miles != null){
      const lastMiles = latest ? latest.service_record_mileage : vee.vee_mileage;
      milesLeft = (lastMiles + st.service_type_default_interval_miles) - vee.vee_mileage;
    }
    if(st.service_type_default_interval_days != null){
      const lastDate = latest ? new Date(latest.service_record_date+"T00:00:00") : null;
      if(lastDate){
        const dueDate = new Date(lastDate);
        dueDate.setDate(dueDate.getDate() + Number(st.service_type_default_interval_days));
        daysLeft = Math.ceil((dueDate - now) / (1000*60*60*24));
      } else {
        daysLeft = st.service_type_default_interval_days; // unknown history
      }
    }

    const isOverdue = (milesLeft != null && milesLeft <= 0) || (daysLeft != null && daysLeft <= 0);
    return { st, latest, milesLeft, daysLeft, isOverdue };
  });

  const overdueCount = items.filter(x=>x.isOverdue).length;
  return { overdueCount, items };
}
