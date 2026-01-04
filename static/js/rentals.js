const RENTALS_API = "http://localhost:8000/api/v1/rentals";
const CUSTOMER_RENTALS_API = "http://localhost:8000/api/v1/customers";

const tableBody = document.querySelector("#rentals-table tbody");
const rentalFormSection = document.querySelector("#rental-form-section");
const customerIdFilterInput = document.querySelector("#customerIdFilter");
const btnFilterCustomer = document.querySelector("#btn-filter-customer");
const btnClearFilter = document.querySelector("#btn-clear-filter");
const btnNewRental = document.querySelector("#btn-new-rental");

async function loadRentals() {
    const res = await fetch(RENTALS_API);
    const data = await res.json();
    renderRentalsTable(data);
}

function renderRentalsTable(rentals) {
    tableBody.innerHTML = "";

    rentals.forEach(r => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${r.rental_id}</td>
            <td>${r.customer_id}</td>
            <td>${r.inventory_id}</td>
            <td>${r.staff_id}</td>
            <td>${r.rental_date}</td>
            <td>${r.return_date || "Pendiente"}</td>
            <td>
                ${
                    r.return_date 
                        ? "" 
                        : `<button onclick="markReturned(${r.rental_id})">Marcar devuelto</button>`
                }
            </td>
        `;

        tableBody.appendChild(tr);
    });

    if (rentals.length === 0) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="7">No hay alquileres</td>`;
        tableBody.appendChild(tr);
    }
}

async function loadRentalsByCustomer(customerId) {
    const res = await fetch(`${CUSTOMER_RENTALS_API}/${customerId}/rentals`);
    if (!res.ok) {
        alert("Error obteniendo alquileres del cliente");
        return;
    }
    const data = await res.json();
    renderRentalsTable(data);
}

async function markReturned(rentalId) {
    const res = await fetch(`${RENTALS_API}/${rentalId}/return`, {
        method: "PUT",
    });
    if (!res.ok) {
        alert("Error marcando devolución");
        return;
    }
    loadRentals();
}


function showNewRentalForm() {
    rentalFormSection.classList.remove("hidden");
    rentalFormSection.innerHTML = `
        <h3>Nuevo alquiler</h3>
        <form id="new-rental-form">
            <label>
                Inventory ID:
                <input type="number" id="inventory_id" required>
            </label>
            <label>
                Customer ID:
                <input type="number" id="customer_id" required>
            </label>
            <label>
                Staff ID:
                <input type="number" id="staff_id" required>
            </label>
            <button type="submit">Crear</button>
            <button type="button" id="btn-cancel-rental">Cancelar</button>
        </form>
    `;

    document.querySelector("#btn-cancel-rental").onclick = () => {
        rentalFormSection.classList.add("hidden");
        rentalFormSection.innerHTML = "";
    };

    document.querySelector("#new-rental-form").onsubmit = async (e) => {
        e.preventDefault();
        const body = {
            inventory_id: Number(document.querySelector("#inventory_id").value),
            customer_id: Number(document.querySelector("#customer_id").value),
            staff_id: Number(document.querySelector("#staff_id").value),
        };

        const res = await fetch(RENTALS_API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
    if (!res.ok) {
    const error = await res.json();
    alert("❌ Error creando alquiler:\n" + JSON.stringify(error));
    return;
}

        rentalFormSection.classList.add("hidden");
        rentalFormSection.innerHTML = "";
        loadRentals();
    };
}

btnFilterCustomer.onclick = () => {
    const id = customerIdFilterInput.value;
    if (!id) {
        alert("Introduce un ID de cliente");
        return;
    }
    loadRentalsByCustomer(id);
};

btnClearFilter.onclick = () => {
    customerIdFilterInput.value = "";
    loadRentals();
};

btnNewRental.onclick = () => {
    showNewRentalForm();
};

loadRentals();