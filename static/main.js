function createSidebar() {
    const sidebar = `
    <center>
        <a href="/" class="no-href-decoration"><img src="logo.png" class="w-50"></a><br><br>
        <h5>Minimize Bias, Maximize Truth</h5>
        <hr class="w-50">
        <br>
        <p class="dimmed-text">You are not logged in.</p>
        <button class="w-100 accent">Log In</button>
        <button class="w-100">Sign Up</button>
        <hr><br>
    </center>
    <h3>Trending topics</h3>
    <button class="w-100 topic"><i class="bi bi-newspaper"></i>&nbsp;&nbsp;&nbsp;Israel Hamas</button>
    <button class="w-100 topic"><i class="bi bi-newspaper"></i>&nbsp;&nbsp;&nbsp;Jay Thapar doing cocaine</button>`;

    document.getElementById("sidebar").innerHTML = sidebar;
    document.getElementById("sidebar").classList.add("col-3", "lighter", "padding");
}
function closeWindow() {
    document.getElementsByClassName("notice-bg")[0].classList.toggle("hidden");
}
function displayLoadingBar() {
    document.getElementsByClassName("big-ass-loading-bar")[0].classList.remove("hidden");
}

function article(_article) {
    return `
        <div class="row article-thumbnail lighter">
            <div class="col-3" style="background-color: var(--background-3); background-image: url(${_article.urlToImage});"></div>
            <div class="col" style="padding-left: 50px;">
                <h3>${_article.title}</h3>
                <a href="/corroborate/${btoa(_article.url)}" class="no-href-decoration">
                    <button onclick="displayLoadingBar()" class="accent">View corroborated</button>
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
    // window.open(`https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`, 'popup');
    window.open("https://www.google.com", "popup");
}