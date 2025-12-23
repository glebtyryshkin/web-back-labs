let currentPage = 1;

document.addEventListener('DOMContentLoaded', () => {
    fetchBooks(true);
});

function fetchBooks(refresh = false) {
    if (refresh) {
        currentPage = 1;
        document.getElementById('books-grid').innerHTML = '';
    }

    const params = new URLSearchParams({
        page: currentPage,
        title: document.getElementById('filter-title').value,
        author: document.getElementById('filter-author').value,
        publisher: document.getElementById('filter-publisher').value,
        pages_min: document.getElementById('filter-pages-min').value,
        pages_max: document.getElementById('filter-pages-max').value,
        sort_by: document.getElementById('sort-by').value,
        sort_dir: document.getElementById('sort-dir').value
    });

    fetch(`/rgz/api/books/?${params.toString()}`)
    .then(res => res.json())
    .then(books => {
        const grid = document.getElementById('books-grid');
        
        // Получаем статус админа из атрибута HTML 
        const isAdmin = grid.getAttribute('data-is-admin') === 'true';

        books.forEach(book => {
            const card = document.createElement('div');
            card.className = 'book-card';
            
            let html = `
                <img src="${book.cover_url}" alt="Обложка" style="width: 150px; height: 220px; object-fit: cover;">
                <h4>${book.title}</h4>
                <p><b>${book.author}</b></p>
                <p>${book.pages} стр., ${book.publisher}</p>
            `;

            if (isAdmin) {
                html += `
                    <button onclick="editBook(${book.id})">Ред.</button>
                    <button class="danger" onclick="deleteBook(${book.id})">Удалить</button>
                `;
            }

            card.innerHTML = html;
            grid.appendChild(card);
        });

        const countSpan = document.getElementById('count-info');
        countSpan.innerText = grid.children.length; 
        
        const btnNext = document.getElementById('btn-next');
        if (books.length < 20) {
            btnNext.style.display = 'none';
        } else {
            btnNext.style.display = 'inline-block';
        }
    })
    .catch(err => console.error("Ошибка загрузки:", err));
}

function applyFilters() {
    fetchBooks(true);
}

function clearFilters() {
    document.getElementById('filter-title').value = '';
    document.getElementById('filter-author').value = '';
    document.getElementById('filter-publisher').value = '';
    document.getElementById('filter-pages-min').value = '';
    document.getElementById('filter-pages-max').value = '';
    fetchBooks(true);
}

function loadNextPage() {
    currentPage++;
    fetchBooks(false);
}

function deleteBook(id) {
    if (confirm('Удалить книгу?')) {
        fetch(`/rgz/api/books/${id}`, { method: 'DELETE' })
        .then(() => {
            fetchBooks(true);
        });
    }
}

function openModal(id = null) {
    const modal = document.getElementById('book-modal');
    modal.style.display = 'block';
    
    if (!id) {
        // Очистка для новой книги
        document.getElementById('book-id').value = '';
        document.getElementById('input-title').value = '';
        document.getElementById('input-author').value = '';
        document.getElementById('input-publisher').value = '';
        document.getElementById('input-pages').value = '';
        document.getElementById('input-cover').value = '';
        document.getElementById('modal-title').innerText = 'Добавить книгу';
    }
}

function closeModal() {
    document.getElementById('book-modal').style.display = 'none';
}

function editBook(id) {
    openModal(id);
    document.getElementById('modal-title').innerText = 'Редактирование книги';
    
    // Загружаем данные книги
    fetch(`/rgz/api/books/${id}`)
    .then(res => res.json())
    .then(book => {
        document.getElementById('book-id').value = book.id;
        document.getElementById('input-title').value = book.title;
        document.getElementById('input-author').value = book.author;
        document.getElementById('input-publisher').value = book.publisher;
        document.getElementById('input-pages').value = book.pages;
        document.getElementById('input-cover').value = book.cover_url;
    })
    .catch(err => console.error("Ошибка загрузки книги:", err));
}

function saveBook() {
    const id = document.getElementById('book-id').value;
    const book = {
        title: document.getElementById('input-title').value,
        author: document.getElementById('input-author').value,
        publisher: document.getElementById('input-publisher').value,
        pages: document.getElementById('input-pages').value,
        cover_url: document.getElementById('input-cover').value || '/static/rgz/book_cover.jpg'
    };
    
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/rgz/api/books/${id}` : '/rgz/api/books/';
    
    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(book)
    }).then(() => {
        closeModal();
        fetchBooks(true);
    });
}
