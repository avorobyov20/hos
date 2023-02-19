function toggleRubricsMenu() {
    let el = document.querySelector(".hos-dropdown-mega .hos-dropdown-content");
    if (el.style.display !== "block") {
        el.style.display = "block";
        el.style.position = "fixed";
    }
    else {
        el.style.display = "none";
    }
}
function hideRubricsMenu() {
    if (document.querySelector(".hos-dropdown-mega .hos-dropdown-content") !== null) {
        if (document.querySelector(".hos-dropdown-mega .hos-dropdown-content").style.display == "block") {
            document.querySelector(".hos-dropdown-mega .hos-dropdown-content").style.display = "none";
        }
    }
}

/**
 * Conversion of string to HTML entities
 */
String.prototype.toHtmlEntities = function() {
    return this.replace(/./gm, function(s) {
        // return "&#" + s.charCodeAt(0) + ";";
        return (s.match(/[a-z0-9\s]+/i)) ? s : "&#" + s.charCodeAt(0) + ";";
    });
};

/**
 * Creation of string from HTML entities
 */
String.fromHtmlEntities = function(string) {
    return (string+"").replace(/&#\d+;/gm,function(s) {
        return String.fromCharCode(s.match(/\d+/gm)[0]);
    })
};

function load_playlist(e, el){
    e.preventDefault();
    if (el.innerHTML.slice(-3) === "(0)") {
        return false;
    }
    let playlist_pk = el.getAttribute('id').slice(12);
    $.getJSON("/" + playlist_pk + "/playlist/", function(result) {
        let res = '<div id="amazingaudioplayer-' + result.pk.toString() + '" class="amazingaudioplayer-x" style="display:block;position:relative;width:100%;height:auto;margin:0px auto 0px;">';
        res += '<ul id="hos-playlist" class="amazingaudioplayer-audios" style="display:none;">';
        let tracks = result.tracks;
        let lis = '';
        let source = [];
        for (let i = 0; i < tracks.length; i++) {
            let track = tracks[i];
            source.push([{src: track.get_audio_url, type: "audio/mpeg"}]);

            lis += '<li data-artist="' + track.artist.toHtmlEntities() + '" ' +
                'data-title="' + track.my + track.title.toHtmlEntities() + '" ' +
                'data-album="' + track.album.toHtmlEntities() + '" ' +
                'data-info="<a target=&apos;_blank&apos; href=&apos;/admin/main/pgm/' + track.pgm_num + '/&apos;>' + track.pgm_num + ' ' + track.pgm_name.toHtmlEntities() + '</a>" ' +
                'data-image="' + track.cover_url + '" ' +
                'data-duration="' + track.duration.toString() + '">' +
                '<div className="amazingaudioplayer-source" ' +
                     'data-src="' + track.get_audio_url + '" ' +
                     'data-type="audio/mpeg"/></li>';
        }
        res += lis + '</ul></div>';
        // перед заменой innerHTML необходимо остановить играющий плеер
        if (typeof window.amazingAudioPlayerObjects !== 'undefined') {
            if (typeof window.amazingAudioPlayerObjects.objects !== 'undefined'){
                for (let i = 0; i < window.amazingAudioPlayerObjects.objects.length; i++) {
                    window.amazingAudioPlayerObjects.objects[i].stopAudio();
                }
            }
        }
        window.amazingAudioPlayerObjects.objects = []; // и очистить массив экземпляров плеера
        document.getElementsByClassName("hos-active-pl")[0].classList.remove("hos-active-pl");
        el.parentNode.classList.add("hos-active-pl");
        document.getElementsByClassName("hos-container__left")[0].innerHTML = res;
        start_new_amazingaudioplayer(parseInt(playlist_pk))(); // в массиве экземпляров появится единственный элемент
        for (let i = 0; i < source.length; i++) { // у которого остается дозаполнить свойство source
            window.amazingAudioPlayerObjects.objects[0].elemArray[i].source=source[i];
        }
        window.amazingAudioPlayerObjects.objects[0].audioRun(0); // обязательно подкачиваем информацию о первом тр
        // window.amazingAudioPlayerObjects.objects[0].playAudio(); // и можно сразу начать его проигрывать
        // остается обновить описание плейлиста в правой панели
        let pldesc = '<div><h3>' + result.name.toHtmlEntities();
        if (result.note) {
            pldesc += '<br>' + result.note.toHtmlEntities();
        }
        pldesc += '</h3>';
        if (result.intro) {
            pldesc += result.intro.toHtmlEntities().split('\n').join('<br>');
        }
        pldesc += '</div>';
        document.getElementsByClassName("hos-container__right")[0].innerHTML = pldesc;
        //console.log(playlist_pk);
    });
}

