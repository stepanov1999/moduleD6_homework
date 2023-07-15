const commentsList = document.querySelector('#comments-list');
const commentsHeader = document.querySelector('#comments-header');
const confirmDeleteCommentButton = document.querySelector('#confirm-delete-comment');

//Add Comment
const addCommentForm = document.getElementById('addCommentForm');
if (addCommentForm) {
    addCommentForm.addEventListener('submit', addComment);
}

function addComment(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const url = form.action;
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data.success) {
                const commentItem = `
                <li class="shadow rounded-3 mb-3">
                    <div class="row p-2">
                        <span class="me-auto"><strong>Author: </strong>${data.comment_user}</span>
                        <span class="ms-auto">${data.comment_publish_time}</span>
                    </div>
                    <hr class="my-0 mx-auto" style="width: 95%">
                    <div class="mx-3 mt-3 text-start">
                        <p style="word-break: break-word" class="m-0 pb-3">${data.comment_text}</p>
                    </div>
                    <hr class="my-0 mx-auto" style="width: 95%">
                    <button 
                        class="btn-sm btn-secondary my-2" 
                        data-bs-toggle="modal" 
                        data-bs-target="#deleteCommentModal" 
                        name="delete_comment" 
                        data-delete-url="${data.comment_delete_url}"
                        onclick="deleteComment(event)"
                        >
                            Delete
                            </button>
                </li>
                `;
                commentsList.insertAdjacentHTML('beforeend', commentItem);
                form.reset();
                commentsHeader.textContent = 'Comments:';
            } else {
                const errors = data.errors;
                const errorList = document.getElementById('error-list');
                errorList.innerHTML = '';
                for (const [key, value] of Object.entries(errors)) {
                    const errorItem = `
                        <li>${key}: ${value}</li>
                `;
                    errorList.insertAdjacentHTML('beforeend', errorItem);
                }
            }
        })
        .catch((error) => console.log(error));
}

//delete Comment
function deleteComment(event) {
    let deleteButton = event.target;
    let deleteUrl = deleteButton.dataset.deleteUrl;
    confirmDeleteCommentButton.addEventListener('click',
        function ConfirmDeleteCommentClick() {
            fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.deleted) {
                        event.target.parentNode.remove();
                        confirmDeleteCommentButton.removeEventListener('click',
                            ConfirmDeleteCommentClick);
                        if (commentsList.innerText.trim() === '') {
                            commentsHeader.textContent = '';
                        }
                    }
                })
                .catch((error) => console.log(error));
        })

}

//subscribe to Category
function subscribeCategory(event) {
    let button = event.target;
    let url = button.dataset.url;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
        .then(response => response.json())
        .then((data) => {
            if (data.success) {
                let sameButtons = document.querySelectorAll(`button[data-url="${url}"]`)
                sameButtons.forEach((button) => {
                    button.classList.replace('btn-outline-secondary', 'btn-secondary');
                    button.title = "Press to unsubscribe"
                    button.dataset.url = data.url;
                    button.onclick = unsubscribeCategory
                })
            } else {
                console.log(data.errors)
            }
        })
        .catch(errors => console.log(errors))
}

//unsubscribe to Category
function unsubscribeCategory(event) {
    let button = event.target;
    let url = button.dataset.url;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
        .then(response => response.json())
        .then((data) => {
            if (data.success) {
                let sameButtons = document.querySelectorAll(`button[data-url="${url}"]`)
                sameButtons.forEach((button) => {
                    button.classList.replace('btn-secondary', 'btn-outline-secondary');
                    button.title = "Press to subscribe"
                    button.dataset.url = data.url;
                    button.onclick = subscribeCategory
                })
            }
        })
        .catch(errors => console.log(errors))
}


function votePost (event) {
    let button = event.target;
    let url = button.dataset.url;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
        .then(response => response.json())
        .then((data) => {
            if (data.success) {
                let voteCount = button.parentNode.firstElementChild.lastElementChild.lastElementChild.textContent;
                button.parentNode.firstElementChild.lastElementChild.lastElementChild.textContent = +(voteCount) + 1;
                button.remove();
            }
        })
        .catch(errors => console.log(errors))
}





