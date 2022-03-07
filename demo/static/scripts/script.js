var round = 1;

function is_last_step(elements) {
    return elements[0].classList.contains("white")
}

function next_step() {
    var elements = document.getElementsByClassName(`row-${round + 1}`);
    
    if (! is_last_step(elements)) {
        for (var i = 0; i < elements.length; i++) {
            elements[i].classList.remove("background-hidden");
        }
        round ++;
    } 
}

function prev_step() {
    if (round != 1) {
        var elements = document.getElementsByClassName(`row-${round}`);
        for (var i = 0; i < elements.length; i++) {
            elements[i].classList.add("background-hidden");
        }
        round --;
    }
}

function jump_to_end() {
    for (i = round; i <= 6; i++) {
        next_step()
    }
}

function jump_to_start() {
    for (i = round; i >= 1; i--) {
        prev_step()
    }
}