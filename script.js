function generateGuestFields() {
    const guestNumber = document.getElementById("guestNumber").value;
    const guestFields = document.getElementById("guestFields");
    guestFields.innerHTML = '';

    for (let i = 1; i <= guestNumber; i++) {
        const guestDiv = document.createElement('div');
        guestDiv.innerHTML = `
            <h3>Guest ${i}</h3>
            <label for="guest${i}Name">Guest ${i} Name:</label>
            <input type="text" id="guest${i}Name" name="guest${i}Name" required>
        `;
        guestFields.appendChild(guestDiv);
    }
}
