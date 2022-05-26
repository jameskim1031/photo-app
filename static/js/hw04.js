const story2Html = story => {
    return `
        <div>
            <img src="${story.user.thumb_url}" class="pic" alt="profile pic for ${story.user.username}" />
            <p>${story.user.username}</p>
        </div>
    `;
};

const profile2Html = profile => {
    return `
    <div class="User">
        <img src="${profile.image_url}" alt="profile pic for ${profile.username}">
        <h1>${profile.username}</h1>
    </div>
    `;
};

const post2Html = post => {
    if (post.comments.length > 0) {
        const recentComment = post.comments[post.comments.length - 1]
        if (post.comments.length > 1) {
            var more = `
                <button data-post-id=${post.id} onclick="showModal(event)" class="viewAllComments" type="button" onclick="">View all ${post.comments.length} comments</button>
                <p><b>${recentComment.user.username}</b> ${recentComment.text}</p>
                <p class="timestamp"> ${recentComment.display_time}</p>
            `
        } else {
            var more = `
            <p>
                <b>${recentComment.user.username}</b> ${recentComment.text}
            </p>
            <p class="timestamp"> ${recentComment.display_time}</p>
            `
        }
    } else {
        var more = ``
    }
    return `
        <section id="post_${post.id}" class="card">
            <div class="Top">
                <h3>${post.user.username}</h3>
            </div>
            <img class="postImage" src=${post.image_url} alt="Image posted by ${post.user.username}">
            <div class="info">
                <div class="buttons">
                    <div>
                        ${renderLikeButton(post)}
                        <i class="far fa-comment"></i>
                        <i class="far fa-paper-plane"></i>
                    </div>
                    <div>
                        ${renderBookmarkButton(post)}
                    </div>
                </div>
                <p class="Likes">
                    <strong>${post.likes.length} like</strong>
                </p>
                <div class="caption">
                    <p>
                        <b>${post.user.username}</b> ${post.caption}
                    </p>
                    <p class="timestamp">${post.display_time}</p>
                </div>
                <div class="comments">
                    ${more}
                </div>
                <div class="add-comment">

                    <input class="comment-textbox_${post.id} comment-textbox"
                    type="text"
                    data-post-id="${post.id}"
                    aria-label="Add a comment" placeholder="Add a comment..." value>

                    <button onclick="addComment(event);"class="link" data-post-id="${post.id}">Post</button>

                </div>
            </div>
        </section>
    `;
};


const renderLikeButton = post => {
    if (post.current_user_like_id) {
        return `
            <button
                data-post-id="${post.id}"
                data-like-id="${post.current_user_like_id}"
                aria-label="Like/ Unlike"
                aria-checked="true"
                onclick="handleLike(event);">
                <i class="fas fa-heart"></i>
            </button>
        `;
    } else {
        return `
            <button
                data-post-id="${post.id}"
                data-like-id="${post.current_user_like_id}"
                aria-label="Like/ Unlike"
                aria-checked="false"
                onclick="handleLike(event);">
                <i class="far fa-heart"></i>
            </button>
        `;
    }
}


const handleLike = ev => {
    const elem = ev.currentTarget;
    if (elem.getAttribute('aria-checked') === 'true') {
        unlikePost(elem);
    } else {
        likePost(elem);
    }
};

const unlikePost = elem => {
    const postId = Number(elem.dataset.postId);
    console.log('unlike post', elem)
    fetch(`/api/posts/likes/${elem.dataset.likeId}`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('redraw the post');
            redrawPost(postId);
            // here is where we ask to redraw the post
        })
};

const likePost = elem => {
    const postId = Number(elem.dataset.postId);
    console.log('like post', elem);
    const postData = {
        "post_id": postId
    }
    fetch("/api/posts/likes/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('redraw the post');
            redrawPost(postId);
            // here is where we ask to redraw the post
        });
};

const renderBookmarkButton = post => {
    if (post.current_user_bookmark_id) {
        return `
            <button
                data-post-id="${post.id}"
                data-bookmark-id="${post.current_user_bookmark_id}"
                aria-label="Bookmark/ Unbookmark"
                aria-checked="true"
                onclick="handleBookmark(event);">
                <i class="fas fa-bookmark"></i>
            </button>
        `;
    } else {
        return `
            <button
                data-post-id="${post.id}"
                data-bookmark-id="${post.current_user_mark_id}"
                aria-label="Bookmark/ Unbookmark"
                aria-checked="false"
                onclick="handleBookmark(event);">
                <i class="far fa-bookmark"></i>
            </button>
        `;
    }
};


const handleBookmark = ev => {
    const elem = ev.currentTarget;
    if (elem.getAttribute('aria-checked') === 'true') {
        unbookmarkPost(elem);
    } else {
        bookmarkPost(elem);
    }
};

const unbookmarkPost = elem => {
    const postId = Number(elem.dataset.postId);
    console.log('unbookmark post', elem)
    fetch(`/api/bookmarks/${elem.dataset.bookmarkId}`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('redraw the post');
            redrawPost(postId);
            // here is where we ask to redraw the post
        })
};

