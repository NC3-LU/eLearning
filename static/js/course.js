    function toggleInfo(card) {
        if (card.querySelector(".description") && document.getElementById("description-container")){
            const description = card.querySelector(".description").innerHTML;
            const descriptionContainer = document.getElementById("description-container");
            descriptionContainer.innerHTML = description;
        }
    }

    window.onload = function () {
        const firstCard = document.querySelector(".card");
        toggleInfo(firstCard);
    };