function toggleFav(e, el){
    e.preventDefault();
    $.getJSON(el.getAttribute('href'), function(result) {
        if (result.status > 0) {
            if (el.classList.contains("hos-faved")) {
                el.classList.remove("hos-faved");
            }
            else {
                el.classList.add("hos-faved");
            }
        }
    });
}

function set_mytrack(e, url){
    //e.preventDefault();
    // /pgm_num/track_pos/my2/set/
    let my_no = url.slice(-6,-5);
    $.getJSON(url, function(result) {
        if (result.status > 0) {
            document.getElementById("hos-menu").children[0].lastChild.innerHTML =
                result[document.getElementById("hos-menu").children[0].lastChild.getAttribute('id')];
            document.getElementById("hos-menu").children[1].lastChild.innerHTML =
                result[document.getElementById("hos-menu").children[1].lastChild.getAttribute('id')];
            document.getElementById("hos-menu").children[2].lastChild.innerHTML =
                result[document.getElementById("hos-menu").children[2].lastChild.getAttribute('id')];
            document.getElementById("hos-menu").children[3].lastChild.innerHTML =
                result[document.getElementById("hos-menu").children[3].lastChild.getAttribute('id')];
            if (my_no === "0") {
                document.getElementsByClassName("amazingaudioplayer-item-title")[window.amazingAudioPlayerObjects.objects[0].currentItem]
                    .firstChild.firstChild.innerHTML='';
            }
            else {
                document.getElementsByClassName("amazingaudioplayer-item-title")[
                    window.amazingAudioPlayerObjects.objects[0].currentItem].firstChild.firstChild.innerHTML= '&nbsp;' + (5-parseInt(my_no)).toString() + '&nbsp;';
            }
        }
    });
}


function filter_subrubric(e, el, subrubric_pk) {
    e.preventDefault();
    document.querySelector(".hos-active-gen").classList.remove("hos-active-gen");
    el.classList.add("hos-active-gen");  // помечаем эту другую рубрику классом
    document.getElementById("hos-subrubrics").innerHTML = el.innerText + '&nbsp;&nbsp;<i class="fa fa-caret-down"></i>';
    document.getElementById("hos-subrubrics").className = "hos-dropbtn subrubric_pk_" + subrubric_pk.toString();
    hossearch_onkeyup(
        !document.getElementById('hos-switch')?
            'hos-switch-all':
            document.getElementById('hos-switch').querySelector('input:checked')
                .nextElementSibling.getAttribute('for')
    );
}