const bookmarkPost = elem => {
    const postId = Number(elem.dataset.postId);
    console.log('bookmark post', elem);
    const postData = {
        "post_id": postId
    }
    fetch("/api/bookmarks/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log('redraw the post');
            redrawPost(postId);
            // here is where we ask to redraw the post
        });
};

const addComment = ev => {
    const postId = Number(ev.currentTarget.dataset.postId);
    const text = document.querySelector(`.comment-textbox_${postId}`).value;
    const postData = {
        "post_id": postId,
        "text": text,
    };

    fetch("/api/comments/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log("Posted" + postData)
        })
        .then(() => {
            displayPosts();
            console.log("updated post");
        })
};

const post2Modal = post => {
    return `
        <div class="modal-bg" aria-hidden="false" role="dialog">
            <button class="close" aria-label="Close the modal window" onclick="closeModal(event);">
            Close</button>
            <div class="modal">
                <img class="modalImage" src="${post.image_url}" />

                <div class="modalRight">
                    <div class="modalUser">
                        <img src="${post.user.thumb_url}" class="modalUserPic" alt="Profile picture for ${post.user.username}"/>
                        <h2>${post.user.username}</h2>
                    </div>
                    <div class = "modelComments"> 
                        ${displayComment(post)}
                    </div>
                </div>
            </div>
        </div>
    `;
};

/* Write displayComment function with for loop */
const displayComment = post => {
    const comments = post.comments
    let html ="";
    for (let i=0;i < comments.length;i++){
        console.log(comments[i]);
        html += `
            <div class="modalComment">
                <div class="modalUserImage">
                    <img src=${comments[i].user.thumb_url}/>
                </div>
                <div class="commentContent">
                    <p><strong>${comments[i].user.username}</strong>  ${comments[i].text}</p>
                    <p><strong>${comments[i].display_time}</strong></p>
                </div>
                <div class="modalUserImage">
                    <i class="far fa-heart"></i>
                </div>
            </div>
        `
    }
    return html;
}

const closeModal = ev => {
    const elem = ev.currentTarget;
    elem.setAttribute('aria-hidden','true')
    document.querySelector('.modal-bg').remove();
    document.querySelector('.viewAllComments').focus();
};


const showModal = ev => {
    const postId = Number(ev.currentTarget.dataset.postId);
    redrawPost(postId, post => {
        const html = post2Modal(post);
        document.querySelector(`#post_${post.id}`).insertAdjacentHTML('beforeend', html);
        document.querySelector('.close').focus();
    })
};

const stringToHTML = htmlString => {
    var parser = new DOMParser();
    var doc = parser.parseFromString(htmlString, 'text/html');
    return doc.body.firstChild;
};

const redrawPost = (postId, callback) => {
    // first, requery the API for the post that has just changed
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(updatedPost => {
            if (!callback) {
                redrawCard(updatedPost);
            } else {
                callback(updatedPost);
            }
        });
};

const redrawCard = post => {
    console.log(post);
    const html = post2Html(post);
    const newElement = stringToHTML(html);
    const postElement = document.querySelector(`#post_${post.id}`);
    console.log(newElement.innerHTML);
    postElement.innerHTML = newElement.innerHTML;
    // then, after you get the response, redraw the post
}

const user2Html = user => {
    return `
        <div class="Profiles">
            <img src="${user.thumb_url}" alt="profile pic for ${user.username}">
            <div class="Name">
                <h1>${user.username}</h1>
                <h2>suggested for you</h2>
            </div>
            <div>
                <button 
                class="follow" 
                aria-label="Follow / Unfollow"
                aria-checked="false"
                data-user-id = "${user.id}"
                onclick = "toggleFollow(event)"
                >follow</button>
            </div>
        </div>
    `;
};

const getSuggestions = () => {
    fetch("/api/suggestions/", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(users => {
            const html = users.map(user2Html).join('')
            document.querySelector(".suggestions").innerHTML = html
        });
};

const toggleFollow = ev => {
    const elem = ev.currentTarget
    console.log(elem.innerHTML)
    if (elem.innerHTML === "follow") {
        followUser(elem.dataset.userId, elem)
    } else {
        unfollowUser(elem.dataset.followingId, elem)
    }
};

const followUser = (userId, elem) => {
    console.log('there')
    const postData = {
        "user_id": userId
    };

    fetch("/api/following/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = 'unfollow';
            elem.classList.add('unfollow');
            elem.classList.remove('follow');
            elem.setAttribute('data-following-id', data.id)
            elem.setAttribute('aria-checked', 'true')
        });
};

const unfollowUser = (followingId, elem) => {
    console.log('hi')
    const deleteURL = `/api/following/${followingId}`;
    fetch(deleteURL, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = 'follow';
            elem.classList.add('follow');
            elem.classList.remove('unfollow');
            elem.removeAttribute('data-following-id');
            elem.setAttribute('aria-checked', 'false')
        });
}

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            // console.log(stories)
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};

const displayProfile = () => {
    fetch('/api/profile')
        .then(response => response.json())
        .then(profile => {
            //   console.log(profile)
            const html = profile2Html(profile);
            document.querySelector('.profile').innerHTML = html;
        })
};


const initPage = () => {
    displayProfile();
    displayPosts();
    displayStories();
    getSuggestions();
};

// invoke init page to display stories:
initPage();