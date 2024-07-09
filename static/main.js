const months = [
    "January", "Febuary", "March", "April", "June", "July", "August", "September", "October", "November", "December"
];
let settings = {
    temp: 0
};

function createNavbar() {
    const navbar = `
        <nav class="w-100 padding-2 lighter-gradient-fill-right">
            <center>
                <div class="row" style="width: 90vw;">
                    <div class="col text-start">
                        <a href="/" class="no-href-decoration"><img src="/static/logo.png" style="height: 45px;"></a>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <b>Minimize Bias, Maximize Truth.</b>
                    </div>
                    <div class="col text-end" id="navbar-user">
                        <img src="/static/loading.gif" class="loading" style="margin: 0px; height: 45px;">
                    </div>
                </div>
            </center>
        </nav>
        <div id="navbar-filler"></div>`;
    
    document.body.innerHTML = navbar + document.body.innerHTML;

    authenticate((data) => {
        document.getElementById("navbar-user").innerHTML = `
            <a href="/dashboard" class="no-href-decoration"><button class="accent">Dashboard</button></a>
            <button onclick="logout()">Log out</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <b>${data.message.username}</b>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <img src="/static/profile.png" class="lightest" style="border-radius: 100%; width: 40px; height: 40px;">`;
    },
    () => {
        document.getElementById("navbar-user").innerHTML = `
            <a href="/login/${btoa("/dashboard")}" class="no-href-decoration"><button class="accent">Log in</button></a>
            <a href="/signup/${btoa("/dashboard")}" class="no-href-decoration"><button>Sign up</button></a>`;
    });
}

function createSidebar() {
    const sidebar = `
    <center>
        <a href="/" class="no-href-decoration"><img src="/static/logo.png" class="w-50"></a><br><br>
        <b>Minimize Bias, Maximize Truth</b>
        <hr class="w-50">
        <br>
        <div id="sidebar-user">
            <center>
                <img src="/static/loading.gif" class="loading">
            </center>
        </div>
        <hr><br>
    </center>`;

    document.getElementById("sidebar").innerHTML = sidebar;
    document.getElementById("sidebar").classList.add("col-3", "lighter", "padding");

    authenticate((data) => {
        document.getElementById("sidebar-user").innerHTML = `
            <p>
                <img src="/static/profile.png" class="lightest" style="border-radius: 100%; width: 40px; height: 40px;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>${data.message.username}</b>
            </p>
            <a href="/dashboard" class="no-href-decoration"><button class="w-100 accent">Dashboard</button></a>
            <button class="w-100" onclick="logout()">Log out</button>`;
    },
    () => {
        document.getElementById("sidebar-user").innerHTML = `
            <p class="dimmed-text">You are not logged in.</p>
            <a href="/login/${btoa("/dashboard")}" class="no-href-decoration"><button class="w-100 accent">Log in</button></a>
            <a href="/signup/${btoa("/dashboard")}" class="no-href-decoration"><button class="w-100">Sign up</button></a>`;
    });
}
function toggleWindow(id = null) {
    let window_element;
    if (id) {
        window_element = document.querySelector(`#${id}`);
    }
    else {
        window_element = document.querySelector(".notice-bg");
    }
    window_element.classList.toggle("hidden");
}
function displayLoadingBar() {
    document.getElementsByClassName("big-loading-bar")[0].classList.remove("hidden");
}

function removeLoadingBar() {
    document.getElementsByClassName("big-loading-bar")[0].classList.add("hidden");
}

function savedArticle(_article) {
    return `<div class="article-thumbnail lightest">
            <h5>${_article.title}</h5>
            <br>
            <button class="accent">View corroborated (don click for now)</button>
            <button onclick="this.parentElement.remove()" style="color: #f54242;">
                <i class="bi bi-trash3-fill"></i>
            </button>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="${atob(_article.id)}">View original</a>
        </div>`;
}

