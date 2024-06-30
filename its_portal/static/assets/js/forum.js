//its_portal/static/assets/js/forum.js

//document.addEventListener('DOMContentLoaded', function() {
//    const forumUrl = document.getElementById('main-area').getAttribute('data-url');
//
//    function loadPosts() {
//        fetch(forumUrl)
//            .then(response => {
//                if (!response.ok) {
//                    throw new Error('Network response was not ok ' + response.statusText);
//                }
//                return response.json();
//            })
//            .then(data => {
//                const postList = document.getElementById('recent-posts-list');
//                postList.innerHTML = data.posts.map(post => `
//                    <div class="list-group-item">
//                        <div class="d-flex align-items-start">
//                            ${post.profile_picture ? `<img src="${post.profile_picture}" alt="Avatar" class="rounded-circle me-3" width="40" height="40">` : `<img src="{% static 'assets/images/default_avatar.png' %}" alt="Default Avatar" class="rounded-circle me-3" width="40" height="40">`}
//                            <div class="flex-fill">
//                                <a href="${post.url}">${post.title}</a>
//                                <p class="mb-0">${post.content}</p>
//                                <small class="text-muted">${post.created_at}</small>
//                            </div>
//                            <a href="${post.reply_url}" class="btn btn-primary ms-3">Reply</a>
//                        </div>
//                    </div>
//                `).join('');
//            })
//            .catch(error => {
//                console.error('There was a problem with the fetch operation:', error);
//                const postList = document.getElementById('recent-posts-list');
//                postList.innerHTML = `<div class="alert alert-danger" role="alert">Error loading posts. Please try again later.</div>`;
//            });
//    }
//
//    loadPosts();
//});

