document.addEventListener("DOMContentLoaded", () => {
    const openButton = document.getElementById("open");
    const modalContainer = document.getElementById("modal_container");
    const createEmployeeForm = document.getElementById("createEmployeeForm");
    const createButton = document.getElementById("create");
    const employeeList = document.getElementById("employeeList");
    const loginModalContainer = document.getElementById("login_modal_container");
    const loginButton = document.getElementById("loginButton");
    const deleteButton = document.getElementById("delete");
    const deleteModalContainer = document.getElementById("delete_modal_container");
    const deleteEmployeeList = document.getElementById("deleteEmployeeList");
    const updateButton = document.getElementById("update");
    const updateModalContainer = document.getElementById("update_modal_container");
    const updateEmployeeList = document.getElementById("updateEmployeeList");
    const updateFormModalContainer = document.getElementById("update_form_modal_container");
    const updateEmployeeForm = document.getElementById("updateEmployeeForm");
    const updateSubmitButton = document.getElementById("updateSubmit");
    const logoutLink = document.querySelector("a[href='index.html']");

    let userToUpdate = null;

    // Open modal logic
    if (openButton && modalContainer) {
        openButton.addEventListener("click", () => {
            modalContainer.classList.add("show");
        });

        modalContainer.querySelector('.modal-content').addEventListener("click", (event) => {
            event.stopPropagation();
        });

        modalContainer.addEventListener("click", () => {
            modalContainer.classList.remove("show");
        });
    }

    if (logoutLink) {
        logoutLink.addEventListener("click", (event) => {
            event.preventDefault();
            window.location.href = "index.html";
        });
    }

    // Fetch and display all employees
    async function fetchAndDisplayEmployees() {
        try {
            const response = await fetch('/users/');
            if (!response.ok) {
                console.error('Failed to fetch employees'); // Silent error logging
                return; // Exit function on failure
            }

            const users = await response.json();
            employeeList.innerHTML = ''; // Clear current list

            users.forEach(user => {
                const employeeCard = document.createElement("div");
                employeeCard.classList.add("employee-card");
                employeeCard.innerHTML = `
                    <h3>${user.username}</h3>
                    <p>Employee</p>
                `;
                employeeList.appendChild(employeeCard);
            });
        } catch (error) {
            console.error('Error fetching employees:', error);
        }
    }

    // Fetch employees on page load
    fetchAndDisplayEmployees();

    // Create employee logic
    if (createButton && createEmployeeForm && employeeList && modalContainer) {
        createButton.addEventListener("click", async () => {
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
    
            if (username && password) {
                const userData = {
                    username: username,
                    password: password
                };
    
                try {
                    const response = await fetch('/users/create', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(userData)
                    });
    
                    if (!response.ok) {
                        throw new Error('Failed to create user');
                    }
    
                    const user = await response.json();
    
                    alert(`User ${user.username} created successfully!`);
    
                    const employeeCard = document.createElement("div");
                    employeeCard.classList.add("employee-card");
                    employeeCard.innerHTML = `
                        <h3>${user.username}</h3>
                        <p>Employee</p>
                    `;
                    employeeList.appendChild(employeeCard);
    
                    createEmployeeForm.reset();
                    modalContainer.classList.remove("show");
                } catch (error) {
                    console.error('Error creating user:', error);
                    alert('Failed to create user. Please try again later.');
                }
            } else {
                alert("Please enter both username and password.");
            }
        });
    }

    // Delete modal logic
    if (deleteButton && deleteModalContainer) {
        deleteButton.addEventListener("click", () => {
            updateDeleteEmployeeList();
            deleteModalContainer.classList.add("show");
        });

        deleteModalContainer.querySelector('.modal-content').addEventListener("click", (event) => {
            event.stopPropagation();
        });

        deleteModalContainer.addEventListener("click", () => {
            deleteModalContainer.classList.remove("show");
        });
    }

    // Update the employee list for deletion
    function updateDeleteEmployeeList() {
        deleteEmployeeList.innerHTML = "";
        const employeeCards = document.querySelectorAll(".employee-card");
        employeeCards.forEach((card, index) => {
            const deleteItem = document.createElement("div");
            deleteItem.classList.add("delete-item");
            deleteItem.innerHTML = `
                ${card.innerHTML}
                <button class="delete-button" data-index="${index}">Delete</button>
            `;
            deleteEmployeeList.appendChild(deleteItem);
        });

        const deleteButtons = deleteEmployeeList.querySelectorAll(".delete-button");
        deleteButtons.forEach((button) => {
            button.addEventListener("click", async (event) => {
                const index = event.target.getAttribute("data-index");
                const employeeCard = document.querySelectorAll(".employee-card")[index];
                const username = employeeCard.querySelector("h3").innerText;

                try {
                    const response = await fetch(`/users/${username}`, {
                        method: 'DELETE'
                    });

                    if (!response.ok) {
                        throw new Error('Failed to delete user');
                    }

                    alert(`User ${username} deleted successfully!`);

                    employeeCard.remove();
                    updateDeleteEmployeeList();
                } catch (error) {
                    console.error('Error deleting user:', error);
                    alert('Failed to delete user. Please try again later.');
                }
            });
        });
    }

    if (updateButton && updateModalContainer) {
        updateButton.addEventListener("click", () => {
            updateEmployeeListContent();
            updateModalContainer.classList.add("show");
        });

        updateModalContainer.addEventListener("click", () => {
            updateModalContainer.classList.remove("show");
        });

        updateModalContainer.querySelector('.modal-content').addEventListener("click", (event) => {
            event.stopPropagation();
        });
    }

    // Update the employee list for updating
    function updateEmployeeListContent() {
        updateEmployeeList.innerHTML = "";
        const employeeCards = document.querySelectorAll(".employee-card");

        employeeCards.forEach((card, index) => {
            const updateItem = document.createElement("div");
            updateItem.classList.add("update-item");
            updateItem.innerHTML = `
                ${card.innerHTML}
                <button class="update-button" data-index="${index}">Update</button>
            `;
            updateEmployeeList.appendChild(updateItem);
        });

        // Add event listeners for update buttons
        const updateButtons = updateEmployeeList.querySelectorAll(".update-button");
        updateButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                const index = event.target.getAttribute("data-index");
                const employeeCard = document.querySelectorAll(".employee-card")[index];
                const username = employeeCard.querySelector("h3").innerText;
                userToUpdate = username;

                // Show update form modal and pre-fill form
                document.getElementById("updateUsername").value = username;
                document.getElementById("updatePassword").value = '';
                updateFormModalContainer.classList.add("show");
            });
        });
    }

    // Handle update submission
    if (updateSubmitButton && updateFormModalContainer) {
        updateSubmitButton.addEventListener("click", async () => {
            const newUsername = document.getElementById("updateUsername").value.trim();
            const newPassword = document.getElementById("updatePassword").value.trim();

            if (userToUpdate && newUsername && newPassword) {
                try {
                    const payload = { new_username: newUsername, new_password: newPassword };
                    console.log('Sending payload:', payload); // Debugging line

                    const response = await fetch(`/users/${userToUpdate}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    });

                    const responseData = await response.json();

                    if (!response.ok) {
                        let errorMessage = 'Failed to update user:';
                        if (responseData.detail) {
                            errorMessage += ` ${responseData.detail.map(err => err.msg).join(', ')}`;
                        } else {
                            errorMessage += ' Unknown error';
                        }
                        throw new Error(errorMessage);
                    }

                    alert(`User ${responseData.username} updated successfully!`);

                    // Update employee card
                    const employeeCard = Array.from(document.querySelectorAll(".employee-card"))
                        .find(card => card.querySelector("h3").innerText === userToUpdate);
                    if (employeeCard) {
                        employeeCard.querySelector("h3").innerText = responseData.username;
        
                    }

                    updateFormModalContainer.classList.remove("show");
                    updateModalContainer.classList.remove("show");
                } catch (error) {
                    console.error('Error updating user:', error);
                    alert(error.message || 'Failed to update user. Please try again later.');
                }
            } else {
                alert("Please enter both username and password.");
            }
        });
    }
});