function submitCustomCorroborated() {
    displayLoadingBar();
    toggleWindow('loading');
    // openCorroborated(document.getElementById("corroborate-url").value, settings);
    window.location.href = corroborateUrl(document.getElementById("corroborate-url").value, settings);
}
function corroborateUrl(url, settings) {
    return `/corroborate/${btoa(url)}/${btoa(JSON.stringify(settings))}`;
}

function article(_article, fid, authenticated = false) {
    // alert(JSON.stringify(Object.keys(_article)))
    // alert(JSON.stringify(_article.link))
    const urlToImage = _article.urlToImage;
    const date = new Date(_article.publishedAt);
    const unscrapable = urlToImage == null;
    let saveButton = "";
    if (unscrapable) {
        const unscrapableWarning = "<i class='bi bi-exclamation-circle-fill danger'></i>&nbsp;&nbsp;&nbsp;You may have issues viewing this source. <a href='/information#unscrapable'>Learn more.</a>";
        return `
            <hr>
            <p class="grey-text">
                <i class="bi bi-eye-slash-fill"></i>&nbsp;&nbsp;&nbsp;
                This news article has been hidden. You may
                <a href="#${fid}" onclick="document.getElementById('${fid}').classList.toggle('collapse')" role="button">click here</a>
                to show article
            </p>
            <div class="collapse" id="${fid}">
                <div class="row article-thumbnail lighter padding-2">
                    <div class="col" style="padding-left: 50px;">
                        <h3 class="article-header">${_article.title}</h3>
                        <button onclick="displayLoadingBar(); toggleWindow('loading'); openCorroborated(${_article.url}, ${settings})" class="accent">View corroborated</button>
                        &nbsp;&nbsp;&nbsp;
                        <a href="${_article.url}">View original <b>(${_article.source.name})</b></a><br/><br/>
                        <p>
                            ${unscrapableWarning}
                        </p>
                    </div>
                </div>
            </div>
            <hr>`;
    }

    return `
        <div class="row article-thumbnail lighter-gradient-fill-right">
            <div class="col-4 px-0" style="background-color: var(--background-3); background-image: url(${urlToImage});">
                <div class="w-100 h-100 gradient-fill-right padding">
                    Source:
                    <h5>${_article.source.name}</h5>
                </div>
            </div>
            <div class="col padding-2" style="padding-left: 50px;">
                <h3 class="article-header">${_article.title}</h3>
                <a href="${corroborateUrl(_article.url, settings)}" class="no-href-decoration">
                    <button onclick="displayLoadingBar(); toggleWindow('loading')" class="accent">View corroborated</button>
                </a>${saveButton}
                &nbsp;&nbsp;&nbsp;
                <a href="${_article.url}">View original <b>(${_article.source.name})</a></b><br/><br/>
            </div>
        </div>`; // ${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}
}

function displayTrendingArticles(data, authenticated = false) {
    const articles = data;
    console.log(articles)
    // alert(JSON.stringify(articles));
    const _articles = document.querySelector("#articles");

    for (let i = 0; i < articles.length; i++) {
        if (articles[i].title == "[Removed]") continue;
        _articles.innerHTML += article(articles[i], i, authenticated);
    }
    const loading = document.querySelector("#articles center");
    console.log(loading)
    loading.remove();
}

function getTrendingArticles() {
    $.post("/gimme", (data) => {
        authenticate((_data) => {
            displayTrendingArticles(data, true);
        }, (_data) => {
            displayTrendingArticles(data, false);
        })
    });
}

function load() {
    $("a").click(function() {
        displayLoadingBar();
    });

    createNavbar();
    // createSidebar();
}

// =====================

function shareTwitter() {
    window.open(`https://twitter.com/intent/tweet?text=${window.location.href}`, "popup");
}
function shareInstagram() {
    window.open(`https://www.instagram.com/?url=${window.location.href}`, "popup");
}
function shareFacebook() {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${window.location.href}`, "popup");
}
function shareReddit() {
    window.open(`https://reddit.com/submit?url=${window.location.href}&title=${document.title}`, "popup");
}

// ======================

