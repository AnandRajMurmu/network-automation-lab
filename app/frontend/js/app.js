"use strict";

const API_BASE = "/api";
const DEVICE_ENDPOINT = `${API_BASE}/devices`;

const elements = {
    apiStatus: document.getElementById("api-status"),
    totalDevices: document.getElementById("total-devices"),
    activeDevices: document.getElementById("active-devices"),
    inactiveDevices: document.getElementById("inactive-devices"),
    tableBody: document.getElementById("device-table-body"),
    inventoryCount: document.getElementById("inventory-count"),
    refreshButton: document.getElementById("refresh-button"),
    addButton: document.getElementById("add-device-button"),
    formPanel: document.getElementById("device-form-panel"),
    form: document.getElementById("device-form"),
    formTitle: document.getElementById("form-title"),
    deviceId: document.getElementById("device-id"),
    hostname: document.getElementById("hostname"),
    managementIp: document.getElementById("management-ip"),
    deviceType: document.getElementById("device-type"),
    location: document.getElementById("location"),
    status: document.getElementById("device-status"),
    saveButton: document.getElementById("save-button"),
    cancelButton: document.getElementById("cancel-button"),
    resetButton: document.getElementById("reset-button"),
    notification: document.getElementById("notification"),
};

let devices = [];
let notificationTimer = null;
let loadingDevices = false;

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...options.headers,
        },
    });

    const contentType = response.headers.get("content-type") || "";
    let data = null;

    if (contentType.includes("application/json")) {
        data = await response.json();
    } else if (response.status !== 204) {
        data = await response.text();
    }

    if (!response.ok) {
        const detail =
            data && typeof data === "object"
                ? data.detail
                : null;

        const message = Array.isArray(detail)
            ? detail.map((item) => item.msg).join("; ")
            : detail || `Request failed with HTTP ${response.status}`;

        throw new Error(message);
    }

    return data;
}

function showNotification(message, type = "success") {
    clearTimeout(notificationTimer);

    elements.notification.textContent = message;
    elements.notification.className = `notification ${type}`;
    elements.notification.hidden = false;

    notificationTimer = setTimeout(() => {
        elements.notification.hidden = true;
    }, 4000);
}

function setApiStatus(online) {
    elements.apiStatus.classList.toggle("online", online);
    elements.apiStatus.classList.toggle("offline", !online);

    const indicator = elements.apiStatus.querySelector(".status-indicator");

    elements.apiStatus.replaceChildren();

    const statusIndicator = document.createElement("span");
    statusIndicator.className = "status-indicator";

    elements.apiStatus.append(
        statusIndicator,
        document.createTextNode(online ? "API Connected" : "API Unavailable"),
    );
}

async function checkApiHealth() {
    try {
        await apiRequest(`${API_BASE}/health`);
        setApiStatus(true);
    } catch (error) {
        setApiStatus(false);
        console.error("API health check failed:", error);
    }
}

function createCell(value, className = "") {
    const cell = document.createElement("td");
    cell.textContent = value ?? "";

    if (className) {
        cell.className = className;
    }

    return cell;
}

function createStatusBadge(status) {
    const badge = document.createElement("span");
    const normalizedStatus = String(status || "").toLowerCase();

    badge.className = "status-badge";

    if (["active", "inactive", "maintenance"].includes(normalizedStatus)) {
        badge.classList.add(`status-${normalizedStatus}`);
    }

    badge.textContent = status || "unknown";
    return badge;
}

function createActionButton(label, className, callback) {
    const button = document.createElement("button");

    button.type = "button";
    button.className = `button ${className}`;
    button.textContent = label;
    button.addEventListener("click", callback);

    return button;
}

function renderDevices() {
    elements.tableBody.replaceChildren();

    elements.totalDevices.textContent = devices.length;

    const activeCount = devices.filter(
        (device) => device.status === "active",
    ).length;

    elements.activeDevices.textContent = activeCount;
    elements.inactiveDevices.textContent = devices.length - activeCount;

    elements.inventoryCount.textContent =
        `${devices.length} device${devices.length === 1 ? "" : "s"} found`;

    if (devices.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 7;
        cell.className = "table-message";
        cell.textContent = "No devices found. Add a device to get started.";

        row.appendChild(cell);
        elements.tableBody.appendChild(row);
        return;
    }

    for (const device of devices) {
        const row = document.createElement("tr");

        row.append(
            createCell(device.id),
            createCell(device.hostname, "device-hostname"),
            createCell(device.management_ip, "device-ip"),
            createCell(device.device_type),
            createCell(device.location),
        );

        const statusCell = document.createElement("td");
        statusCell.appendChild(createStatusBadge(device.status));
        row.appendChild(statusCell);

        const actionsCell = document.createElement("td");
        const actions = document.createElement("div");

        actions.className = "device-actions";

        actions.append(
            createActionButton("Edit", "button-secondary", () => {
                openEditForm(device);
            }),
            createActionButton("Delete", "button-danger", () => {
                deleteDevice(device);
            }),
        );

        actionsCell.appendChild(actions);
        row.appendChild(actionsCell);

        elements.tableBody.appendChild(row);
    }
}

