const API_URL = "http://localhost:8000/api/v1/customers";

const tableBody = document.querySelector("#customers-table tbody");
const searchInput = document.querySelector("#search");
const formSection = document.querySelector("#form-section");
const btnNew = document.querySelector("#btn-new");

async function loadCustomers() {
    const res = await fetch(API_URL);
    const data = await res.json();
    renderTable(data);
}

function renderTable(customers) {
    tableBody.innerHTML = "";

    customers.forEach(c => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${c.customer_id}</td>
            <td>${c.first_name} ${c.last_name}</td>
            <td>${c.email}</td>
            <td>${c.active ? "Sí" : "No"}</td>
            <td>
                <button onclick="editCustomer(${c.customer_id})">Editar</button>
                <button onclick="deleteCustomer(${c.customer_id})">Borrar</button>
            </td>
        `;

        tableBody.appendChild(tr);
    });
}

async function deleteCustomer(id) {
    if (!confirm("¿Seguro que quieres borrar este cliente?")) return;

    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    loadCustomers();
}

function editCustomer(id) {
    formSection.classList.remove("hidden");
    formSection.innerHTML = `
        <h3>Editar Cliente</h3>
        <form id="edit-form">
            <label>Email:
                <input type="email" id="email">
            </label>
            <label>Activo:
                <select id="active">
                    <option value="1">Sí</option>
                    <option value="0">No</option>
                </select>
            </label>
            <button type="submit">Guardar</button>
        </form>
    `;

    document.querySelector("#edit-form").onsubmit = async (e) => {
        e.preventDefault();

        const email = document.querySelector("#email").value;
        const active = Number(document.querySelector("#active").value);

        await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, active })
        });

        formSection.classList.add("hidden");
        loadCustomers();
    };
}

btnNew.onclick = () => {
    formSection.classList.remove("hidden");
    formSection.innerHTML = `
        <h3>Nuevo Cliente</h3>
        <form id="new-form">
            <label>Nombre:
                <input type="text" id="first_name" required>
            </label>
            <label>Apellidos:
                <input type="text" id="last_name" required>
            </label>
            <label>Email:
                <input type="email" id="email" required>
            </label>
            <label>Store ID:
                <input type="number" id="store_id" value="1" required>
            </label>
            <label>Address ID:
                <input type="number" id="address_id" value="1" required>
            </label>
            <button type="submit">Crear</button>
        </form>
    `;

    document.querySelector("#new-form").onsubmit = async (e) => {
        e.preventDefault();

        const body = {
            first_name: document.querySelector("#first_name").value,
            last_name: document.querySelector("#last_name").value,
            email: document.querySelector("#email").value,
            store_id: Number(document.querySelector("#store_id").value),
            address_id: Number(document.querySelector("#address_id").value),
            active: 1
        };

        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const error = await res.json();
            alert("❌ Error al crear cliente:\n" + JSON.stringify(error));
            return;
        }

        alert("✅ Cliente creado correctamente");
        formSection.classList.add("hidden");
        loadCustomers();
    };
};

loadCustomers();