function authenticate(_success, failure = null, username = null, password = null) {
    if (!username) {
        const cookies = getUserCookies();
        username = cookies.username;
        password = cookies.password;

        if (username.length == 0) {
            if (!failure) {
                window.location.href = `/login/${btoa("/dashboard")}`;
            }
            else {
                failure({
                    "success": false,
                    "message": "Error fetching user cookies"
                });
            }
            return;
        }
    }

    $.post(getUserDataRequestString(username, password), (data) => {
        const success = data && data.success;

        if (!success) {
            if (!failure) {
                window.location.href = `/login/${btoa("/dashboard")}`;
            }
            else {
                failure(data);
            }
            return;
        }
        _success(data);
    });
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function storeUserData(username, password) {
    document.cookie = `username=${username};path=/`;
    document.cookie = `password=${password};path=/`;
}
function getUserCookies() {
    return {
        username: getCookie("username"),
        password: getCookie("password")
    };
}
function removeUserData() {
    document.cookie = `username=;expires=Thu, 18 Dec 2013 12:00:00 UTC;path=/`;
    document.cookie = `password=;expires=Thu, 18 Dec 2013 12:00:00 UTC;path=/`;
}
function logout() {
    removeUserData();
    window.location.href = "/";
}
function login(redirect) {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    displayLoadingBar();
    
    authenticate(() => {
        storeUserData(username, password);
        window.location.href = redirect;
    }, (data) => {
        document.getElementById("error").innerText = data.message;
        removeLoadingBar();
    }, username, password);
}
function signup(redirect) {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    displayLoadingBar();

    $.post(createAccountRequestString(username, password), (data) => {
        const success = data && data.success;

        if (!success) {
            document.getElementById("error").innerText = data.message;
            removeLoadingBar();
            return;
        }
        storeUserData(username, password);
        window.location.href = redirect;
    });
}

// ======================

function saveArticle(id, title) {
    const user_cookies = getUserCookies();
    $.post(`/savearticle/${btoa(user_cookies.username)}/${btoa(user_cookies.password)}/${id}/${btoa(title)}`, (data) => {
        const success = data && data.success;
        if (!success) {
            alert("Unable to save your article")
            return;
        }
        alert(JSON.stringify(data))
    })
}

function loadSavedArticles(saved_articles) {
    const saved = document.querySelector("#saved-content");
    saved.innerHTML = "";
    if (!saved_articles || saved_articles.length == 0) {
        saved.innerHTML = "You don't have any saved articles...<br><a href="/">Find some!</a>";
        return;
    }

    for (let i = 0; i < saved_articles.length; i++) {
        saved.innerHTML += savedArticle(saved_articles[i]);
    }
}

function getUserDataRequestString(username = null, password = null) {
    if (username && password) {
        return `/getuserdata/${btoa(username)}/${btoa(password)}`;
    }

    const user_cookies = getUserCookies();
    return `/getuserdata/${btoa(user_cookies.username)}/${btoa(user_cookies.password)}`;
}
function createAccountRequestString(username, password) {
    return `/createaccount/${btoa(username)}/${btoa(password)}`;
}

function loadDashboard() {
    if (!getUserCookies().username) {
        window.location.href = `/login/${btoa("/dashboard")}`;
        return;
    }

    $.post(getUserDataRequestString(), (data) => {
        const success = data && data.success;
        
        if (!success) {
            window.location.href = `/login/${btoa("/dashboard")}`;
            return;
        }

        loadSavedArticles(data.message.saved_articles);
    });
}

function switchTab(button, id) {
    const tab_contents = document.querySelectorAll(".tab-content");
    const tabs = document.querySelectorAll(".tab");

    // alert(JSON.stringify(Object.keys(tabs)));

    for (let i = 0; i < tab_contents.length; i++) { // Assume there are equal amounts of tab contents and tab buttons
        tab_contents[i].classList.add("hidden");
        tabs[i].classList.remove("accent");
    }
    document.getElementById(id).classList.remove("hidden");
    button.classList.add("accent");
}