async function loadDevices() {
    if (loadingDevices) {
        return;
    }

    loadingDevices = true;
    elements.refreshButton.disabled = true;

    elements.inventoryCount.textContent = "Loading inventory...";

    try {
        const result = await apiRequest(DEVICE_ENDPOINT);

        if (!Array.isArray(result)) {
            throw new Error("The API returned an invalid inventory response.");
        }

        devices = result;
        renderDevices();
        setApiStatus(true);
    } catch (error) {
        console.error("Failed to load devices:", error);

        elements.tableBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 7;
        cell.className = "table-message";
        cell.textContent = "Unable to load inventory. Check the API and retry.";

        row.appendChild(cell);
        elements.tableBody.appendChild(row);

        elements.inventoryCount.textContent = "Inventory unavailable";
        setApiStatus(false);
        showNotification(error.message, "error");
    } finally {
        loadingDevices = false;
        elements.refreshButton.disabled = false;
    }
}

function openCreateForm() {
    elements.form.reset();
    elements.deviceId.value = "";
    elements.formTitle.textContent = "Add Network Device";
    elements.saveButton.textContent = "Save Device";

    elements.formPanel.hidden = false;
    elements.formPanel.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    elements.hostname.focus();
}

function openEditForm(device) {
    elements.form.reset();

    elements.deviceId.value = device.id;
    elements.hostname.value = device.hostname;
    elements.managementIp.value = device.management_ip;
    elements.deviceType.value = device.device_type;
    elements.location.value = device.location;
    elements.status.value = device.status;

    elements.formTitle.textContent = `Edit Device #${device.id}`;
    elements.saveButton.textContent = "Update Device";

    elements.formPanel.hidden = false;
    elements.formPanel.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    elements.hostname.focus();
}

function closeForm() {
    elements.formPanel.hidden = true;
    elements.form.reset();
    elements.deviceId.value = "";
}

async function saveDevice(event) {
    event.preventDefault();

    if (!elements.form.reportValidity()) {
        return;
    }

    const id = elements.deviceId.value;

    const device = {
        hostname: elements.hostname.value.trim(),
        management_ip: elements.managementIp.value.trim(),
        device_type: elements.deviceType.value.trim(),
        location: elements.location.value.trim(),
        status: elements.status.value,
    };

    const isEditing = Boolean(id);
    const url = isEditing
        ? `${DEVICE_ENDPOINT}/${encodeURIComponent(id)}`
        : DEVICE_ENDPOINT;

    elements.saveButton.disabled = true;
    elements.saveButton.textContent = isEditing ? "Updating..." : "Saving...";

    try {
        await apiRequest(url, {
            method: isEditing ? "PUT" : "POST",
            body: JSON.stringify(device),
        });

        closeForm();

        showNotification(
            isEditing
                ? "Device updated successfully."
                : "Device created successfully.",
        );

        await loadDevices();
    } catch (error) {
        console.error("Failed to save device:", error);
        showNotification(error.message, "error");
    } finally {
        elements.saveButton.disabled = false;
        elements.saveButton.textContent = elements.deviceId.value
            ? "Update Device"
            : "Save Device";
    }
}

async function deleteDevice(device) {
    const confirmed = window.confirm(
        `Delete ${device.hostname} (${device.management_ip}) from the inventory?`,
    );

    if (!confirmed) {
        return;
    }

    try {
        await apiRequest(
            `${DEVICE_ENDPOINT}/${encodeURIComponent(device.id)}`,
            { method: "DELETE" },
        );

        showNotification(`${device.hostname} deleted successfully.`);
        await loadDevices();
    } catch (error) {
        console.error("Failed to delete device:", error);
        showNotification(error.message, "error");
    }
}

elements.refreshButton.addEventListener("click", loadDevices);
elements.addButton.addEventListener("click", openCreateForm);
elements.cancelButton.addEventListener("click", closeForm);

elements.resetButton.addEventListener("click", () => {
    if (!elements.deviceId.value) {
        elements.form.reset();
    }
});

elements.form.addEventListener("submit", saveDevice);

// Start the dashboard.
checkApiHealth();
loadDevices();
