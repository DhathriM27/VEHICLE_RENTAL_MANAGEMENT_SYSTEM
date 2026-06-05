
// ---------------- LOAD VEHICLES ----------------
async function loadVehicles() {

    const res = await fetch("http://127.0.0.1:5000/vehicles");
    const data = await res.json();

    const container = document.getElementById("vehicleList");
    container.innerHTML = "";

    data.forEach(v => {
        container.innerHTML += `
            <div class="vehicle">
                <b>ID:</b> ${v.vehicle_id} <br>
                <b>Name:</b> ${v.vehicle_name} <br>
                <b>Type:</b> ${v.vehicle_type} <br>
                <b>Rent:</b> ₹${v.rent_per_day} <br>
                <b>Available:</b> ${v.availability}
            </div>
        `;
    });
}


// ---------------- ADD VEHICLE ----------------
async function addVehicle() {

    const data = {
        vehicle_name: document.getElementById("v_name").value="",
        vehicle_type: document.getElementById("v_type").value="",
        rent_per_day: document.getElementById("v_rent").value=""
    };

    const res = await fetch("http://127.0.0.1:5000/add_vehicle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);
    loadVehicles();
}


// ---------------- ADD CUSTOMER ----------------
async function addCustomer() {

    const data = {
        customer_name: document.getElementById("c_name").value="",
        phone: document.getElementById("c_phone").value="",
        email: document.getElementById("c_email").value=""
    };

    const res = await fetch("http://127.0.0.1:5000/add_customer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);
}


// ---------------- RENT VEHICLE ----------------
async function rentVehicle() {

    const data = {
        customer_id: document.getElementById("r_customer").value="",
        vehicle_id: document.getElementById("r_vehicle").value=""
    };

    const res = await fetch("http://127.0.0.1:5000/rent_vehicle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);
}