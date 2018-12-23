const API_URL = window.location.origin;

(() => {
  const form = document.getElementById('recommendationForm');
  form.onsubmit = (event) => {
    event.preventDefault();
    const course = document.getElementById('course').value;

    fetch(`${API_URL}/recommendations?course=${course}`)
      .then(response => {
        if (!response.ok) { throw response; }
        return response.json()
      })
      .then(data => {
        const bookList = document.getElementById('bookList');
        bookList.innerHTML = '';

        data.books.forEach(book => {
          const bookItem = document.createElement('li');
          bookItem.appendChild(document.createTextNode(`${book.title}, ${book.author}`));
          bookList.appendChild(bookItem);
        });
      })
      .catch(response => response.json().then(error => alert(error.message) ));
  }
})();
