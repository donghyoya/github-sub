const setCrawlingProcessBox = (isVisible) => {
    let crawlingProcessBox = document.getElementById("crawling-process");
    if (isVisible) {
        if (crawlingProcessBox.classList.contains("d-none")) {
            crawlingProcessBox.classList.remove("d-none");
        }
    } else {
        if (!crawlingProcessBox.classList.contains("d-none")) {
            crawlingProcessBox.classList.add("d-none");
        }
    }
}

const setAiProcessBox = (isVisible) => {
    let aiProcessBox = document.getElementById("ai-process");
    if (isVisible) {
        if (aiProcessBox.classList.contains("d-none")) {
            aiProcessBox.classList.remove("d-none");
        }
    } else {
        if (!aiProcessBox.classList.contains("d-none")) {
            aiProcessBox.classList.add("d-none");
        }
    }
}