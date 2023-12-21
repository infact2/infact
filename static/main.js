function closeWindow() {
    document.getElementsByClassName('notice-bg')[0].classList.toggle('hidden');
}

function article(_article) {
    return `
        <div class="row article-thumbnail lighter">
            <div class="col-3" style="background-color: var(--background-3); background-image: url(${_article.urlToImage});"></div>
            <div class="col" style="padding-left: 50px;">
                <h3>${_article.title}</h3>
                <a href="/corroborate/${btoa(_article.url)}">
                    <button class="accent">View</button>
                </a>
                &nbsp;&nbsp;&nbsp;
                <a href="${_article.url}">View original</a><br/><br/>
                <p>Source: ${_article.source.name}<br/>By ${_article.author}</p>
            </div>
        </div>
    `;
}

function getTrendingArticles() {
    $.post("/gimme", (data) => {
        if (data.status == "ok") {
            const articles = data.articles;
            // alert(JSON.stringify(articles));
            const _articles = document.querySelector("#articles");

            for (let i = 0; i < articles.length; i++) {
                if (articles[i].title == "[Removed]") continue;
                _articles.innerHTML += article(articles[i]);
            }
        }
        else {
            alert(data.statu)
        }
    });
}

//=====================

function shareFacebook() {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`, 'popup');
}