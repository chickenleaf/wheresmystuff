const API_URL = 'http://localhost:8000';

document.getElementById('submitItemForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        location: document.getElementById('location').value,
        status: document.getElementById('status').value
    };

    try {
        const response = await fetch(`${API_URL}/items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Item submitted successfully!');
            e.target.reset();
        } else {
            alert('Failed to submit item. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});

document.getElementById('searchItemForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const searchQuery = document.getElementById('searchQuery').value;

    try {
        const response = await fetch(`${API_URL}/items/?search=${encodeURIComponent(searchQuery)}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            const items = await response.json();
            displaySearchResults(items);
        } else {
            alert('Failed to search items. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});

function displaySearchResults(items) {
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';

    items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `
            <h5>${item.title}</h5>
            <p>${item.description}</p>
            <p><strong>Category:</strong> ${item.category}</p>
            <p><strong>Location:</strong> ${item.location}</p>
            <p><strong>Status:</strong> ${item.status}</p>
        `;
        resultsList.appendChild(li);
    });

    document.getElementById('searchResults').style.display = 'block';
}

// Add login and registration functionality here