window.addEventListener("click", function(event) {
    if (event.target.id !== "hos-subrubrics" && event.target.parentNode.id !== "hos-subrubrics") {
        hideRubricsMenu();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    let modal = document.getElementById("popup-msg-modal-window");
    if (modal !== null) {
        modal.style.display = "block";
        let span = document.getElementsByClassName("hos-popup-modal-close-btn")[0];
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }

    if (document.getElementById('dragMe')) {
        // Query the element
        const resizer = document.getElementById('dragMe');
        const leftSide = resizer.previousElementSibling;
        const rightSide = resizer.nextElementSibling;
        // The current position of mouse
        let x = 0;
        let y = 0;
        let leftWidth = 0;
        // Handle the mousedown event
        // that's triggered when user drags the resizer
        const mouseDownHandler = function (e) {
            // Get the current mouse position
            x = e.clientX;
            y = e.clientY;
            leftWidth = leftSide.getBoundingClientRect().width;
            // Attach the listeners to `document`
            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        };
        const mouseMoveHandler = function (e) {
            // How far the mouse has been moved
            const dx = e.clientX - x;
            const dy = e.clientY - y;
            const newLeftWidth = ((leftWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
            leftSide.style.width = `${newLeftWidth}%`;
            resizer.style.cursor = 'col-resize';
            document.body.style.cursor = 'col-resize';
            leftSide.style.userSelect = 'none';
            leftSide.style.pointerEvents = 'none';
            rightSide.style.userSelect = 'none';
            rightSide.style.pointerEvents = 'none';
        };
        const mouseUpHandler = function () {
            resizer.style.removeProperty('cursor');
            document.body.style.removeProperty('cursor');
            leftSide.style.removeProperty('user-select');
            leftSide.style.removeProperty('pointer-events');
            rightSide.style.removeProperty('user-select');
            rightSide.style.removeProperty('pointer-events');
            // Remove the handlers of `mousemove` and `mouseup`
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };
        // Attach the handler
        resizer.addEventListener('mousedown', mouseDownHandler);
    }
    start_new_amazingaudioplayer(2)();
});

function hossearch_onkeyup(myRadio_for) {

    let input, filter, ul, li, a, i, filtered_cnt, filtered_before_active, scrolled_div;
    scrolled_div = document.querySelector(".hos-sidenav");  // прокручиваемый список плейлистов

    input = document.getElementById("hos-search");
    filter = input.value.toUpperCase();
    ul = document.getElementById("hos-menu");
    li = ul.getElementsByTagName("li");

    filtered_cnt = 0;  // счетчик количества записей, удовлетворяющих фильтру
    filtered_before_active = 0;  // счетчик количества записей, удовлетворяющих фильтру и стоящих перед или= active_pl

    for (i = 0; i < li.length; i++) {
        a = li[i].lastElementChild; // последним элементом должен быть a
        let pre_filter_passed = true;
        //if (li[i].childElementCount > 1) { // будем фильтровать, учитывая переключатель
        if (li[i].className.indexOf("subrubric_pk_") > -1) { // будем фильтровать, учитывая переключатель

            if (document.getElementById("hos-subrubrics").classList.contains("subrubric_pk_0") === false) {  //если выбрана конкретная рубрика
                if (li[i].classList.contains(document.getElementById("hos-subrubrics").className.replace("hos-dropbtn", "").trim()) === false) {
                    pre_filter_passed = false;  // и текущий li не относится к этой рубрике
                }
            }
            if (pre_filter_passed && myRadio_for === "hos-switch-fav") { //если он в положении fav
                if (li[i].firstElementChild.classList.contains("hos-faved") === false) { // а у элемента нет класса hos-faved
                    pre_filter_passed = false; // то такой элемент не должен попадать в выборку независимо от того, что введено в поиске
                }
            }
            if (pre_filter_passed === true && a.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
                filtered_cnt = filtered_cnt + 1; // подсчитываем кол-во записей, удовлетворяющих фильтру
                if (filtered_before_active >= 0) {
                    filtered_before_active = filtered_before_active + 1;
                }
                if (li[i].classList.contains("hos-active-pl")) { // если активный плейлист удовлетворяет фильтру,
                    filtered_before_active = (-1) * filtered_before_active; // перестаем увеличивать filtered_before_active
                }
            } else {
                li[i].style.display = "none";
            }
        }
    }

    if (filter === "")
        document.getElementById("hos-search-for").textContent = ""
    else
        document.getElementById("hos-search-for").textContent = filtered_cnt;

    if (filtered_before_active < 0) {  // если активный элемент попал под условие фильтрации,
        scrolled_div.scrollTop = Math.trunc(  // то прокручиваем скроллбар
            (Math.abs(filtered_before_active)-1)/filtered_cnt * (scrolled_div.scrollHeight - 9)
        );
    }
    else {
        scrolled_div.scrollTop = 0;
    }
}
